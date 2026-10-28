import React from 'react';
import {
  Search,
  GitCompare,
  BarChart3,
  BookOpen,
  History,
  Activity,
  Layers,
  ShieldCheck
} from 'lucide-react';

export function Navbar({ activeTab, setActiveTab, onOpenDisclaimer, healthData }) {
  const navItems = [
    { id: 'search', label: 'Search & Retrieve', icon: Search },
    { id: 'compare', label: 'Method Comparison', icon: GitCompare },
    { id: 'evaluation', label: 'IR Evaluation', icon: BarChart3 },
    { id: 'catalog', label: 'Document Catalog', icon: BookOpen },
    { id: 'history', label: 'Search History', icon: History },
    { id: 'architecture', label: 'Pipeline Architecture', icon: Layers },
  ];

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Identity */}
          <div
            onClick={() => setActiveTab('search')}
            className="flex items-center gap-3 cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-600 to-sky-600 flex items-center justify-center text-white shadow-md shadow-teal-500/20 group-hover:scale-105 transition-transform">
              <Activity className="w-6 h-6 stroke-[2.2]" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-xl tracking-tight text-slate-900 group-hover:text-teal-700 transition-colors">
                  MedQuery
                </span>
                <span className="px-2 py-0.5 text-[10px] font-semibold bg-teal-100 text-teal-800 rounded-full border border-teal-200">
                  IR Engine v1.0
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium hidden sm:block">
                Hybrid Document Retrieval & Semantic Ranking (BM25 + BERT)
              </p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                    isActive
                      ? 'bg-teal-50 text-teal-700 border border-teal-200 shadow-xs'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80 border border-transparent'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-teal-600' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Right Status / Actions */}
          <div className="flex items-center gap-2">
            <button
              onClick={onOpenDisclaimer}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-medium text-slate-700 hover:bg-slate-50 hover:border-slate-300 transition-colors cursor-pointer"
            >
              <ShieldCheck className="w-4 h-4 text-teal-600" />
              <span className="hidden sm:inline">IR Scope</span>
            </button>

            {healthData && (
              <div className="hidden lg:flex items-center gap-2 px-2.5 py-1 bg-slate-100 rounded-lg text-[11px] font-medium text-slate-600 border border-slate-200">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>{healthData.total_documents || 105} Docs</span>
                <span className="text-slate-300">•</span>
                <span>{healthData.total_chunks || 315} Passages</span>
              </div>
            )}
          </div>
        </div>

        {/* Mobile Navigation Scrollbar */}
        <div className="md:hidden flex overflow-x-auto py-2 space-x-2 border-t border-slate-100">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap cursor-pointer ${
                  isActive
                    ? 'bg-teal-600 text-white'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
}
