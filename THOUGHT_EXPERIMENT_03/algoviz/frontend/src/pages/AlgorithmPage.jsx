import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';

const AlgorithmPage = () => {
  const { algorithmId } = useParams();
  const [algorithmInfo, setAlgorithmInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [trace, setTrace] = useState(null);
  const [traceLoading, setTraceLoading] = useState(false);

  useEffect(() => {
    loadAlgorithmInfo();
  }, [algorithmId]);

  const loadAlgorithmInfo = async () => {
    try {
      setLoading(true);
      const info = await api.fetchAlgorithmInfo(algorithmId);
      setAlgorithmInfo(info);
      setError(null);
    } catch (err) {
      setError('Failed to load algorithm information');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadExample = async () => {
    try {
      setTraceLoading(true);
      const example = await api.getDefaultExample(algorithmId);
      const result = await api.generateTrace(algorithmId, example);
      setTrace(result);
    } catch (err) {
      console.error('Failed to load example:', err);
      alert('Failed to load example. Check console for details.');
    } finally {
      setTraceLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-emerald-400 mx-auto mb-4"></div>
          <p className="text-slate-400">Loading algorithm...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center max-w-md">
          <div className="text-red-400 text-5xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-red-400 mb-2">Error</h2>
          <p className="text-slate-400 mb-4">{error}</p>
          <Link 
            to="/"
            className="inline-block px-6 py-2 bg-emerald-500 hover:bg-emerald-600 rounded-lg transition-colors"
          >
            Back to Home
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-6 py-12">
      <div className="mb-6">
        <Link 
          to="/" 
          className="text-emerald-400 hover:text-emerald-300 transition-colors flex items-center gap-2"
        >
          ← Back to Algorithms
        </Link>
      </div>

      <header className="mb-8">
        <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
          {algorithmInfo.name}
        </h1>
        <p className="text-xl text-slate-400">{algorithmInfo.description}</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-bold text-emerald-400 mb-2">Difficulty</h3>
          <p className="text-2xl text-white">{algorithmInfo.difficulty}</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-bold text-emerald-400 mb-2">Time Complexity</h3>
          <p className="text-2xl text-white">{algorithmInfo.complexity?.time}</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-bold text-emerald-400 mb-2">Space Complexity</h3>
          <p className="text-2xl text-white">{algorithmInfo.complexity?.space}</p>
        </div>
      </div>

      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 mb-8">
        <h2 className="text-2xl font-bold text-emerald-400 mb-4">Visualization</h2>
        
        <button
          onClick={handleLoadExample}
          disabled={traceLoading}
          className="px-6 py-3 bg-emerald-500 hover:bg-emerald-600 disabled:bg-slate-600 rounded-lg transition-colors font-medium"
        >
          {traceLoading ? 'Loading...' : 'Run Example'}
        </button>

        {trace && (
          <div className="mt-6">
            <h3 className="text-lg font-bold text-cyan-400 mb-3">Trace Output</h3>
            <div className="bg-slate-900 rounded-lg p-4 max-h-96 overflow-auto">
              <pre className="text-sm text-slate-300">
                {JSON.stringify(trace, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>

      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <h2 className="text-2xl font-bold text-emerald-400 mb-4">Tags</h2>
        <div className="flex flex-wrap gap-2">
          {algorithmInfo.tags?.map(tag => (
            <span key={tag} className="px-3 py-1 bg-slate-700 rounded-full text-sm text-slate-300">
              {tag}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AlgorithmPage;