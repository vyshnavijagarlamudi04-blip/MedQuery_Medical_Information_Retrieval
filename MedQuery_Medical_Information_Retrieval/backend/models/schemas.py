"""
Pydantic Schemas for MedQuery API.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., description="Natural language medical query", min_length=1)
    method: str = Field("hybrid", description="Retrieval method: tfidf, bm25, semantic, hybrid")
    top_k: int = Field(5, description="Number of results to return", ge=1, le=50)
    bm25_weight: Optional[float] = Field(0.5, description="Weight for BM25 in hybrid search", ge=0.0, le=1.0)
    semantic_weight: Optional[float] = Field(0.5, description="Weight for Semantic in hybrid search", ge=0.0, le=1.0)
    category_filter: Optional[str] = Field(None, description="Optional medical category filter")


class SearchResultItem(BaseModel):
    rank: int
    document_id: str
    chunk_id: str
    title: str
    category: str
    disease: str
    section: Optional[str] = ""
    passage: str
    source: Optional[str] = ""
    score: float
    raw_score: Optional[float] = None
    bm25_score: Optional[float] = None
    norm_bm25: Optional[float] = None
    semantic_score: Optional[float] = None
    hybrid_score: Optional[float] = None
    method: str


class SearchResponse(BaseModel):
    query: str
    method: str
    total_results: int
    search_time_ms: float
    results: List[SearchResultItem]
    category_filter: Optional[str] = None
    bm25_weight: Optional[float] = None
    semantic_weight: Optional[float] = None


class CompareRequest(BaseModel):
    query: str = Field(..., description="Query to compare across all 4 retrieval methods", min_length=1)
    top_k: int = Field(5, description="Number of results per method", ge=1, le=20)
    category_filter: Optional[str] = Field(None)


class MethodComparisonResult(BaseModel):
    method: str
    search_time_ms: float
    results: List[SearchResultItem]


class CompareResponse(BaseModel):
    query: str
    methods: Dict[str, MethodComparisonResult]


class DocumentItem(BaseModel):
    document_id: str
    title: str
    category: str
    disease: str
    chunk_count: int
    source: str
    preview: str


class DocumentsListResponse(BaseModel):
    total_documents: int
    total_chunks: int
    documents: List[DocumentItem]


class CategoryCount(BaseModel):
    category: str
    count: int


class HistoryItem(BaseModel):
    id: str
    timestamp: str
    query: str
    method: str
    top_k: int
    search_time_ms: float
    top_title: Optional[str] = ""
    top_score: Optional[float] = 0.0


class EvaluationSummary(BaseModel):
    method: str
    num_queries: int
    map: float
    mrr: float
    precision_5: float = Field(alias="precision@5")
    recall_5: float = Field(alias="recall@5")
    f1_5: float = Field(alias="f1@5")
    precision_10: float = Field(alias="precision@10")
    recall_10: float = Field(alias="recall@10")
    f1_10: float = Field(alias="f1@10")
    ndcg_5: float = Field(alias="ndcg@5")


class EvaluationResponse(BaseModel):
    status: str
    last_evaluated_at: Optional[str] = None
    summary_table: List[Dict[str, Any]]
    chart_url: Optional[str] = None
    queries_evaluated: int
