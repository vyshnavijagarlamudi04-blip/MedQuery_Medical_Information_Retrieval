"""
FastAPI Routes for MedQuery.
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from backend.models.schemas import (
    SearchRequest,
    SearchResponse,
    CompareRequest,
    CompareResponse,
    DocumentsListResponse,
    CategoryCount,
    HistoryItem,
    EvaluationResponse
)
from backend.services.search_service import SearchService

router = APIRouter()

# Dependency injection for SearchService singleton
_search_service: Optional[SearchService] = None

def get_search_service() -> SearchService:
    global _search_service
    if _search_service is None:
        _search_service = SearchService()
        _search_service.initialize()
    return _search_service


@router.get("/")
def root():
    return {
        "project": "MedQuery – Medical Information Retrieval System",
        "subtitle": "Hybrid Medical Document Retrieval and Semantic Ranking using BM25 and BERT",
        "version": "1.0.0",
        "disclaimer": "MedQuery is an educational information retrieval system. It retrieves information from its document collection and does not provide medical diagnosis or replace professional medical advice.",
        "documentation": "/docs",
        "status": "operational"
    }


@router.get("/health")
def health(service: SearchService = Depends(get_search_service)):
    catalog = service.get_documents_catalog()
    return {
        "status": "healthy",
        "total_documents": catalog["total_documents"],
        "total_chunks": catalog["total_chunks"],
        "retrieval_engines": list(service.retrievers.keys()),
        "sbert_model": service.indexer.sbert_model_name
    }


@router.post("/search", response_model=SearchResponse)
def search(request: SearchRequest, service: SearchService = Depends(get_search_service)):
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Search query must not be empty.")

    res = service.search(
        query=request.query,
        method=request.method,
        top_k=request.top_k,
        bm25_weight=request.bm25_weight or 0.5,
        semantic_weight=request.semantic_weight or 0.5,
        category_filter=request.category_filter
    )
    return res


@router.post("/compare", response_model=CompareResponse)
def compare_retrieval_methods(
    request: CompareRequest,
    service: SearchService = Depends(get_search_service)
):
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Comparison query must not be empty.")

    res = service.compare_methods(
        query=request.query,
        top_k=request.top_k,
        category_filter=request.category_filter
    )
    return res


@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form("General"),
    title: Optional[str] = Form(None),
    disease: Optional[str] = Form(None),
    service: SearchService = Depends(get_search_service)
):
    # Security: check file extension
    valid_exts = [".txt", ".pdf", ".csv"]
    filename = file.filename or "uploaded_doc"
    if not any(filename.lower().endswith(ext) for ext in valid_exts):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed formats: {', '.join(valid_exts)}"
        )

    # Security: size limit 15MB
    content_bytes = await file.read()
    if len(content_bytes) > 15 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 15MB.")

    if len(content_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        result = service.upload_document(
            file_bytes=content_bytes,
            filename=filename,
            category=category,
            title=title,
            disease=disease
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")


@router.get("/documents", response_model=DocumentsListResponse)
def get_documents(service: SearchService = Depends(get_search_service)):
    return service.get_documents_catalog()


@router.get("/categories", response_model=List[CategoryCount])
def get_categories(service: SearchService = Depends(get_search_service)):
    return service.get_categories()


@router.get("/search/history", response_model=List[HistoryItem])
def get_search_history(service: SearchService = Depends(get_search_service)):
    return service.get_search_history()


@router.get("/evaluation", response_model=EvaluationResponse)
def get_evaluation(service: SearchService = Depends(get_search_service)):
    return service.get_evaluation_data()


@router.post("/evaluation/run", response_model=EvaluationResponse)
def run_evaluation(service: SearchService = Depends(get_search_service)):
    return service.run_evaluation()
