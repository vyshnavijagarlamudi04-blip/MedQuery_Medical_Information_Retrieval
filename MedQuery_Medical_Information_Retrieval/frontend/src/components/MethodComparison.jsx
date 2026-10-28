import React, { useState } from 'react';
import {
  GitCompare,
  Zap,
  Search,
  CheckCircle,
  HelpCircle,
  Tag,
  ArrowRight
} from 'lucide-react';
import { compareMethods } from '../services/api';
import { SAMPLE_QUERIES } from './SearchBar';

export function MethodComparison() {
  const [query, setQuery] = useState('What causes high blood pressure and hypertension?');
  const [topK, setTopK] = useState(5);
  const [loading, setLoading] = useState(false);
  const [comparisonData, setComparisonData] = useState(null);
  const [error, setError] = useState(null);

  const handleRunComparison = async (searchQ) => {
    const qToRun = searchQ || query;
    if (!qToRun.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const data = await compareMethods(qToRun.trim(), topK);
      setComparisonData(data);
    } catch (err) {
      setError(err.message || 'Failed to compare retrieval methods');
    } finally {
      setLoading(false);
    }
  };

  const methodsList = [
    { key: 'hybrid', label: 'Hybrid (BM25 + SBERT)', badge: 'Recommended', color: 'border-teal-500 bg-teal-50/30' },
    { key: 'bm25', label: 'BM25 Okapi', badge: 'Probabilistic Lexical', color: 'border-sky-500 bg-sky-50/30' },
    { key: 'semantic', label: 'SBERT Semantic', badge: 'Dense Embeddings', color: 'border-indigo-500 bg-indigo-50/30' },
    { key: 'tfidf', label: 'TF-IDF Baseline', badge: 'Vector Space Model', color: 'border-slate-400 bg-slate-50/30' },
  ];

  return (
    <div className="space-y-6">
      {/* Header & Query Box */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-slate-200">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center border border-teal-200">
            <GitCompare className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900">Multi-Method Retrieval Comparison</h2>
            <p className="text-xs text-slate-500">
              Run TF-IDF, BM25, Semantic BERT, and Hybrid simultaneous searches on the same query to inspect ranking variance.
            </p>
          </div>
        </div>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleRunComparison();
          }}
          className="mt-4 flex gap-3 flex-col sm:flex-row"
        >
          <div className="relative flex-1">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter comparison query..."
              className="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:bg-white"
            />
          </div>

          <div className="flex items-center gap-2">
            <select
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              className="px-3 py-3 rounded-xl bg-slate-50 border border-slate-200 text-xs font-semibold text-slate-700"
            >
              <option value={3}>Top 3</option>
              <option value={5}>Top 5</option>
              <option value={10}>Top 10</option>
            </select>

            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="px-6 py-3 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-semibold text-xs transition-colors cursor-pointer shadow-sm disabled:opacity-50"
            >
              {loading ? 'Evaluating...' : 'Compare All 4'}
            </button>
          </div>
        </form>

        {/* Quick Sample Queries */}
        <div className="mt-4 pt-3 border-t border-slate-100 flex items-center gap-2 flex-wrap text-xs">
          <span className="text-slate-400 font-medium">Try:</span>
          {SAMPLE_QUERIES.slice(0, 4).map((s, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => {
                setQuery(s);
                handleRunComparison(s);
              }}
              className="text-slate-600 hover:text-teal-700 hover:underline cursor-pointer"
            >
              "{s}"
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-2xl text-red-700 text-xs">
          {error}
        </div>
      )}

      {/* Comparison Grid (Side by side 4 columns) */}
      {comparisonData && (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 animate-in fade-in duration-200">
          {methodsList.map((m) => {
            const data = comparisonData.methods[m.key];
            const results = data ? data.results : [];
            const latency = data ? data.search_time_ms : 0;

            return (
              <div
                key={m.key}
                className={`bg-white rounded-2xl border-t-4 ${m.color} border-x border-b border-slate-200 p-4 flex flex-col shadow-xs`}
              >
                {/* Column Header */}
                <div className="pb-3 mb-3 border-b border-slate-100">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-sm text-slate-900">{m.label}</span>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
                      {m.badge}
                    </span>
                  </div>
                  <div className="flex items-center gap-1 text-[11px] text-teal-700 font-medium">
                    <Zap className="w-3 h-3 text-amber-500" />
                    <span>Latency: {latency} ms</span>
                  </div>
                </div>

                {/* Ranked List */}
                <div className="space-y-3 flex-1">
                  {results.length === 0 ? (
                    <div className="text-xs text-slate-400 py-6 text-center">No documents retrieved.</div>
                  ) : (
                    results.map((r, i) => (
                      <div
                        key={i}
                        className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 hover:bg-white hover:border-slate-300 transition-colors text-xs space-y-1.5"
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-bold text-slate-900">Rank #{r.rank}</span>
                          <span className="font-mono text-[10px] font-bold px-1.5 py-0.5 rounded bg-white border border-slate-200 text-teal-700">
                            Score: {(r.score || 0).toFixed(3)}
                          </span>
                        </div>
                        <h4 className="font-semibold text-slate-800 leading-snug line-clamp-2">
                          {r.title}
                        </h4>
                        <p className="text-slate-500 text-[11px] line-clamp-2 leading-relaxed">
                          {r.passage}
                        </p>
                      </div>
                    ))
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
