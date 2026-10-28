"""
TF-IDF Baseline Retriever for MedQuery.
Uses Term Frequency-Inverse Document Frequency and Cosine Similarity.
"""

from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from src.preprocessing.cleaner import clean_text


class TfidfRetriever:
    """TF-IDF retrieval baseline using cosine similarity."""

    def __init__(self, indexer):
        self.indexer = indexer

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves Top-K passages using TF-IDF cosine similarity.
        """
        if not query or not query.strip():
            return []

        if self.indexer.tfidf_vectorizer is None or self.indexer.tfidf_matrix is None:
            raise RuntimeError("TF-IDF index is not initialized.")

        # Clean and vectorize query
        cleaned_query = clean_text(query)
        if not cleaned_query:
            return []

        query_vec = self.indexer.tfidf_vectorizer.transform([cleaned_query])

        # Compute cosine similarity
        scores = cosine_similarity(query_vec, self.indexer.tfidf_matrix).flatten()

        # Build candidate results
        candidates = []
        for idx, score in enumerate(scores):
            chunk = self.indexer.chunks[idx]
            if category_filter and category_filter.lower() != "all":
                if chunk.get("category", "").lower() != category_filter.lower():
                    continue

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
                "score": float(score),
                "raw_score": float(score),
                "tfidf_score": float(score),
                "method": "tfidf"
            })

        # Sort descending by score
        candidates.sort(key=lambda x: x["score"], reverse=True)

        # Deduplicate or retain top chunk per document if desired, or return top passages
        results = []
        for rank, item in enumerate(candidates[:top_k], start=1):
            item["rank"] = rank
            results.append(item)

        return results
