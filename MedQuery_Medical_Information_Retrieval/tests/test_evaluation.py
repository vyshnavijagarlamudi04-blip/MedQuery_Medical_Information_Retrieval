"""
Unit tests for Information Retrieval evaluation metrics.
"""

import pytest
from src.evaluation.evaluator import IREvaluator


def test_precision_recall_f1():
    retrieved = [
        {"document_id": "DOC_1"},
        {"document_id": "DOC_2"},
        {"document_id": "DOC_3"},
        {"document_id": "DOC_4"},
        {"document_id": "DOC_5"},
    ]
    relevant = {"DOC_1", "DOC_3"}

    p5 = IREvaluator.precision_at_k(retrieved, relevant, k=5)
    assert p5 == 2 / 5

    r5 = IREvaluator.recall_at_k(retrieved, relevant, k=5)
    assert r5 == 1.0  # both relevant retrieved

    f1 = IREvaluator.f1_at_k(p5, r5)
    assert round(f1, 4) == round(2 * (0.4 * 1.0) / (0.4 + 1.0), 4)


def test_mrr():
    retrieved_1 = [{"document_id": "DOC_A"}, {"document_id": "DOC_B"}]
    relevant_1 = {"DOC_A"}
    assert IREvaluator.reciprocal_rank(retrieved_1, relevant_1) == 1.0

    retrieved_2 = [{"document_id": "DOC_X"}, {"document_id": "DOC_A"}]
    assert IREvaluator.reciprocal_rank(retrieved_2, relevant_1) == 0.5

    retrieved_none = [{"document_id": "DOC_X"}, {"document_id": "DOC_Y"}]
    assert IREvaluator.reciprocal_rank(retrieved_none, relevant_1) == 0.0


def test_ndcg_perfect():
    retrieved = [{"document_id": "DOC_1"}, {"document_id": "DOC_2"}, {"document_id": "DOC_3"}]
    relevant = {"DOC_1", "DOC_2"}
    ndcg = IREvaluator.ndcg_at_k(retrieved, relevant, k=3)
    assert round(ndcg, 4) == 1.0
