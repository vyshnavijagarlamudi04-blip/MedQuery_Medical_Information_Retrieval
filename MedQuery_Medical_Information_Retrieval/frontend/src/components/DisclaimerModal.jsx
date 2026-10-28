import React from 'react';
import { AlertTriangle, ShieldCheck, X } from 'lucide-react';

export function DisclaimerBanner({ onOpenModal }) {
  return (
    <div className="bg-amber-50 border-b border-amber-200 px-4 py-2 text-xs text-amber-900 flex items-center justify-between">
      <div className="flex items-center gap-2 max-w-5xl mx-auto w-full">
        <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
        <p className="font-medium">
          <strong className="font-semibold">Educational Information Retrieval Notice:</strong> MedQuery is an educational Information Retrieval system. It retrieves and ranks relevant passages from its curated document collection and does not provide clinical medical diagnosis or replace professional medical advice.
        </p>
      </div>
      <button
        onClick={onOpenModal}
        className="text-amber-800 underline hover:text-amber-950 font-medium ml-4 shrink-0 text-xs cursor-pointer"
      >
        Learn More
      </button>
    </div>
  );
}

export function DisclaimerModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200 relative animate-in fade-in zoom-in-95 duration-150">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 p-1 rounded-lg hover:bg-slate-100 cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-teal-50 border border-teal-200 flex items-center justify-center text-teal-600">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900">Medical Safety & System Scope</h3>
            <p className="text-xs text-slate-500">Information Retrieval Project Specification</p>
          </div>
        </div>

        <div className="space-y-3 text-sm text-slate-600 leading-relaxed">
          <p className="p-3 bg-amber-50 border border-amber-200 rounded-lg text-amber-900 text-xs font-medium">
            "MedQuery is an educational information retrieval system. It retrieves information from its document collection and does not provide medical diagnosis or replace professional medical advice."
          </p>

          <h4 className="font-semibold text-slate-800 text-sm mt-3">What This System Does:</h4>
          <ul className="list-disc pl-5 space-y-1 text-xs">
            <li>Indexes a verified corpus of educational medical documents from NIH MedlinePlus, WHO, CDC, and NHS.</li>
            <li>Executes Lexical (TF-IDF, BM25) and Dense Semantic (Sentence-BERT) passage retrieval.</li>
            <li>Reranks candidate medical passages via configurable linear score fusion.</li>
            <li>Evaluates ranking accuracy using standard IR metrics (Precision@K, Recall@K, MAP, MRR, NDCG@K).</li>
          </ul>

          <h4 className="font-semibold text-slate-800 text-sm mt-3">What This System Does NOT Do:</h4>
          <ul className="list-disc pl-5 space-y-1 text-xs">
            <li>Does not formulate clinical diagnoses or symptom checks for individual patients.</li>
            <li>Does not prescribe medication dosages or generate personalized treatment recommendations.</li>
            <li>Does not replace emergency clinical triage or physician consultation.</li>
          </ul>
        </div>

        <div className="mt-6 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-medium text-sm transition-colors cursor-pointer shadow-sm"
          >
            I Understand
          </button>
        </div>
      </div>
    </div>
  );
}
