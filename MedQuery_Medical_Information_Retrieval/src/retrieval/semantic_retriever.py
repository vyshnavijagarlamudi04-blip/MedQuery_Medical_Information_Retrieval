"""
Semantic Information Retrieval for MedQuery.
Uses Sentence-BERT (all-MiniLM-L6-v2) dense neural embeddings and cosine similarity.
"""

from typing import List, Dict, Any, Optional
import numpy as np


class SemanticRetriever:
    """Dense semantic retrieval using Sentence-BERT embeddings."""

    def __init__(self, indexer):
        self.indexer = indexer

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves Top-K passages using Sentence-BERT cosine similarity.
        """
        if not query or not query.strip():
            return []

        if self.indexer.sbert_embeddings is None:
            raise RuntimeError("SBERT embeddings are not initialized.")

        # Encode query
        model = self.indexer.get_sbert_model()
        query_emb = model.encode([query.strip()], convert_to_numpy=True, normalize_embeddings=True)[0]

        # Cosine similarity via dot product of unit-normalized vectors
        scores = np.dot(self.indexer.sbert_embeddings, query_emb)

        candidates = []
        for idx, score in enumerate(scores):
            chunk = self.indexer.chunks[idx]
            if category_filter and category_filter.lower() != "all":
                if chunk.get("category", "").lower() != category_filter.lower():
                    continue

            # Scale cosine similarity from [-1, 1] to [0, 1] if needed, or keep cosine
            # Typically SBERT cosine scores for related text are in [0.2, 0.9]
            sim_score = float(max(0.0, score))

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
                "score": round(sim_score, 4),
                "raw_score": round(float(score), 4),
                "semantic_score": round(sim_score, 4),
                "method": "semantic"
            })

        # Sort descending by cosine similarity score
        candidates.sort(key=lambda x: x["score"], reverse=True)

        results = []
        for rank, item in enumerate(candidates[:top_k], start=1):
            item["rank"] = rank
            results.append(item)

        return results
