import React from 'react';

const AnalyzeIcon = ({ className = "w-12 h-12" }) => {
  return (
    <svg 
      className={className}
      viewBox="0 0 100 100" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Brain outline */}
      <path
        d="M30 25C25 25 20 30 20 35C20 37 20.5 38.5 21.5 40C18 41 15 44 15 48C15 51 16.5 53.5 19 55C18 57 17.5 59 17.5 61C17.5 67 22 72 28 72C29 72 30 71.8 31 71.5C32 74 34.5 76 37.5 76C39 76 40.4 75.5 41.5 74.5C42.5 76.5 44.5 78 47 78H53C55.5 78 57.5 76.5 58.5 74.5C59.6 75.5 61 76 62.5 76C65.5 76 68 74 69 71.5C70 71.8 71 72 72 72C78 72 82.5 67 82.5 61C82.5 59 82 57 81 55C83.5 53.5 85 51 85 48C85 44 82 41 78.5 40C79.5 38.5 80 37 80 35C80 30 75 25 70 25C67 25 64.5 26.5 63 28.5C61.5 26 59 24 56 24H44C41 24 38.5 26 37 28.5C35.5 26.5 33 25 30 25Z"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="text-primary"
        fill="none"
      />
      
      {/* Animated circuit lines inside brain */}
      <g className="animate-pulse">
        <circle cx="35" cy="45" r="2" fill="currentColor" className="text-primary" />
        <circle cx="50" cy="40" r="2" fill="currentColor" className="text-primary" />
        <circle cx="65" cy="45" r="2" fill="currentColor" className="text-primary" />
        <circle cx="42" cy="55" r="2" fill="currentColor" className="text-primary" />
        <circle cx="58" cy="55" r="2" fill="currentColor" className="text-primary" />
        <circle cx="50" cy="65" r="2" fill="currentColor" className="text-primary" />
        
        <line x1="35" y1="45" x2="42" y2="55" stroke="currentColor" strokeWidth="1.5" className="text-primary opacity-60" />
        <line x1="50" y1="40" x2="35" y2="45" stroke="currentColor" strokeWidth="1.5" className="text-primary opacity-60" />
        <line x1="50" y1="40" x2="65" y2="45" stroke="currentColor" strokeWidth="1.5" className="text-primary opacity-60" />
        <line x1="65" y1="45" x2="58" y2="55" stroke="currentColor" strokeWidth="1.5" className="text-primary opacity-60" />
        <line x1="42" y1="55" x2="50" y2="65" stroke="currentColor" strokeWidth="1.5" className="text-primary opacity-60" />
        <line x1="58" y1="55" x2="50" y2="65" stroke="currentColor" strokeWidth="1.5" className="text-primary opacity-60" />
      </g>
      
      {/* Animated thought sparkles */}
      <g className="animate-sparkle">
        <circle cx="25" cy="35" r="1.5" fill="currentColor" className="text-accent-purple">
          <animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite" />
        </circle>
        <circle cx="75" cy="35" r="1.5" fill="currentColor" className="text-accent-cyan">
          <animate attributeName="opacity" values="0;1;0" dur="2s" begin="0.5s" repeatCount="indefinite" />
        </circle>
      </g>
    </svg>
  );
};

export default AnalyzeIcon;
