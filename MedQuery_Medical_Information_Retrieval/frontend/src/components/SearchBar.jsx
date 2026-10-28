import React from 'react';
import {
  Search,
  Sliders,
  Sparkles,
  Layers,
  Cpu,
  Hash,
  Filter,
  X,
  Compass
} from 'lucide-react';

export const SAMPLE_QUERIES = [
  "What are common symptoms of diabetes?",
  "What causes hypertension?",
  "What are common asthma triggers?",
  "How can dengue be prevented?",
  "What are symptoms of anemia?",
  "What causes migraine?",
  "What are the symptoms of pneumonia?",
  "How is food poisoning prevented?"
];

export function SearchBar({
  query,
  setQuery,
  method,
  setMethod,
  topK,
  setTopK,
  bm25Weight,
  setBm25Weight,
  semanticWeight,
  setSemanticWeight,
  categoryFilter,
  setCategoryFilter,
  categories,
  onSearch,
  loading
}) {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  const handleSampleClick = (sample) => {
    setQuery(sample);
    onSearch(sample);
  };

  const handleWeightPreset = (bm, sem) => {
    setBm25Weight(bm);
    setSemanticWeight(sem);
  };

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-slate-200 mb-8">
      {/* Search Input Bar */}
      <form onSubmit={handleSubmit} className="mb-5">
        <div className="relative flex items-center">
          <div className="absolute left-4 text-slate-400 pointer-events-none">
            <Search className="w-5 h-5 text-teal-600" />
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search medical documents (e.g., 'What are common symptoms of diabetes?', 'Hypertension causes')..."
            className="w-full pl-12 pr-28 py-4 rounded-2xl bg-slate-50 border border-slate-200 text-slate-900 placeholder:text-slate-400 text-base focus:outline-none focus:ring-2 focus:ring-teal-500 focus:bg-white transition-all shadow-inner"
          />
          {query && (
            <button
              type="button"
              onClick={() => setQuery('')}
              className="absolute right-24 text-slate-400 hover:text-slate-600 p-1 cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          )}
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="absolute right-2.5 px-5 py-2.5 rounded-xl bg-gradient-to-r from-teal-600 to-sky-600 hover:from-teal-700 hover:to-sky-700 text-white font-semibold text-sm shadow-md shadow-teal-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      {/* Control Bar: Methods, Top-K, Category Filter */}
      <div className="flex items-center justify-between flex-wrap gap-4 pt-2 pb-4 border-b border-slate-100 text-xs">
        {/* Method Selector */}
        <div className="flex items-center gap-1.5 flex-wrap">
          <span className="font-bold text-slate-500 uppercase tracking-wider mr-1 flex items-center gap-1">
            <Cpu className="w-3.5 h-3.5 text-teal-600" /> Method:
          </span>

          <button
            type="button"
            onClick={() => setMethod('hybrid')}
            className={`px-3 py-1.5 rounded-lg font-semibold transition-all cursor-pointer ${
              method === 'hybrid'
                ? 'bg-teal-600 text-white shadow-xs'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            Hybrid (BM25 + SBERT) ⭐
          </button>

          <button
            type="button"
            onClick={() => setMethod('bm25')}
            className={`px-3 py-1.5 rounded-lg font-semibold transition-all cursor-pointer ${
              method === 'bm25'
                ? 'bg-sky-600 text-white shadow-xs'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            BM25 Okapi
          </button>

          <button
            type="button"
            onClick={() => setMethod('semantic')}
            className={`px-3 py-1.5 rounded-lg font-semibold transition-all cursor-pointer ${
              method === 'semantic'
                ? 'bg-indigo-600 text-white shadow-xs'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            SBERT Semantic
          </button>

          <button
            type="button"
            onClick={() => setMethod('tfidf')}
            className={`px-3 py-1.5 rounded-lg font-semibold transition-all cursor-pointer ${
              method === 'tfidf'
                ? 'bg-slate-700 text-white shadow-xs'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            TF-IDF Baseline
          </button>
        </div>

        {/* Top-K and Category Dropdowns */}
        <div className="flex items-center gap-3">
          {/* Top-K */}
          <div className="flex items-center gap-1.5">
            <Hash className="w-3.5 h-3.5 text-slate-400" />
            <span className="font-semibold text-slate-600">Top-K:</span>
            <select
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              className="bg-slate-100 border border-slate-200 rounded-lg px-2.5 py-1 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-1 focus:ring-teal-500"
            >
              <option value={5}>Top 5</option>
              <option value={10}>Top 10</option>
              <option value={20}>Top 20</option>
            </select>
          </div>

          {/* Category Filter */}
          <div className="flex items-center gap-1.5">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <span className="font-semibold text-slate-600">Category:</span>
            <select
              value={categoryFilter || 'All'}
              onChange={(e) => setCategoryFilter(e.target.value === 'All' ? null : e.target.value)}
              className="bg-slate-100 border border-slate-200 rounded-lg px-2.5 py-1 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-1 focus:ring-teal-500 max-w-[140px] truncate"
            >
              <option value="All">All Categories</option>
              {categories.map((c) => (
                <option key={c.category} value={c.category}>
                  {c.category} ({c.count})
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Hybrid Weight Configuration Panel (Visible only when Hybrid is selected) */}
      {method === 'hybrid' && (
        <div className="mt-4 p-4 bg-teal-50/60 rounded-2xl border border-teal-100 text-xs">
          <div className="flex items-center justify-between mb-2">
            <span className="font-bold text-teal-900 flex items-center gap-1.5">
              <Sliders className="w-4 h-4 text-teal-600" />
              Hybrid Fusion Weights (Linear Re-ranking Formula):
            </span>
            <span className="font-mono font-bold text-teal-800">
              {bm25Weight.toFixed(2)} × BM25 + {semanticWeight.toFixed(2)} × SBERT
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-center">
            <div className="flex items-center gap-3">
              <span className="font-medium text-slate-600 text-[11px] w-20">BM25 Weight:</span>
              <input
                type="range"
                min="0.0"
                max="1.0"
                step="0.05"
                value={bm25Weight}
                onChange={(e) => {
                  const val = parseFloat(e.target.value);
                  setBm25Weight(val);
                  setSemanticWeight(parseFloat((1.0 - val).toFixed(2)));
                }}
                className="w-full accent-teal-600"
              />
              <span className="font-mono text-teal-800 font-semibold w-10 text-right">{bm25Weight.toFixed(2)}</span>
            </div>

            {/* Quick Presets */}
            <div className="flex items-center gap-2 justify-start md:justify-end">
              <span className="text-[11px] text-slate-500 font-medium">Presets:</span>
              <button
                type="button"
                onClick={() => handleWeightPreset(0.5, 0.5)}
                className={`px-2.5 py-1 rounded text-[11px] font-semibold border cursor-pointer transition-colors ${
                  bm25Weight === 0.5 ? 'bg-teal-600 text-white border-teal-600' : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
                }`}
              >
                Balanced 50/50
              </button>
              <button
                type="button"
                onClick={() => handleWeightPreset(0.7, 0.3)}
                className={`px-2.5 py-1 rounded text-[11px] font-semibold border cursor-pointer transition-colors ${
                  bm25Weight === 0.7 ? 'bg-teal-600 text-white border-teal-600' : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
                }`}
              >
                Keyword 70/30
              </button>
              <button
                type="button"
                onClick={() => handleWeightPreset(0.3, 0.7)}
                className={`px-2.5 py-1 rounded text-[11px] font-semibold border cursor-pointer transition-colors ${
                  bm25Weight === 0.3 ? 'bg-teal-600 text-white border-teal-600' : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
                }`}
              >
                Semantic 30/70
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Sample Demo Queries */}
      <div className="mt-4 pt-3">
        <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-500 mb-2">
          <Compass className="w-3.5 h-3.5 text-teal-600" />
          <span>Predefined Demo Queries (Click to test):</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {SAMPLE_QUERIES.map((sample, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSampleClick(sample)}
              className="px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-teal-50 hover:text-teal-700 hover:border-teal-200 text-slate-600 text-xs font-medium border border-slate-200 transition-all cursor-pointer text-left"
            >
              "{sample}"
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
