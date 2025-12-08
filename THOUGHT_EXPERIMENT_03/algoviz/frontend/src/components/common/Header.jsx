import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Header = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'text-emerald-400' : 'text-slate-300 hover:text-white';
  };

  return (
    <header className="bg-slate-800 border-b border-slate-700">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-emerald-400 to-cyan-400 rounded-lg flex items-center justify-center">
              <span className="text-slate-900 font-bold text-lg">A</span>
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
              AlgoViz
            </span>
          </Link>

          <nav className="flex gap-8">
            <Link to="/" className={`transition-colors ${isActive('/')}`}>
              Algorithms
            </Link>
            <Link to="/about" className={`transition-colors ${isActive('/about')}`}>
              About
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;