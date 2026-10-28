import React from 'react';
import {
  Layers,
  Database,
  Cpu,
  Search,
  Zap,
  BarChart3,
  Sliders,
  CheckCircle2,
  ArrowDown
} from 'lucide-react';

export function SystemArchitecture() {
  const pipelineSteps = [
    {
      title: "1. Medical Dataset Collection",
      desc: "Curated collection of 105 structured medical documents across 12 specialties with verified sources (WHO, CDC, NIH, NHS).",
      icon: Database,
      tag: "105 Documents"
    },
    {
      title: "2. Text Cleaning & Tokenization",
      desc: "Whitespace normalization, unicode cleaning, and safe medical tokenization preserving critical acronyms (e.g. Type-2, COVID-19, B12).",
      icon: Cpu,
      tag: "TextCleaner"
    },
    {
      title: "3. Semantic Document Chunking",
      desc: "Structured splitting into 3 distinct passages per document: Overview & Pathophysiology, Symptoms & Causes, and Treatment & Prevention.",
      icon: Layers,
      tag: "315 Chunks"
    },
    {
      title: "4. Dual-Index Construction",
      desc: "Building BM25 Okapi inverted index, TF-IDF vector space sparse matrix (22,400 vocab), and generating 384-dimensional dense SBERT embeddings.",
      icon: Sliders,
      tag: "BM25 + all-MiniLM-L6-v2"
    },
    {
      title: "5. Multi-Stage Hybrid Retrieval & Fusion",
      desc: "Query-time dual retrieval generating top candidates. Min-max normalization maps BM25 to [0,1], fused linearly with SBERT cosine similarity.",
      icon: Search,
      tag: "w_bm25 * NormBM25 + w_sem * Cosine"
    },
    {
      title: "6. Candidate Re-ranking & Top-K Extraction",
      desc: "Re-ranks candidate pool by final hybrid score, extracts passage snippets, highlights matching terms, and measures sub-second latency.",
      icon: Zap,
      tag: "Re-ranking Engine"
    },
    {
      title: "7. Standard IR Metric Evaluation",
      desc: "Evaluation against 35 ground-truth queries measuring Precision@K, Recall@K, F1@K, Mean Average Precision (MAP), MRR, and NDCG@K.",
      icon: BarChart3,
      tag: "TREC / Manning IR Standard"
    }
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-slate-200">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center border border-teal-200">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900">System Architecture & IR Pipeline</h2>
            <p className="text-xs text-slate-500">
              End-to-End Hybrid Medical Document Retrieval and Semantic Ranking Pipeline
            </p>
          </div>
        </div>

        {/* Pipeline Diagram Cards */}
        <div className="mt-8 space-y-4 max-w-3xl mx-auto">
          {pipelineSteps.map((step, idx) => {
            const Icon = step.icon;
            return (
              <div key={idx} className="flex flex-col items-center">
                <div className="w-full bg-slate-50 border border-slate-200 rounded-2xl p-5 hover:border-teal-300 transition-colors">
                  <div className="flex items-start gap-4">
                    <div className="w-10 h-10 rounded-xl bg-teal-100/70 text-teal-700 flex items-center justify-center shrink-0 font-bold text-sm">
                      <Icon className="w-5 h-5" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between gap-2 flex-wrap mb-1">
                        <h3 className="font-bold text-slate-900 text-sm">{step.title}</h3>
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-white text-teal-800 border border-slate-200">
                          {step.tag}
                        </span>
                      </div>
                      <p className="text-slate-600 text-xs leading-relaxed">{step.desc}</p>
                    </div>
                  </div>
                </div>

                {idx < pipelineSteps.length - 1 && (
                  <div className="my-1.5 text-teal-500 flex items-center justify-center">
                    <ArrowDown className="w-4 h-4 stroke-[2.5]" />
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Mathematical Formulations Card */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-slate-200">
        <h3 className="text-base font-bold text-slate-900 mb-4">Core Mathematical Formulations</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-2">
            <h4 className="font-bold text-slate-800 text-xs">1. BM25 Okapi Lexical Score:</h4>
            <div className="p-2 bg-white rounded-lg border border-slate-200 font-mono text-[11px] text-teal-900">
              Score(D, Q) = ∑ IDF(q_i) · [f(q_i, D) · (k_1 + 1)] / [f(q_i, D) + k_1 · (1 - b + b · |D|/avgdl)]
            </div>
            <p className="text-slate-500 text-[11px]">
              Where k_1 = 1.5 and b = 0.75 regulate term frequency saturation and document length normalization.
            </p>
          </div>

          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-2">
            <h4 className="font-bold text-slate-800 text-xs">2. Hybrid Linear Re-Ranking Formula:</h4>
            <div className="p-2 bg-white rounded-lg border border-slate-200 font-mono text-[11px] text-teal-900">
              Hybrid(D, Q) = α · NormBM25(D, Q) + (1 - α) · Cosine(E_Q, E_D)
            </div>
            <p className="text-slate-500 text-[11px]">
              Where α ∈ [0, 1] is the user-configurable BM25 weight (default 0.5) and E represents unit-normalized dense embeddings.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
