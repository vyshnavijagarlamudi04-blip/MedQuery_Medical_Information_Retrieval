"""
IREvaluator: Calculates standard Information Retrieval metrics
(Precision@K, Recall@K, F1@K, MAP, MRR, NDCG@K) for medical queries
against ground-truth relevance judgements.
Follows standard TREC / Manning-Raghavan IR evaluation protocols.
"""

import math
import os
from typing import List, Dict, Any, Set, Tuple
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class IREvaluator:
    """Evaluates IR systems across standard metrics."""

    @staticmethod
    def deduplicate_by_document(retrieved: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Retains the highest-scoring passage for each unique document_id
        to evaluate document-level retrieval accuracy.
        """
        seen_docs = set()
        deduped = []
        for item in retrieved:
            doc_id = item.get("document_id")
            if doc_id and doc_id not in seen_docs:
                seen_docs.add(doc_id)
                deduped.append(item)
        return deduped

    @staticmethod
    def precision_at_k(retrieved: List[Dict[str, Any]], relevant_ids: Set[str], k: int) -> float:
        """Precision at rank K: fraction of top-K retrieved documents that are relevant."""
        if k <= 0:
            return 0.0
        top_k = retrieved[:k]
        if not top_k:
            return 0.0
        rel_count = sum(1 for item in top_k if item.get("document_id") in relevant_ids)
        return min(1.0, rel_count / k)

    @staticmethod
    def recall_at_k(retrieved: List[Dict[str, Any]], relevant_ids: Set[str], k: int) -> float:
        """Recall at rank K: fraction of total relevant documents retrieved in top-K."""
        if not relevant_ids or k <= 0:
            return 0.0
        top_k = retrieved[:k]
        retrieved_relevant_docs = {item["document_id"] for item in top_k if item.get("document_id") in relevant_ids}
        return min(1.0, len(retrieved_relevant_docs) / len(relevant_ids))

    @staticmethod
    def f1_at_k(precision: float, recall: float) -> float:
        """Harmonic mean of precision and recall."""
        if precision + recall <= 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)

    @staticmethod
    def reciprocal_rank(retrieved: List[Dict[str, Any]], relevant_ids: Set[str], max_k: int = 10) -> float:
        """Reciprocal rank of the first relevant document."""
        for rank, item in enumerate(retrieved[:max_k], start=1):
            if item.get("document_id") in relevant_ids:
                return 1.0 / rank
        return 0.0

    @staticmethod
    def average_precision(retrieved: List[Dict[str, Any]], relevant_ids: Set[str], max_k: int = 10) -> float:
        """Average Precision (AP) up to rank max_k."""
        if not relevant_ids:
            return 0.0

        top_items = retrieved[:max_k]
        relevant_seen = 0
        precisions_sum = 0.0

        for rank, item in enumerate(top_items, start=1):
            if item.get("document_id") in relevant_ids:
                relevant_seen += 1
                precisions_sum += relevant_seen / rank

        denominator = min(len(relevant_ids), max_k)
        if denominator == 0:
            return 0.0
        return min(1.0, precisions_sum / denominator)

    @staticmethod
    def ndcg_at_k(retrieved: List[Dict[str, Any]], relevant_ids: Set[str], k: int = 10) -> float:
        """Normalized Discounted Cumulative Gain at rank K."""
        top_k = retrieved[:k]
        if not top_k or not relevant_ids:
            return 0.0

        # DCG calculation
        dcg = 0.0
        for i, item in enumerate(top_k, start=1):
            rel = 1 if item.get("document_id") in relevant_ids else 0
            if rel > 0:
                dcg += 1.0 / math.log2(i + 1)

        # IDCG calculation (all relevant documents ranked at top)
        idcg = 0.0
        ideal_rels = min(len(relevant_ids), k)
        for i in range(1, ideal_rels + 1):
            idcg += 1.0 / math.log2(i + 1)

        if idcg == 0.0:
            return 0.0
        return min(1.0, dcg / idcg)

    @classmethod
    def evaluate_retriever_on_queries(
        cls,
        retriever,
        queries: List[Dict[str, Any]],
        method_name: str,
        k_values: List[int] = [5, 10]
    ) -> Dict[str, Any]:
        """
        Runs evaluation for a single retrieval method across all queries.
        """
        all_metrics = []
        max_k = max(k_values)
        fetch_k = max_k * 3  # Fetch more chunks to ensure unique document coverage

        for q in queries:
            query_text = q["query"]
            rel_ids_raw = q.get("relevant_document_ids", "")
            relevant_ids = set([doc_id.strip() for doc_id in str(rel_ids_raw).split(",") if doc_id.strip()])

            raw_retrieved = retriever.retrieve(query_text, top_k=fetch_k)
            retrieved = cls.deduplicate_by_document(raw_retrieved)[:max_k]

            q_metrics = {
                "query_id": q.get("query_id", ""),
                "query": query_text,
                "relevant_count": len(relevant_ids)
            }

            for k in k_values:
                p = cls.precision_at_k(retrieved, relevant_ids, k)
                r = cls.recall_at_k(retrieved, relevant_ids, k)
                f1 = cls.f1_at_k(p, r)
                ndcg = cls.ndcg_at_k(retrieved, relevant_ids, k)

                q_metrics[f"precision@{k}"] = p
                q_metrics[f"recall@{k}"] = r
                q_metrics[f"f1@{k}"] = f1
                q_metrics[f"ndcg@{k}"] = ndcg

            q_metrics["rr"] = cls.reciprocal_rank(retrieved, relevant_ids, max_k)
            q_metrics["ap"] = cls.average_precision(retrieved, relevant_ids, max_k)
            all_metrics.append(q_metrics)

        # Aggregate averages
        summary = {
            "method": method_name,
            "num_queries": len(queries),
            "map": round(float(np.mean([m["ap"] for m in all_metrics])), 4),
            "mrr": round(float(np.mean([m["rr"] for m in all_metrics])), 4),
        }

        for k in k_values:
            summary[f"precision@{k}"] = round(float(np.mean([m[f"precision@{k}"] for m in all_metrics])), 4)
            summary[f"recall@{k}"] = round(float(np.mean([m[f"recall@{k}"] for m in all_metrics])), 4)
            summary[f"f1@{k}"] = round(float(np.mean([m[f"f1@{k}"] for m in all_metrics])), 4)
            summary[f"ndcg@{k}"] = round(float(np.mean([m[f"ndcg@{k}"] for m in all_metrics])), 4)

        return {
            "summary": summary,
            "query_details": all_metrics
        }

    @staticmethod
    def generate_comparison_chart(
        df_results: pd.DataFrame,
        output_image_path: str = "results/evaluation_comparison.png"
    ) -> None:
        """
        Generates and saves a clean, publication-ready comparison bar chart.
        """
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        methods = df_results["method"].tolist()

        metrics = ["precision@5", "recall@5", "f1@5", "map", "mrr", "ndcg@5"]
        labels = ["P@5", "R@5", "F1@5", "MAP", "MRR", "NDCG@5"]

        x = np.arange(len(labels))
        width = 0.18
        fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

        # Medical healthcare aesthetic color palette: Slate, Sky Blue, Teal, Indigo
        colors = ["#64748b", "#0284c7", "#0d9488", "#2563eb"]

        for i, (method, color) in enumerate(zip(methods, colors[:len(methods)])):
            row = df_results[df_results["method"] == method].iloc[0]
            vals = [float(row.get(m, 0.0)) for m in metrics]
            bars = ax.bar(x + (i - 1.5) * width, vals, width, label=method.upper(), color=color, alpha=0.92)
            # Add small value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                if height > 0.05:
                    ax.annotate(f"{height:.2f}",
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom', fontsize=7, fontweight='bold', color="#1e293b")

        ax.set_ylabel("Metric Score", fontsize=11, fontweight="bold", color="#1e293b")
        ax.set_title("MedQuery Information Retrieval Benchmark Comparison\n(TF-IDF vs BM25 vs SBERT Semantic vs Hybrid)", fontsize=13, fontweight="bold", pad=15, color="#0f172a")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=10, fontweight="bold", color="#334155")
        ax.set_ylim(0, 1.15)
        ax.grid(axis="y", linestyle="--", alpha=0.4, color="#cbd5e1")
        ax.set_facecolor("#f8fafc")
        fig.patch.set_facecolor("#ffffff")
        ax.legend(loc="upper right", frameon=True, fontsize=9, facecolor="#ffffff", edgecolor="#e2e8f0")

        plt.tight_layout()
        plt.savefig(output_image_path, dpi=300)
        plt.close()
        print(f"Refined comparison chart saved to {output_image_path}")
