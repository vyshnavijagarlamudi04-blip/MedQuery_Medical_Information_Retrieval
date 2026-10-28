"""
SearchService: Orchestrates index loading, query execution, latency measurement,
document uploads (TXT, PDF, CSV), and search history logging.
"""

import os
import io
import time
import uuid
import json
from typing import List, Dict, Any, Optional
import pandas as pd
from pypdf import PdfReader

from src.indexing.indexer import MedicalIndexer
from src.retrieval.tfidf_retriever import TfidfRetriever
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.semantic_retriever import SemanticRetriever
from src.retrieval.hybrid_retriever import HybridRetriever
from src.evaluation.evaluator import IREvaluator


class SearchService:
    """Singleton service for retrieval and document operations."""

    def __init__(self, index_dir: str = "indexes"):
        self.index_dir = index_dir
        self.indexer = MedicalIndexer(index_dir=index_dir)
        self.history_file = os.path.join("data", "search_history.json")
        self.search_history: List[Dict[str, Any]] = []

        self.retrievers: Dict[str, Any] = {}
        self._load_search_history()

    def initialize(self) -> None:
        """Loads index into memory and initializes retrieval algorithms."""
        print("Initializing SearchService...")
        if not self.indexer.load():
            print("Indexes not found on disk. Building now...")
            chunk_file = "data/chunked_medical_documents.csv"
            if not os.path.exists(chunk_file):
                from scripts.preprocess import preprocess_and_chunk
                preprocess_and_chunk()

            df = pd.read_csv(chunk_file, encoding="utf-8")
            chunks = df.to_dict(orient="records")
            self.indexer.build_indexes(chunks)
            self.indexer.save()

        # Instantiate retrievers
        self.retrievers = {
            "tfidf": TfidfRetriever(self.indexer),
            "bm25": BM25Retriever(self.indexer),
            "semantic": SemanticRetriever(self.indexer),
            "hybrid": HybridRetriever(self.indexer, bm25_weight=0.5, semantic_weight=0.5)
        }
        print("SearchService initialized successfully with all 4 retrieval engines ready.")

    def search(
        self,
        query: str,
        method: str = "hybrid",
        top_k: int = 5,
        bm25_weight: float = 0.5,
        semantic_weight: float = 0.5,
        category_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes search using the specified IR method and measures latency.
        """
        method_key = method.lower().strip()
        if method_key not in self.retrievers:
            method_key = "hybrid"

        retriever = self.retrievers[method_key]

        start_time = time.perf_counter()

        if method_key == "hybrid":
            results = retriever.retrieve(
                query,
                top_k=top_k,
                bm25_weight=bm25_weight,
                semantic_weight=semantic_weight,
                category_filter=category_filter
            )
        else:
            results = retriever.retrieve(
                query,
                top_k=top_k,
                category_filter=category_filter
            )

        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # Log into search history
        top_title = results[0]["title"] if results else ""
        top_score = results[0]["score"] if results else 0.0

        history_entry = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "query": query,
            "method": method_key,
            "top_k": top_k,
            "search_time_ms": latency_ms,
            "top_title": top_title,
            "top_score": top_score
        }
        self.search_history.insert(0, history_entry)
        if len(self.search_history) > 100:
            self.search_history = self.search_history[:100]
        self._save_search_history()

        return {
            "query": query,
            "method": method_key,
            "total_results": len(results),
            "search_time_ms": latency_ms,
            "results": results,
            "category_filter": category_filter,
            "bm25_weight": bm25_weight if method_key == "hybrid" else None,
            "semantic_weight": semantic_weight if method_key == "hybrid" else None
        }

    def compare_methods(
        self,
        query: str,
        top_k: int = 5,
        category_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes TF-IDF, BM25, Semantic, and Hybrid simultaneously for the same query.
        """
        comparisons = {}
        for method_name, retriever in self.retrievers.items():
            start_time = time.perf_counter()
            results = retriever.retrieve(query, top_k=top_k, category_filter=category_filter)
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            comparisons[method_name] = {
                "method": method_name,
                "search_time_ms": latency_ms,
                "results": results
            }
        return {
            "query": query,
            "methods": comparisons
        }

    def upload_document(
        self,
        file_bytes: bytes,
        filename: str,
        category: str = "General",
        title: Optional[str] = None,
        disease: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Safely processes uploaded TXT, PDF, or CSV document, extracts text,
        chunks it, and updates search indexes dynamically.
        """
        ext = os.path.splitext(filename)[1].lower()
        extracted_text = ""
        doc_title = title or os.path.splitext(filename)[0]

        if ext == ".txt":
            extracted_text = file_bytes.decode("utf-8", errors="replace").strip()
        elif ext == ".pdf":
            try:
                reader = PdfReader(io.BytesIO(file_bytes))
                pages_text = []
                for p in reader.pages:
                    txt = p.extract_text()
                    if txt:
                        pages_text.append(txt)
                extracted_text = "\n\n".join(pages_text).strip()
            except Exception as e:
                raise ValueError(f"Could not read PDF: {str(e)}")
        elif ext == ".csv":
            try:
                df = pd.read_csv(io.BytesIO(file_bytes), encoding="utf-8")
                # If structured medical CSV
                if "content" in df.columns:
                    added_docs = []
                    for _, row in df.iterrows():
                        doc_dict = row.to_dict()
                        if not doc_dict.get("document_id"):
                            doc_dict["document_id"] = f"DOC_UPL_{uuid.uuid4().hex[:6]}"
                        chunks = self.indexer.add_document(doc_dict)
                        added_docs.append(doc_dict.get("title", "Untitled"))
                    return {
                        "status": "success",
                        "message": f"Successfully indexed {len(added_docs)} documents from CSV.",
                        "documents_added": len(added_docs)
                    }
                else:
                    # Concatenate columns
                    extracted_text = df.to_string()
            except Exception as e:
                raise ValueError(f"Could not read CSV: {str(e)}")
        else:
            raise ValueError(f"Unsupported file format: {ext}. Only TXT, PDF, and CSV are allowed.")

        if not extracted_text:
            raise ValueError("The uploaded document contains no readable text.")

        doc_id = f"DOC_UPL_{uuid.uuid4().hex[:6].upper()}"
        doc_dict = {
            "document_id": doc_id,
            "title": doc_title,
            "category": category,
            "disease": disease or doc_title,
            "content": extracted_text,
            "source": f"Upload: {filename}"
        }

        # Add to indexer
        new_chunks = self.indexer.add_document(doc_dict)

        # Refresh retrievers with updated index
        self.retrievers["tfidf"] = TfidfRetriever(self.indexer)
        self.retrievers["bm25"] = BM25Retriever(self.indexer)
        self.retrievers["semantic"] = SemanticRetriever(self.indexer)
        self.retrievers["hybrid"] = HybridRetriever(self.indexer)

        return {
            "status": "success",
            "document_id": doc_id,
            "title": doc_title,
            "category": category,
            "chunks_created": len(new_chunks),
            "total_collection_chunks": len(self.indexer.chunks)
        }

    def get_documents_catalog(self) -> Dict[str, Any]:
        """Returns catalog of indexed unique documents with chunk count and preview."""
        doc_map = {}
        for c in self.indexer.chunks:
            did = c["document_id"]
            if did not in doc_map:
                doc_map[did] = {
                    "document_id": did,
                    "title": c.get("title", ""),
                    "category": c.get("category", "General"),
                    "disease": c.get("disease", ""),
                    "chunk_count": 0,
                    "source": c.get("source", "MedQuery Knowledgebase"),
                    "preview": c.get("chunk_text", "")[:180] + "..."
                }
            doc_map[did]["chunk_count"] += 1

        docs_list = list(doc_map.values())
        return {
            "total_documents": len(docs_list),
            "total_chunks": len(self.indexer.chunks),
            "documents": docs_list
        }

    def get_categories(self) -> List[Dict[str, Any]]:
        """Returns distinct categories and their document counts."""
        catalog = self.get_documents_catalog()["documents"]
        counts = {}
        for d in catalog:
            cat = d["category"] or "General"
            counts[cat] = counts.get(cat, 0) + 1
        return [{"category": k, "count": v} for k, v in sorted(counts.items())]

    def get_search_history(self) -> List[Dict[str, Any]]:
        """Returns recent searches."""
        return self.search_history

    def get_evaluation_data(self) -> Dict[str, Any]:
        """Returns benchmark evaluation metrics and status."""
        eval_csv = "results/evaluation_results.csv"
        chart_path = "results/evaluation_comparison.png"

        if not os.path.exists(eval_csv):
            # Run evaluation on the fly if not cached
            from scripts.evaluate import run_benchmark
            run_benchmark()

        df = pd.read_csv(eval_csv)
        summary_table = df.to_dict(orient="records")

        return {
            "status": "available",
            "last_evaluated_at": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getmtime(eval_csv))),
            "queries_evaluated": 35,
            "summary_table": summary_table,
            "chart_url": "/static/results/evaluation_comparison.png" if os.path.exists(chart_path) else None
        }

    def run_evaluation(self) -> Dict[str, Any]:
        """Triggers a fresh evaluation run."""
        from scripts.evaluate import run_benchmark
        run_benchmark()
        return self.get_evaluation_data()

    def _load_search_history(self) -> None:
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.search_history = json.load(f)
            except Exception:
                self.search_history = []

    def _save_search_history(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.search_history, f, indent=2)
        except Exception as e:
            print(f"Warning: could not save search history: {e}")
