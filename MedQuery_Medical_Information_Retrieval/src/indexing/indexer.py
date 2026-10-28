"""
MedicalIndexer: Manages building, saving, loading, and incrementally updating
the search indexes (TF-IDF, BM25, and SBERT embeddings).
"""

import os
import json
import pickle
import time
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from src.preprocessing.cleaner import tokenize, clean_text
from src.preprocessing.chunker import DocumentChunker


class MedicalIndexer:
    """Coordinates indexing across TF-IDF, BM25, and Sentence-BERT."""

    def __init__(
        self,
        index_dir: str = "indexes",
        sbert_model_name: str = "all-MiniLM-L6-v2"
    ):
        self.index_dir = index_dir
        self.sbert_model_name = sbert_model_name
        self.sbert_model: Optional[SentenceTransformer] = None

        # Index artifacts
        self.chunks: List[Dict[str, Any]] = []
        self.tfidf_vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        self.bm25_model: Optional[BM25Okapi] = None
        self.tokenized_corpus: List[List[str]] = []
        self.sbert_embeddings: Optional[np.ndarray] = None
        self.metadata: Dict[str, Any] = {}

    def get_sbert_model(self) -> SentenceTransformer:
        """Lazy load SentenceTransformer model."""
        if self.sbert_model is None:
            print(f"Loading SentenceTransformer model '{self.sbert_model_name}'...")
            self.sbert_model = SentenceTransformer(self.sbert_model_name)
        return self.sbert_model

    def build_indexes(
        self,
        chunks: List[Dict[str, Any]],
        force_sbert_rebuild: bool = False
    ) -> None:
        """
        Builds TF-IDF, BM25, and SBERT indexes from a list of chunk dictionaries.
        """
        if not chunks:
            raise ValueError("Cannot build index from empty chunks list.")

        self.chunks = chunks
        print(f"Building indexes for {len(chunks)} passages...")
        start_time = time.time()

        # 1. Build TF-IDF index
        print("  -> Computing TF-IDF vectorizer and sparse matrix...")
        texts = [c.get("clean_chunk_text", clean_text(c["chunk_text"])) for c in self.chunks]
        self.tfidf_vectorizer = TfidfVectorizer(
            tokenizer=tokenize,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1
        )
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)

        # 2. Build BM25 index
        print("  -> Tokenizing passages and fitting BM25Okapi...")
        self.tokenized_corpus = [tokenize(c["chunk_text"]) for c in self.chunks]
        self.bm25_model = BM25Okapi(self.tokenized_corpus)

        # 3. Generate SBERT Embeddings
        embeddings_path = os.path.join(self.index_dir, "sbert_embeddings.npy")
        if (
            not force_sbert_rebuild
            and os.path.exists(embeddings_path)
            and len(self.chunks) == self._get_cached_chunk_count()
        ):
            print("  -> Loading cached SBERT embeddings...")
            self.sbert_embeddings = np.load(embeddings_path)
        else:
            print(f"  -> Generating SBERT embeddings with {self.sbert_model_name}...")
            model = self.get_sbert_model()
            # Encode chunk texts
            texts_to_embed = [
                f"{c.get('title', '')}: {c.get('chunk_text', '')}"
                for c in self.chunks
            ]
            self.sbert_embeddings = model.encode(
                texts_to_embed,
                show_progress_bar=True,
                convert_to_numpy=True,
                normalize_embeddings=True
            )

        elapsed = time.time() - start_time
        print(f"Index building completed in {elapsed:.2f}s.")

        self.metadata = {
            "num_chunks": len(self.chunks),
            "num_documents": len(set(c["document_id"] for c in self.chunks)),
            "sbert_model": self.sbert_model_name,
            "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "build_duration_sec": round(elapsed, 2)
        }

    def _get_cached_chunk_count(self) -> int:
        meta_path = os.path.join(self.index_dir, "metadata.json")
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                    return meta.get("num_chunks", -1)
            except Exception:
                return -1
        return -1

    def save(self) -> None:
        """Saves all indexes to disk in index_dir."""
        os.makedirs(self.index_dir, exist_ok=True)
        print(f"Saving indexes to '{self.index_dir}'...")

        # Save chunks
        chunks_path = os.path.join(self.index_dir, "chunks.pkl")
        with open(chunks_path, "wb") as f:
            pickle.dump(self.chunks, f)

        # Save TF-IDF
        tfidf_path = os.path.join(self.index_dir, "tfidf.pkl")
        with open(tfidf_path, "wb") as f:
            pickle.dump({
                "vectorizer": self.tfidf_vectorizer,
                "matrix": self.tfidf_matrix
            }, f)

        # Save BM25
        bm25_path = os.path.join(self.index_dir, "bm25.pkl")
        with open(bm25_path, "wb") as f:
            pickle.dump({
                "model": self.bm25_model,
                "corpus": self.tokenized_corpus
            }, f)

        # Save SBERT Embeddings
        if self.sbert_embeddings is not None:
            emb_path = os.path.join(self.index_dir, "sbert_embeddings.npy")
            np.save(emb_path, self.sbert_embeddings)

        # Save metadata
        meta_path = os.path.join(self.index_dir, "metadata.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)

        print("All index artifacts saved successfully.")

    def load(self) -> bool:
        """Loads all indexes from disk. Returns True if successful, False otherwise."""
        chunks_path = os.path.join(self.index_dir, "chunks.pkl")
        tfidf_path = os.path.join(self.index_dir, "tfidf.pkl")
        bm25_path = os.path.join(self.index_dir, "bm25.pkl")
        emb_path = os.path.join(self.index_dir, "sbert_embeddings.npy")
        meta_path = os.path.join(self.index_dir, "metadata.json")

        if not all(os.path.exists(p) for p in [chunks_path, tfidf_path, bm25_path, emb_path]):
            return False

        print(f"Loading indexes from '{self.index_dir}'...")
        with open(chunks_path, "rb") as f:
            self.chunks = pickle.load(f)

        with open(tfidf_path, "rb") as f:
            data = pickle.load(f)
            self.tfidf_vectorizer = data["vectorizer"]
            self.tfidf_matrix = data["matrix"]

        with open(bm25_path, "rb") as f:
            data = pickle.load(f)
            self.bm25_model = data["model"]
            self.tokenized_corpus = data["corpus"]

        self.sbert_embeddings = np.load(emb_path)

        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)

        print(f"Loaded index successfully with {len(self.chunks)} chunks.")
        return True

    def add_document(self, doc_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Dynamically appends new document passages, generates new embeddings,
        and updates the search index in real time.
        """
        new_chunks = DocumentChunker.chunk_structured_document(doc_dict)
        if not new_chunks:
            # Try free text chunking
            content = doc_dict.get("content", "")
            doc_id = doc_dict.get("document_id", f"DOC_UPLOAD_{int(time.time())}")
            title = doc_dict.get("title", "Uploaded Document")
            category = doc_dict.get("category", "General")
            new_chunks = DocumentChunker.chunk_free_text(
                content,
                doc_id=doc_id,
                title=title,
                category=category,
                source=doc_dict.get("source", "User Upload")
            )

        if not new_chunks:
            return []

        # Encode new chunks with SBERT
        model = self.get_sbert_model()
        new_texts = [f"{c.get('title', '')}: {c.get('chunk_text', '')}" for c in new_chunks]
        new_embs = model.encode(new_texts, convert_to_numpy=True, normalize_embeddings=True)

        # Append to existing
        self.chunks.extend(new_chunks)
        if self.sbert_embeddings is not None:
            self.sbert_embeddings = np.vstack([self.sbert_embeddings, new_embs])
        else:
            self.sbert_embeddings = new_embs

        # Update TF-IDF & BM25
        texts = [c.get("clean_chunk_text", clean_text(c["chunk_text"])) for c in self.chunks]
        self.tfidf_vectorizer = TfidfVectorizer(
            tokenizer=tokenize,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1
        )
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)

        self.tokenized_corpus = [tokenize(c["chunk_text"]) for c in self.chunks]
        self.bm25_model = BM25Okapi(self.tokenized_corpus)

        # Update metadata & persist
        self.metadata["num_chunks"] = len(self.chunks)
        self.metadata["num_documents"] = len(set(c["document_id"] for c in self.chunks))
        self.metadata["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.save()

        return new_chunks
