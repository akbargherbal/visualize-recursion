import React from 'react';

const AboutPage = () => {
  return (
    <div className="container mx-auto px-6 py-12 max-w-4xl">
      <h1 className="text-4xl font-bold mb-8 bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
        About AlgoViz
      </h1>
      
      <div className="prose prose-invert max-w-none">
        <section className="mb-8">
          <h2 className="text-2xl font-bold text-emerald-400 mb-4">What is AlgoViz?</h2>
          <p className="text-slate-300 leading-relaxed">
            AlgoViz is an interactive platform for visualizing computer science algorithms. 
            Our goal is to make complex algorithms easier to understand through step-by-step 
            visual representations of their execution.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-bold text-emerald-400 mb-4">Features</h2>
          <ul className="space-y-3 text-slate-300">
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 mt-1">✓</span>
              <span>Step-by-step execution traces with detailed state information</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 mt-1">✓</span>
              <span>Interactive visualizations for various algorithm categories</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 mt-1">✓</span>
              <span>Customizable input data for experimentation</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 mt-1">✓</span>
              <span>Playback controls to pause, rewind, and analyze execution</span>
            </li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-bold text-emerald-400 mb-4">Technology Stack</h2>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <h3 className="font-bold text-cyan-400 mb-2">Frontend</h3>
              <ul className="text-slate-300 text-sm space-y-1">
                <li>React</li>
                <li>React Router</li>
                <li>Tailwind CSS</li>
              </ul>
            </div>
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <h3 className="font-bold text-cyan-400 mb-2">Backend</h3>
              <ul className="text-slate-300 text-sm space-y-1">
                <li>Python</li>
                <li>Flask</li>
                <li>Custom Trace Engine</li>
              </ul>
            </div>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-emerald-400 mb-4">Open Source</h2>
          <p className="text-slate-300 leading-relaxed">
            AlgoViz is an open-source project. Contributions are welcome! 
            Whether you want to add new algorithms, improve visualizations, 
            or fix bugs, we'd love your help.
          </p>
        </section>
      </div>
    </div>
  );
};

export default AboutPage;