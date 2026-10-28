/**
 * MedQuery API Service
 * Handles communication with the FastAPI backend.
 */

const API_BASE = import.meta.env.VITE_API_URL || '/api';

export async function search(params) {
  const { query, method = 'hybrid', topK = 5, bm25Weight = 0.5, semanticWeight = 0.5, categoryFilter = null } = params;
  const res = await fetch(`${API_BASE}/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query,
      method,
      top_k: parseInt(topK, 10),
      bm25_weight: parseFloat(bm25Weight),
      semantic_weight: parseFloat(semanticWeight),
      category_filter: categoryFilter === 'All' ? null : categoryFilter,
    }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Search failed with status ${res.status}`);
  }
  return res.json();
}

export async function compareMethods(query, topK = 5, categoryFilter = null) {
  const res = await fetch(`${API_BASE}/compare`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query,
      top_k: parseInt(topK, 10),
      category_filter: categoryFilter === 'All' ? null : categoryFilter,
    }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Comparison failed with status ${res.status}`);
  }
  return res.json();
}

export async function getDocuments() {
  const res = await fetch(`${API_BASE}/documents`);
  if (!res.ok) throw new Error('Failed to load documents catalog');
  return res.json();
}

export async function getCategories() {
  const res = await fetch(`${API_BASE}/categories`);
  if (!res.ok) throw new Error('Failed to load categories');
  return res.json();
}

export async function getSearchHistory() {
  const res = await fetch(`${API_BASE}/search/history`);
  if (!res.ok) throw new Error('Failed to load search history');
  return res.json();
}

export async function getEvaluation() {
  const res = await fetch(`${API_BASE}/evaluation`);
  if (!res.ok) throw new Error('Failed to load evaluation metrics');
  return res.json();
}

export async function runEvaluation() {
  const res = await fetch(`${API_BASE}/evaluation/run`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to run benchmark evaluation');
  return res.json();
}

export async function uploadDocument(formData) {
  const res = await fetch(`${API_BASE}/documents/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Upload failed with status ${res.status}`);
  }
  return res.json();
}

export async function getHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Backend offline');
  return res.json();
}
