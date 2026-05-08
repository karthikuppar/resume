'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function History() {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch the data from your FastAPI backend endpoint
    const fetchHistory = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/resume/history');
        const data = await response.json();
        setHistory(data);
      } catch (error) {
        console.error("Failed to fetch history:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  return (
    <main className="min-h-screen p-10 bg-gray-50 text-gray-900">
      <div className="max-w-5xl mx-auto space-y-8">
        
        {/* Header & Navigation */}
        <div className="flex justify-between items-center border-b pb-4">
          <h1 className="text-3xl font-bold text-blue-600">Analysis History</h1>
          <Link href="/" className="bg-white border border-blue-600 text-blue-600 px-4 py-2 rounded-lg hover:bg-blue-50 transition">
            &larr; Back to Upload
          </Link>
        </div>

        {/* Loading State */}
        {loading && <p className="text-center text-gray-500">Loading your history...</p>}

        {/* History Grid */}
        {!loading && history.length === 0 && (
          <p className="text-center text-gray-500">No resumes analyzed yet. Go upload one!</p>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {history.map((record) => (
            <div key={record.id} className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 flex flex-col space-y-4">
              <h2 className="text-xl font-bold">{record.filename}</h2>
              
              <div>
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Core Skills</h3>
                <div className="flex flex-wrap gap-2">
                  {record.skills.map((skill: string, index: number) => (
                    <span key={index} className="bg-blue-50 text-blue-700 px-2 py-1 rounded text-xs border border-blue-100">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              <div className="flex-grow">
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Summary Preview</h3>
                <p className="text-sm text-gray-600 line-clamp-3">
                  {record.analysis_summary}
                </p>
              </div>
            </div>
          ))}
        </div>

      </div>
    </main>
  );
}