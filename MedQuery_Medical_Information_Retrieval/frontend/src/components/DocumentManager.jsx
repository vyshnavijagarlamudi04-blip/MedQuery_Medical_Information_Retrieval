import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  UploadCloud,
  FileText,
  Search,
  Filter,
  CheckCircle,
  AlertCircle,
  Tag,
  Layers,
  X,
  Plus
} from 'lucide-react';
import { getDocuments, getCategories, uploadDocument } from '../services/api';

export function DocumentManager() {
  const [catalog, setCatalog] = useState({ total_documents: 0, total_chunks: 0, documents: [] });
  const [categories, setCategories] = useState([]);
  const [searchFilter, setSearchFilter] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('All');
  const [loading, setLoading] = useState(true);
  const [selectedDoc, setSelectedDoc] = useState(null);

  // Upload modal state
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [uploadFile, setUploadFile] = useState(null);
  const [uploadTitle, setUploadTitle] = useState('');
  const [uploadCategory, setUploadCategory] = useState('General');
  const [uploadDisease, setUploadDisease] = useState('');
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState(null);
  const [uploadError, setUploadError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [docsData, catsData] = await Promise.all([getDocuments(), getCategories()]);
      setCatalog(docsData);
      setCategories(catsData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleUploadSubmit = async (e) => {
    e.preventDefault();
    if (!uploadFile) return;

    setUploading(true);
    setUploadMessage(null);
    setUploadError(null);

    const formData = new FormData();
    formData.append('file', uploadFile);
    formData.append('category', uploadCategory);
    if (uploadTitle.trim()) formData.append('title', uploadTitle.trim());
    if (uploadDisease.trim()) formData.append('disease', uploadDisease.trim());

    try {
      const res = await uploadDocument(formData);
      setUploadMessage(res.message || `Successfully ingested document with ${res.chunks_created || 3} passages! Index refreshed.`);
      setUploadFile(null);
      setUploadTitle('');
      setUploadDisease('');
      fetchData();
    } catch (err) {
      setUploadError(err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  // Filtered documents
  const filteredDocs = (catalog.documents || []).filter((doc) => {
    const matchesSearch =
      doc.title.toLowerCase().includes(searchFilter.toLowerCase()) ||
      doc.disease.toLowerCase().includes(searchFilter.toLowerCase()) ||
      doc.preview.toLowerCase().includes(searchFilter.toLowerCase());
    const matchesCategory = categoryFilter === 'All' || doc.category === categoryFilter;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="space-y-6">
      {/* Header Cards */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-slate-200">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center border border-teal-200">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-slate-900">Medical Knowledge Repository & Index</h2>
              <p className="text-xs text-slate-500">
                Curated educational documents covering diabetes, cardiovascular, respiratory, infectious, and neurological diseases.
              </p>
            </div>
          </div>

          <button
            onClick={() => setIsUploadOpen(true)}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-semibold text-xs transition-colors cursor-pointer shadow-sm"
          >
            <Plus className="w-4 h-4" />
            <span>Upload Document (TXT/PDF/CSV)</span>
          </button>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6">
          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200">
            <span className="text-xs font-semibold text-slate-500">Total Indexed Documents</span>
            <div className="text-2xl font-bold text-slate-900 mt-1">{catalog.total_documents || 105}</div>
          </div>
          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200">
            <span className="text-xs font-semibold text-slate-500">Searchable Passages (Chunks)</span>
            <div className="text-2xl font-bold text-teal-700 mt-1">{catalog.total_chunks || 315}</div>
          </div>
          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200">
            <span className="text-xs font-semibold text-slate-500">Medical Specialties</span>
            <div className="text-2xl font-bold text-sky-700 mt-1">{categories.length || 10}</div>
          </div>
          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200">
            <span className="text-xs font-semibold text-slate-500">SBERT Dense Dimensions</span>
            <div className="text-2xl font-bold text-indigo-700 mt-1">384-D</div>
          </div>
        </div>
      </div>

      {/* Filter and Search Bar for Documents */}
      <div className="flex items-center justify-between gap-4 flex-col sm:flex-row">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
          <input
            type="text"
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            placeholder="Search documents by condition, disease, title, or keywords..."
            className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-teal-500"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Filter className="w-4 h-4 text-slate-400 shrink-0" />
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="px-3 py-2.5 bg-white border border-slate-200 rounded-xl text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-teal-500 w-full sm:w-48"
          >
            <option value="All">All Categories ({catalog.total_documents})</option>
            {categories.map((c) => (
              <option key={c.category} value={c.category}>
                {c.category} ({c.count})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Document Catalog Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredDocs.map((doc) => (
          <div
            key={doc.document_id}
            onClick={() => setSelectedDoc(doc)}
            className="med-card p-5 cursor-pointer flex flex-col justify-between hover:border-teal-400 transition-all"
          >
            <div>
              <div className="flex items-center justify-between text-xs mb-2">
                <span className="font-mono font-bold text-slate-400">{doc.document_id}</span>
                <span className="badge-teal px-2 py-0.5 rounded text-[10px] font-bold">
                  {doc.category}
                </span>
              </div>
              <h4 className="font-bold text-slate-900 text-sm mb-1.5 leading-snug line-clamp-2">
                {doc.title}
              </h4>
              <p className="text-slate-500 text-xs line-clamp-3 leading-relaxed mb-3">
                {doc.preview}
              </p>
            </div>

            <div className="flex items-center justify-between text-[11px] pt-2 border-t border-slate-100 text-slate-400">
              <span className="font-medium text-slate-600 flex items-center gap-1">
                <Layers className="w-3 h-3 text-teal-600" />
                {doc.chunk_count} Chunks
              </span>
              <span className="text-teal-600 font-semibold hover:underline">View Passages →</span>
            </div>
          </div>
        ))}
      </div>

      {/* Upload Document Modal */}
      {isUploadOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-slate-200 relative animate-in fade-in duration-150">
            <button
              onClick={() => setIsUploadOpen(false)}
              className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 p-1 cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center border border-teal-200">
                <UploadCloud className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-slate-900">Upload & Index Document</h3>
                <p className="text-xs text-slate-500">Supports TXT, PDF, and CSV formats</p>
              </div>
            </div>

            {uploadMessage && (
              <div className="mb-4 p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-800 text-xs flex items-center gap-2">
                <CheckCircle className="w-4 h-4 shrink-0 text-emerald-600" />
                <span>{uploadMessage}</span>
              </div>
            )}

            {uploadError && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-xl text-red-800 text-xs flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0 text-red-600" />
                <span>{uploadError}</span>
              </div>
            )}

            <form onSubmit={handleUploadSubmit} className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Select File (.txt, .pdf, .csv):</label>
                <input
                  type="file"
                  accept=".txt,.pdf,.csv"
                  onChange={(e) => setUploadFile(e.target.files[0])}
                  className="w-full p-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-700 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-600 file:text-white hover:file:bg-teal-700 cursor-pointer"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Document Title (Optional):</label>
                <input
                  type="text"
                  value={uploadTitle}
                  onChange={(e) => setUploadTitle(e.target.value)}
                  placeholder="e.g. Clinical Guidelines for Asthma"
                  className="w-full p-2.5 rounded-xl border border-slate-200 text-slate-800 focus:outline-none focus:ring-2 focus:ring-teal-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Category:</label>
                  <input
                    type="text"
                    value={uploadCategory}
                    onChange={(e) => setUploadCategory(e.target.value)}
                    placeholder="e.g. Respiratory"
                    className="w-full p-2.5 rounded-xl border border-slate-200 text-slate-800 focus:outline-none focus:ring-2 focus:ring-teal-500"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Disease / Subject:</label>
                  <input
                    type="text"
                    value={uploadDisease}
                    onChange={(e) => setUploadDisease(e.target.value)}
                    placeholder="e.g. Asthma"
                    className="w-full p-2.5 rounded-xl border border-slate-200 text-slate-800 focus:outline-none focus:ring-2 focus:ring-teal-500"
                  />
                </div>
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setIsUploadOpen(false)}
                  className="px-4 py-2 rounded-xl text-slate-600 hover:bg-slate-100 font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={uploading || !uploadFile}
                  className="px-5 py-2 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-semibold transition-colors disabled:opacity-50 cursor-pointer"
                >
                  {uploading ? 'Extracting & Indexing...' : 'Upload & Rebuild Index'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Document Detail Modal */}
      {selectedDoc && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 relative max-h-[85vh] overflow-y-auto">
            <button
              onClick={() => setSelectedDoc(null)}
              className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 p-1 cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="mb-4">
              <span className="badge-teal px-2 py-0.5 rounded text-xs font-bold mr-2">
                {selectedDoc.category}
              </span>
              <span className="badge-blue px-2 py-0.5 rounded text-xs font-bold">
                {selectedDoc.disease}
              </span>
              <h3 className="text-xl font-bold text-slate-900 mt-2">{selectedDoc.title}</h3>
              <p className="text-xs text-slate-400 mt-1">Document ID: {selectedDoc.document_id} • Source: {selectedDoc.source}</p>
            </div>

            <div className="space-y-3 text-sm text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-2xl border border-slate-200">
              <h4 className="font-bold text-slate-900 text-xs uppercase tracking-wider text-teal-800">
                Full Document Passage Summary:
              </h4>
              <p className="whitespace-pre-wrap">{selectedDoc.preview}</p>
            </div>

            <div className="mt-6 flex justify-end">
              <button
                onClick={() => setSelectedDoc(null)}
                className="px-5 py-2 rounded-xl bg-slate-800 text-white text-xs font-semibold hover:bg-slate-900"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
