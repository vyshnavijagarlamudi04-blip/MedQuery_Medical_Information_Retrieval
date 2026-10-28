import React, { useState, useEffect } from 'react';
import {
  History,
  Search,
  Clock,
  Zap,
  ArrowRight,
  RotateCcw
} from 'lucide-react';
import { getSearchHistory } from '../services/api';

export function SearchHistory({ onSelectQuery }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const data = await getSearchHistory();
      setHistory(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-slate-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center border border-teal-200">
              <History className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-slate-900">Search Query History</h2>
              <p className="text-xs text-slate-500">
                Log of recent medical queries, retrieval engines used, and measured latency.
              </p>
            </div>
          </div>

          <button
            onClick={fetchHistory}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-slate-600 hover:bg-slate-50 cursor-pointer"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Refresh</span>
          </button>
        </div>

        {/* History Table */}
        <div className="mt-6 overflow-x-auto">
          {history.length === 0 ? (
            <div className="py-12 text-center text-xs text-slate-400">
              No recent searches recorded yet. Run a query in the Search tab to view logs.
            </div>
          ) : (
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase tracking-wider text-[11px] border-y border-slate-200">
                <tr>
                  <th className="py-3 px-4 font-bold">Timestamp</th>
                  <th className="py-3 px-4 font-bold">Query</th>
                  <th className="py-3 px-4 font-bold">Method</th>
                  <th className="py-3 px-4 font-bold">Latency</th>
                  <th className="py-3 px-4 font-bold">Top Retrieved Result</th>
                  <th className="py-3 px-4 font-bold text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {history.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3 px-4 text-slate-500 whitespace-nowrap">
                      {item.timestamp}
                    </td>
                    <td className="py-3 px-4 font-semibold text-slate-900 max-w-xs truncate">
                      "{item.query}"
                    </td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-slate-100 text-slate-700 border border-slate-200">
                        {item.method}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono text-teal-700 font-semibold">
                      {item.search_time_ms} ms
                    </td>
                    <td className="py-3 px-4 text-slate-600 max-w-xs truncate">
                      {item.top_title || '--'}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => onSelectQuery(item.query, item.method)}
                        className="px-3 py-1 rounded-lg bg-teal-50 hover:bg-teal-100 text-teal-700 font-semibold text-[11px] inline-flex items-center gap-1 cursor-pointer transition-colors"
                      >
                        <span>Re-run</span>
                        <ArrowRight className="w-3 h-3" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
