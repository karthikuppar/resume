'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/v1/resume/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Upload failed", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-10 bg-gray-50 text-gray-900">
      <div className="max-w-4xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-blue-600">AI Resume Analyzer</h1>
          <p className="text-gray-600">Upload your PDF resume for an instant AI career roadmap.</p>
        </div>

        {/* Upload Box */}
        <form onSubmit={handleUpload} className="bg-white p-8 rounded-xl shadow-sm border border-gray-200 text-center space-y-4">
          <input 
            type="file" 
            accept=".pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          <button 
            type="submit" 
            disabled={!file || loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium disabled:opacity-50 transition-all hover:bg-blue-700"
          >
            {loading ? "Analyzing with AI..." : "Upload & Analyze"}
          </button>
        </form>

        {/* Navigation to History */}
        <div className="text-center">
          <Link href="/history" className="text-blue-600 hover:text-blue-800 underline font-medium">
            View Past Analyses &rarr;
          </Link>
        </div>

        {/* Results Section */}
        {result && (
          <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-200 space-y-6">
            <h2 className="text-2xl font-bold border-b pb-2">Analysis Results for {result.filename}</h2>
            
            <div>
              <h3 className="text-lg font-semibold text-blue-600 mb-2">Detected Skills</h3>
              <div className="flex flex-wrap gap-2">
                {result.skills.map((skill: string, index: number) => (
                  <span key={index} className="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-sm border border-blue-100">
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-blue-600 mb-2">AI Career Roadmap</h3>
              <div className="bg-gray-50 p-4 rounded-lg whitespace-pre-wrap font-mono text-sm border">
                {result.analysis_summary}
              </div>
            </div>
          </div>
        )}

      </div>
    </main>
  );
}