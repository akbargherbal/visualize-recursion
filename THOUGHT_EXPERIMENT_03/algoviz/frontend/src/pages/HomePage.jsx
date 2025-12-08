import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AlgorithmCard from '../components/common/AlgorithmCard';
import api from '../services/api';

const HomePage = () => {
  const [algorithms, setAlgorithms] = useState([]);
  const [categories, setCategories] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadAlgorithms();
  }, []);

  const loadAlgorithms = async () => {
    try {
      const data = await api.fetchAlgorithms();
      setAlgorithms(data);
      
      // Group by category
      const grouped = data.reduce((acc, alg) => {
        if (!acc[alg.category]) acc[alg.category] = [];
        acc[alg.category].push(alg);
        return acc;
      }, {});
      
      setCategories(grouped);
    } catch (error) {
      console.error('Failed to load algorithms:', error);
      setError('Failed to load algorithms. Make sure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleAlgorithmClick = (algorithmId) => {
    navigate(`/algorithm/${algorithmId}`);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-emerald-400 mx-auto mb-4"></div>
          <p className="text-slate-400">Loading algorithms...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center max-w-md">
          <div className="text-red-400 text-5xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-red-400 mb-2">Connection Error</h2>
          <p className="text-slate-400 mb-4">{error}</p>
          <button 
            onClick={loadAlgorithms}
            className="px-6 py-2 bg-emerald-500 hover:bg-emerald-600 rounded-lg transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-6 py-12">
      <header className="text-center mb-16">
        <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
          Algorithm Visualizer
        </h1>
        <p className="text-xl text-slate-400">
          Interactive visualizations of computer science algorithms
        </p>
      </header>

      {Object.keys(categories).length === 0 ? (
        <div className="text-center text-slate-400 py-12">
          <p className="text-xl">No algorithms available yet.</p>
          <p className="mt-2">Check your backend server.</p>
        </div>
      ) : (
        Object.entries(categories).map(([category, algs]) => (
          <section key={category} className="mb-12">
            <h2 className="text-3xl font-bold mb-6 text-emerald-400">{category}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {algs.map(algorithm => (
                <AlgorithmCard
                  key={algorithm.id}
                  algorithm={algorithm}
                  onClick={() => handleAlgorithmClick(algorithm.id)}
                />
              ))}
            </div>
          </section>
        ))
      )}
    </div>
  );
};

export default HomePage;