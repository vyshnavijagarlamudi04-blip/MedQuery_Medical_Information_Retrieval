"""
BM25 Information Retrieval for MedQuery.
Uses rank-bm25 (BM25Okapi) for probabilistic keyword retrieval.
"""

from typing import List, Dict, Any, Optional
import numpy as np
from src.preprocessing.cleaner import tokenize


class BM25Retriever:
    """Keyword-based probabilistic retrieval using BM25Okapi."""

    def __init__(self, indexer):
        self.indexer = indexer

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves Top-K passages using BM25 scoring.
        """
        if not query or not query.strip():
            return []

        if self.indexer.bm25_model is None:
            raise RuntimeError("BM25 index is not initialized.")

        tokens = tokenize(query)
        if not tokens:
            return []

        raw_scores = self.indexer.bm25_model.get_scores(tokens)

        # Min-max normalization for BM25 scores
        max_score = float(np.max(raw_scores)) if len(raw_scores) > 0 else 1.0
        min_score = float(np.min(raw_scores)) if len(raw_scores) > 0 else 0.0
        score_range = max_score - min_score if max_score > min_score else 1.0

        candidates = []
        for idx, raw_score in enumerate(raw_scores):
            chunk = self.indexer.chunks[idx]
            if category_filter and category_filter.lower() != "all":
                if chunk.get("category", "").lower() != category_filter.lower():
                    continue

            norm_score = float((raw_score - min_score) / score_range) if max_score > 0 else 0.0

            candidates.append({
                "chunk_idx": idx,
                "document_id": chunk["document_id"],
                "chunk_id": chunk["chunk_id"],
                "title": chunk["title"],
                "category": chunk.get("category", "General"),
                "disease": chunk.get("disease", ""),
                "section": chunk.get("section", ""),
                "passage": chunk["chunk_text"],
                "source": chunk.get("source", ""),
                "score": round(norm_score, 4),
                "raw_score": round(float(raw_score), 4),
                "bm25_score": round(float(raw_score), 4),
                "norm_bm25_score": round(norm_score, 4),
                "method": "bm25"
            })

        # Sort descending by raw BM25 score
        candidates.sort(key=lambda x: x["raw_score"], reverse=True)

        results = []
        for rank, item in enumerate(candidates[:top_k], start=1):
            item["rank"] = rank
            results.append(item)

        return results
