import React, { useState, useEffect } from 'react';
import {
  Navbar
} from './components/Navbar';
import {
  DisclaimerBanner,
  DisclaimerModal
} from './components/DisclaimerModal';
import {
  SearchBar
} from './components/SearchBar';
import {
  SearchResultCard
} from './components/SearchResultCard';
import {
  MethodComparison
} from './components/MethodComparison';
import {
  EvaluationDashboard
} from './components/EvaluationDashboard';
import {
  DocumentManager
} from './components/DocumentManager';
import {
  SearchHistory
} from './components/SearchHistory';
import {
  SystemArchitecture
} from './components/SystemArchitecture';
import {
  search,
  getCategories,
  getHealth
} from './services/api';
import {
  Zap,
  CheckCircle,
  FileQuestion,
  Sparkles,
  Info,
  Clock,
  Layers,
  Activity
} from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('search');
  const [isDisclaimerOpen, setIsDisclaimerOpen] = useState(false);

  // Search parameters
  const [query, setQuery] = useState('');
  const [method, setMethod] = useState('hybrid');
  const [topK, setTopK] = useState(5);
  const [bm25Weight, setBm25Weight] = useState(0.5);
  const [semanticWeight, setSemanticWeight] = useState(0.5);
  const [categoryFilter, setCategoryFilter] = useState('All');

  // Search states
  const [searchResults, setSearchResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Catalog & System data
  const [categories, setCategories] = useState([]);
  const [healthData, setHealthData] = useState(null);

  useEffect(() => {
    // Initial load
    getCategories()
      .then(setCategories)
      .catch((err) => console.log('Backend not yet ready for categories:', err));
    getHealth()
      .then(setHealthData)
      .catch((err) => console.log('Backend not yet ready for health:', err));
  }, []);

  const handlePerformSearch = async (queryText) => {
    const q = queryText || query;
    if (!q || !q.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const data = await search({
        query: q.trim(),
        method,
        topK,
        bm25Weight,
        semanticWeight,
        categoryFilter: categoryFilter === 'All' ? null : categoryFilter,
      });
      setSearchResults(data);
      // Ensure we are in search tab
      setActiveTab('search');
    } catch (err) {
      setError(err.message || 'Search execution failed');
      setSearchResults(null);
    } finally {
      setLoading(false);
    }
  };

  const handleReRunFromHistory = (qText, methodUsed) => {
    setQuery(qText);
    if (methodUsed) setMethod(methodUsed);
    setActiveTab('search');
    handlePerformSearch(qText);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 font-sans selection:bg-teal-100 selection:text-teal-900">
      {/* Top Disclaimer Notice Banner */}
      <DisclaimerBanner onOpenModal={() => setIsDisclaimerOpen(true)} />

      {/* Main Top Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenDisclaimer={() => setIsDisclaimerOpen(true)}
        healthData={healthData}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'search' && (
          <div className="space-y-6">
            {/* Search Controls & Presets */}
            <SearchBar
              query={query}
              setQuery={setQuery}
              method={method}
              setMethod={setMethod}
              topK={topK}
              setTopK={setTopK}
              bm25Weight={bm25Weight}
              setBm25Weight={setBm25Weight}
              semanticWeight={semanticWeight}
              setSemanticWeight={setSemanticWeight}
              categoryFilter={categoryFilter}
              setCategoryFilter={setCategoryFilter}
              categories={categories}
              onSearch={handlePerformSearch}
              loading={loading}
            />

            {/* Error Message */}
            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-2xl text-red-700 text-xs">
                {error}
              </div>
            )}

            {/* Loading Indicator */}
            {loading && (
              <div className="py-16 text-center space-y-3">
                <div className="w-10 h-10 border-3 border-teal-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
                <p className="text-xs font-semibold text-slate-500">
                  Retrieving passages via {method.toUpperCase()} and computing relevance...
                </p>
              </div>
            )}

            {/* Search Results Display */}
            {!loading && searchResults && (
              <div className="space-y-4 animate-in fade-in duration-150">
                {/* Latency & Summary Header */}
                <div className="flex items-center justify-between flex-wrap gap-2 px-1 text-xs">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-slate-900 text-sm">
                      Search Results for: <span className="text-teal-700">"{searchResults.query}"</span>
                    </span>
                    <span className="text-slate-400">
                      ({searchResults.total_results} passages retrieved)
                    </span>
                  </div>

                  <div className="flex items-center gap-3">
                    <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-100 text-teal-800 border border-teal-200 font-mono font-bold text-xs shadow-xs">
                      <Zap className="w-3.5 h-3.5 text-teal-600 fill-teal-600" />
                      <span>Search time: {searchResults.search_time_ms} ms</span>
                    </div>

                    <span className="px-2.5 py-1 rounded-full bg-slate-200 text-slate-700 font-semibold uppercase text-[10px]">
                      Method: {searchResults.method}
                    </span>
                  </div>
                </div>

                {/* Empty State */}
                {searchResults.results.length === 0 ? (
                  <div className="bg-white rounded-3xl p-12 text-center border border-slate-200 space-y-2">
                    <FileQuestion className="w-10 h-10 text-slate-300 mx-auto" />
                    <h3 className="font-bold text-slate-800 text-sm">No matching medical documents found</h3>
                    <p className="text-xs text-slate-500 max-w-sm mx-auto">
                      Try broadening your query, selecting "All Categories", or switching to Hybrid or Semantic retrieval.
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {searchResults.results.map((item, idx) => (
                      <SearchResultCard
                        key={`${item.chunk_id}_${idx}`}
                        result={item}
                        query={searchResults.query}
                        searchMethod={searchResults.method}
                      />
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Initial Hero / Welcome State (when no search executed yet) */}
            {!loading && !searchResults && (
              <div className="bg-white rounded-3xl p-8 sm:p-12 border border-slate-200 text-center shadow-xs space-y-6">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-teal-500 to-sky-500 text-white flex items-center justify-center mx-auto shadow-lg shadow-teal-500/20">
                  <Activity className="w-8 h-8 stroke-[2.2]" />
                </div>
                <div className="max-w-xl mx-auto space-y-2">
                  <h2 className="text-2xl font-bold text-slate-900">
                    Medical Information Retrieval Engine
                  </h2>
                  <p className="text-xs sm:text-sm text-slate-500 leading-relaxed">
                    Search over 105 educational medical conditions using natural language. MedQuery combines BM25 lexical token matching with Sentence-BERT dense semantic similarity to surface the most relevant clinical passages.
                  </p>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-3xl mx-auto text-left text-xs pt-4">
                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-1">
                    <h4 className="font-bold text-slate-800">1. Probabilistic Lexical</h4>
                    <p className="text-slate-500 text-[11px]">
                      BM25 Okapi indexes term frequency and inverse document frequency across structured medical passages.
                    </p>
                  </div>
                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-1">
                    <h4 className="font-bold text-slate-800">2. Dense SBERT Semantic</h4>
                    <p className="text-slate-500 text-[11px]">
                      all-MiniLM-L6-v2 encodes semantic concepts into 384-D vector space, overcoming vocabulary mismatch.
                    </p>
                  </div>
                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-1">
                    <h4 className="font-bold text-slate-800">3. Hybrid Re-Ranking</h4>
                    <p className="text-slate-500 text-[11px]">
                      Interpolates normalized BM25 with SBERT cosine similarity, re-ranking candidate pools for optimal precision.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab: Method Comparison */}
        {activeTab === 'compare' && <MethodComparison />}

        {/* Tab: Evaluation Dashboard */}
        {activeTab === 'evaluation' && <EvaluationDashboard />}

        {/* Tab: Document Catalog */}
        {activeTab === 'catalog' && <DocumentManager />}

        {/* Tab: Search History */}
        {activeTab === 'history' && (
          <SearchHistory onSelectQuery={handleReRunFromHistory} />
        )}

        {/* Tab: Architecture */}
        {activeTab === 'architecture' && <SystemArchitecture />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 space-y-1">
          <p className="font-semibold text-slate-700">
            MedQuery – Medical Information Retrieval System
          </p>
          <p className="text-[11px] text-slate-400">
            B.Tech Information Retrieval Mini Project • Powered by BM25, Sentence-BERT, FastAPI & React
          </p>
          <p className="text-[10px] text-amber-700 font-medium pt-1">
            Notice: Educational Information Retrieval Research Prototype. Not intended for clinical diagnostic use.
          </p>
        </div>
      </footer>

      {/* Medical Safety Disclaimer Modal */}
      <DisclaimerModal
        isOpen={isDisclaimerOpen}
        onClose={() => setIsDisclaimerOpen(false)}
      />
    </div>
  );
}
