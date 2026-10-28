"""
Hybrid Retrieval and Re-ranking for MedQuery.
Combines BM25 keyword matching with Sentence-BERT dense semantic ranking.
"""

from typing import List, Dict, Any, Optional
import numpy as np

from src.preprocessing.cleaner import tokenize
from .bm25_retriever import BM25Retriever
from .semantic_retriever import SemanticRetriever


class HybridRetriever:
    """
    Hybrid retriever combining lexical (BM25) and dense semantic (SBERT) retrieval,
    with configurable weights and candidate re-ranking.
    """

    def __init__(
        self,
        indexer,
        bm25_weight: float = 0.5,
        semantic_weight: float = 0.5,
        candidate_pool_size: int = 25
    ):
        self.indexer = indexer
        self.bm25_weight = bm25_weight
        self.semantic_weight = semantic_weight
        self.candidate_pool_size = candidate_pool_size

        self.bm25_retriever = BM25Retriever(indexer)
        self.semantic_retriever = SemanticRetriever(indexer)

    def set_weights(self, bm25_weight: float, semantic_weight: float) -> None:
        """Configures the interpolation weights."""
        total = bm25_weight + semantic_weight
        if total <= 0:
            bm25_weight, semantic_weight = 0.5, 0.5
            total = 1.0
        self.bm25_weight = bm25_weight / total
        self.semantic_weight = semantic_weight / total

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        bm25_weight: Optional[float] = None,
        semantic_weight: Optional[float] = None,
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes hybrid retrieval:
        1. Fetch top candidates from BM25 and Semantic retrievers.
        2. Form candidate pool.
        3. Compute normalized scores and linear combination.
        4. Re-rank and return Top-K.
        """
        if not query or not query.strip():
            return []

        # Determine weights
        w_bm25 = self.bm25_weight if bm25_weight is None else bm25_weight
        w_sem = self.semantic_weight if semantic_weight is None else semantic_weight
        total_w = w_bm25 + w_sem
        if total_w <= 0:
            w_bm25, w_sem = 0.5, 0.5
        else:
            w_bm25, w_sem = w_bm25 / total_w, w_sem / total_w

        # 1. Retrieve candidate pool from BM25
        bm25_candidates = self.bm25_retriever.retrieve(
            query,
            top_k=self.candidate_pool_size,
            category_filter=category_filter
        )

        # 2. Retrieve candidate pool from Semantic
        semantic_candidates = self.semantic_retriever.retrieve(
            query,
            top_k=self.candidate_pool_size,
            category_filter=category_filter
        )

        # Build candidate map by chunk_id
        candidate_map: Dict[str, Dict[str, Any]] = {}

        # Add BM25 candidates
        for c in bm25_candidates:
            cid = c["chunk_id"]
            candidate_map[cid] = {
                "chunk_idx": c["chunk_idx"],
                "document_id": c["document_id"],
                "chunk_id": cid,
                "title": c["title"],
                "category": c["category"],
                "disease": c["disease"],
                "section": c["section"],
                "passage": c["passage"],
                "source": c["source"],
                "bm25_raw": c["bm25_score"],
                "norm_bm25": c["norm_bm25_score"],
                "semantic_score": 0.0,
                "method": "hybrid"
            }

        # Add / update with Semantic candidates
        model = self.indexer.get_sbert_model()
        query_emb = model.encode([query.strip()], convert_to_numpy=True, normalize_embeddings=True)[0]

        for c in semantic_candidates:
            cid = c["chunk_id"]
            if cid in candidate_map:
                candidate_map[cid]["semantic_score"] = c["semantic_score"]
            else:
                # Also compute BM25 score for this chunk if not in top BM25
                tokens = tokenize(query)
                chunk_tokens = self.indexer.tokenized_corpus[c["chunk_idx"]]
                # Approximate BM25 or compute on the fly
                raw_bm25 = float(self.indexer.bm25_model.get_batch_scores(tokens, [c["chunk_idx"]])[0]) if hasattr(self.indexer.bm25_model, "get_batch_scores") else 0.0
                
                candidate_map[cid] = {
                    "chunk_idx": c["chunk_idx"],
                    "document_id": c["document_id"],
                    "chunk_id": cid,
                    "title": c["title"],
                    "category": c["category"],
                    "disease": c["disease"],
                    "section": c["section"],
                    "passage": c["passage"],
                    "source": c["source"],
                    "bm25_raw": round(raw_bm25, 4),
                    "norm_bm25": 0.0,
                    "semantic_score": c["semantic_score"],
                    "method": "hybrid"
                }

        if not candidate_map:
            return []

        # Ensure all candidates in the candidate pool have both BM25 and Semantic scores computed
        all_candidates = list(candidate_map.values())
        indices = [c["chunk_idx"] for c in all_candidates]

        # Compute exact semantic score for any candidate that only had BM25
        for c in all_candidates:
            if c["semantic_score"] == 0.0:
                chunk_emb = self.indexer.sbert_embeddings[c["chunk_idx"]]
                cos_sim = float(np.dot(chunk_emb, query_emb))
                c["semantic_score"] = round(float(max(0.0, cos_sim)), 4)

        # Normalize BM25 across candidates
        bm25_vals = [c["bm25_raw"] for c in all_candidates]
        max_bm25 = max(bm25_vals) if bm25_vals else 1.0
        min_bm25 = min(bm25_vals) if bm25_vals else 0.0
        span = max_bm25 - min_bm25 if max_bm25 > min_bm25 else 1.0

        for c in all_candidates:
            norm_b = (c["bm25_raw"] - min_bm25) / span if max_bm25 > 0 else 0.0
            c["norm_bm25"] = round(float(norm_b), 4)

            # Re-ranking Formula:
            # Hybrid Score = w_bm25 * norm_bm25 + w_sem * semantic_score
            hybrid_score = (w_bm25 * c["norm_bm25"]) + (w_sem * c["semantic_score"])
            c["hybrid_score"] = round(float(hybrid_score), 4)
            c["score"] = c["hybrid_score"]
            c["raw_score"] = c["hybrid_score"]
            c["bm25_weight"] = round(w_bm25, 2)
            c["semantic_weight"] = round(w_sem, 2)

        # Sort candidate pool by hybrid score descending (Re-ranking step)
        all_candidates.sort(key=lambda x: x["hybrid_score"], reverse=True)

        results = []
        for rank, item in enumerate(all_candidates[:top_k], start=1):
            item["rank"] = rank
            results.append(item)

        return results
