"""
Integration and API endpoint tests using FastAPI TestClient.
"""

import io
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "MedQuery" in data["project"]
    assert "disclaimer" in data


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["total_documents"] >= 100


def test_search_api_hybrid():
    payload = {
        "query": "What are common symptoms of diabetes?",
        "method": "hybrid",
        "top_k": 5
    }
    response = client.post("/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == payload["query"]
    assert len(data["results"]) == 5
    assert data["search_time_ms"] > 0
    assert any("diabetes" in r["title"].lower() for r in data["results"])


def test_search_api_empty_query_error():
    payload = {
        "query": "",
        "method": "hybrid"
    }
    response = client.post("/search", json=payload)
    assert response.status_code == 422 or response.status_code == 400


def test_compare_api():
    payload = {
        "query": "What causes asthma?",
        "top_k": 3
    }
    response = client.post("/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "methods" in data
    assert "bm25" in data["methods"]
    assert "semantic" in data["methods"]
    assert "tfidf" in data["methods"]
    assert "hybrid" in data["methods"]


def test_get_documents():
    response = client.get("/documents")
    assert response.status_code == 200
    data = response.json()
    assert data["total_documents"] >= 100
    assert len(data["documents"]) >= 100


def test_get_categories():
    response = client.get("/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_search_history():
    response = client.get("/search/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_evaluation():
    response = client.get("/evaluation")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "available"
    assert len(data["summary_table"]) >= 4


def test_upload_txt_document():
    txt_content = b"Title: Test Migraine Ingestion\nCategory: Neurology\nMigraine is a severe neurovascular headache."
    files = {"file": ("test_doc.txt", io.BytesIO(txt_content), "text/plain")}
    data = {"category": "Neurology", "title": "Test Migraine Ingestion"}

    response = client.post("/documents/upload", files=files, data=data)
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data["status"] == "success"
    assert resp_data["chunks_created"] >= 1


def test_upload_invalid_file_extension():
    fake_exe = b"MZ90000BinaryContent"
    files = {"file": ("malicious.exe", io.BytesIO(fake_exe), "application/octet-stream")}
    response = client.post("/documents/upload", files=files)
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]


def test_upload_empty_file():
    empty = b""
    files = {"file": ("empty.txt", io.BytesIO(empty), "text/plain")}
    response = client.post("/documents/upload", files=files)
    assert response.status_code == 400
