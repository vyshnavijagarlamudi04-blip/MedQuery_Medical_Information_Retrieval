import React, { useState } from 'react';
import {
  ChevronDown,
  ChevronUp,
  ExternalLink,
  BookOpen,
  Tag,
  Zap,
  Cpu,
  Layers,
  FileText
} from 'lucide-react';

/**
 * Highlights terms matching the query inside the text.
 */
function HighlightedText({ text, query }) {
  if (!query || !text) return <span>{text}</span>;

  // Split query into significant words (>2 chars, skip standard small stopwords)
  const stopWords = new Set(['the', 'and', 'what', 'are', 'is', 'for', 'with', 'from', 'how', 'can', 'does', 'in', 'of', 'to']);
  const terms = query
    .toLowerCase()
    .split(/\s+/)
    .map(w => w.replace(/[^\w]/g, ''))
    .filter(w => w.length > 2 && !stopWords.has(w));

  if (terms.length === 0) return <span>{text}</span>;

  const pattern = new RegExp(`(${terms.join('|')})`, 'gi');
  const parts = text.split(pattern);

  return (
    <span>
      {parts.map((part, i) => {
        const isMatch = terms.some(t => t.toLowerCase() === part.toLowerCase());
        return isMatch ? (
          <mark key={i} className="match-highlight">
            {part}
          </mark>
        ) : (
          part
        );
      })}
    </span>
  );
}

export function SearchResultCard({ result, query, searchMethod }) {
  const [expanded, setExpanded] = useState(false);

  const {
    rank,
    title,
    category,
    disease,
    section,
    passage,
    source,
    score,
    bm25_score,
    norm_bm25,
    semantic_score,
    hybrid_score,
    method
  } = result;

  // Compute a color gradient class for the score badge
  const getScoreBadgeClass = (s) => {
    if (s >= 0.75) return 'bg-emerald-50 text-emerald-700 border-emerald-200';
    if (s >= 0.50) return 'bg-teal-50 text-teal-700 border-teal-200';
    if (s >= 0.30) return 'bg-sky-50 text-sky-700 border-sky-200';
    return 'bg-slate-50 text-slate-700 border-slate-200';
  };

  return (
    <article className="med-card p-5 hover:border-teal-300 transition-all">
      {/* Top Header Row */}
      <div className="flex items-start justify-between gap-4 mb-2.5">
        <div className="flex items-center gap-2.5 flex-wrap">
          {/* Rank Badge */}
          <span className="flex items-center justify-center w-7 h-7 rounded-lg bg-slate-900 text-white font-bold text-xs shadow-xs">
            #{rank}
          </span>

          {/* Category Pill */}
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-semibold badge-teal">
            <Tag className="w-3 h-3" />
            {category || 'General'}
          </span>

          {/* Disease Name */}
          {disease && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-semibold badge-blue">
              <FileText className="w-3 h-3" />
              {disease}
            </span>
          )}

          {/* Passage Section Label */}
          {section && (
            <span className="text-[11px] font-medium text-slate-500 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
              {section}
            </span>
          )}
        </div>

        {/* Primary Relevance Score Badge */}
        <div className="flex items-center gap-1.5 shrink-0">
          <div className={`px-3 py-1 rounded-lg border text-xs font-bold flex items-center gap-1 ${getScoreBadgeClass(score)}`}>
            <Zap className="w-3.5 h-3.5" />
            <span>Score: {(score || 0).toFixed(4)}</span>
          </div>
        </div>
      </div>

      {/* Document Title */}
      <h3 className="text-base font-bold text-slate-900 mb-2 leading-snug">
        <HighlightedText text={title} query={query} />
      </h3>

      {/* Passage Snippet */}
      <div className="text-sm text-slate-600 leading-relaxed bg-slate-50/70 p-3.5 rounded-xl border border-slate-100 mb-3">
        <HighlightedText
          text={expanded ? passage : passage.length > 260 ? `${passage.slice(0, 260)}...` : passage}
          query={query}
        />
      </div>

      {/* Score Breakdown & Metadata Footer */}
      <div className="flex items-center justify-between flex-wrap gap-2 text-xs pt-2 border-t border-slate-100">
        <div className="flex items-center gap-2 flex-wrap text-[11px]">
          {/* Method badge */}
          <span className="font-semibold text-slate-500 uppercase tracking-wider">
            {method || searchMethod}:
          </span>

          {/* Detailed Scores for Hybrid */}
          {method === 'hybrid' && (
            <>
              <span className="px-2 py-0.5 rounded bg-sky-50 text-sky-700 border border-sky-200 font-mono">
                BM25: {bm25_score != null ? bm25_score.toFixed(2) : '-'} (norm: {norm_bm25 != null ? norm_bm25.toFixed(2) : '-'})
              </span>
              <span className="px-2 py-0.5 rounded bg-teal-50 text-teal-700 border border-teal-200 font-mono">
                SBERT Cosine: {semantic_score != null ? semantic_score.toFixed(3) : '-'}
              </span>
              <span className="px-2 py-0.5 rounded bg-indigo-50 text-indigo-700 border border-indigo-200 font-mono font-bold">
                Hybrid Re-Rank: {hybrid_score != null ? hybrid_score.toFixed(3) : score.toFixed(3)}
              </span>
            </>
          )}

          {method === 'bm25' && (
            <span className="px-2 py-0.5 rounded bg-sky-50 text-sky-700 border border-sky-200 font-mono">
              Raw BM25: {bm25_score != null ? bm25_score.toFixed(2) : score.toFixed(2)}
            </span>
          )}

          {method === 'semantic' && (
            <span className="px-2 py-0.5 rounded bg-teal-50 text-teal-700 border border-teal-200 font-mono">
              Dense Cosine Similarity: {semantic_score != null ? semantic_score.toFixed(4) : score.toFixed(4)}
            </span>
          )}

          {method === 'tfidf' && (
            <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200 font-mono">
              TF-IDF Cosine: {score.toFixed(4)}
            </span>
          )}

          {/* Source Citation */}
          {source && (
            <span className="text-slate-400 flex items-center gap-1 ml-1">
              • Source: {source}
            </span>
          )}
        </div>

        {/* Read More / Collapse Toggle */}
        {passage.length > 260 && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="flex items-center gap-1 text-teal-600 hover:text-teal-800 font-semibold cursor-pointer text-xs"
          >
            {expanded ? (
              <>
                <span>Show Less</span>
                <ChevronUp className="w-3.5 h-3.5" />
              </>
            ) : (
              <>
                <span>Read Full Passage</span>
                <ChevronDown className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        )}
      </div>
    </article>
  );
}
