import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/common/Header';
import HomePage from './pages/HomePage';
import AlgorithmPage from './pages/AlgorithmPage';
import AboutPage from './pages/AboutPage';

function App() {
  return (
    <div className="min-h-screen bg-slate-900 text-white">
      <Header />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/algorithm/:algorithmId" element={<AlgorithmPage />} />
        <Route path="/about" element={<AboutPage />} />
      </Routes>
    </div>
  );
}

export default App;