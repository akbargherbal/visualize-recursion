import React from 'react';

const AlgorithmCard = ({ algorithm, onClick }) => {
  const difficultyColors = {
    Easy: 'text-green-400 border-green-400',
    Medium: 'text-amber-400 border-amber-400',
    Hard: 'text-red-400 border-red-400'
  };

  return (
    <div 
      className="bg-slate-800 rounded-xl p-6 cursor-pointer hover:scale-105 transition-all border-2 border-slate-700 hover:border-emerald-500 shadow-lg hover:shadow-emerald-500/20"
      onClick={onClick}
    >
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-xl font-bold text-white">{algorithm.name}</h3>
        <span className={`px-2 py-1 rounded text-xs border ${difficultyColors[algorithm.difficulty] || 'text-slate-400 border-slate-400'}`}>
          {algorithm.difficulty}
        </span>
      </div>
      
      <p className="text-slate-400 text-sm mb-4 line-clamp-2">
        {algorithm.description}
      </p>
      
      <div className="flex gap-4 text-xs text-slate-500 mb-4">
        <div className="flex items-center gap-1">
          <span className="text-emerald-400">⏱</span>
          <span>{algorithm.complexity?.time || 'N/A'}</span>
        </div>
        <div className="flex items-center gap-1">
          <span className="text-cyan-400">⚡</span>
          <span>{algorithm.complexity?.space || 'N/A'}</span>
        </div>
      </div>
      
      <div className="flex flex-wrap gap-2">
        {algorithm.tags?.slice(0, 3).map(tag => (
          <span key={tag} className="px-2 py-1 bg-slate-700 rounded text-xs text-slate-300">
            {tag}
          </span>
        ))}
        {algorithm.tags?.length > 3 && (
          <span className="px-2 py-1 bg-slate-700 rounded text-xs text-slate-400">
            +{algorithm.tags.length - 3}
          </span>
        )}
      </div>
    </div>
  );
};

export default AlgorithmCard;