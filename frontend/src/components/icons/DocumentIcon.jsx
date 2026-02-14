import React from 'react';

const DocumentIcon = ({ className = "w-12 h-12" }) => {
  return (
    <svg 
      className={className}
      viewBox="0 0 100 100" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Document outline */}
      <path
        d="M30 10H60L80 30V85C80 88 78 90 75 90H25C22 90 20 88 20 85V15C20 12 22 10 25 10H30Z"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinejoin="round"
        fill="none"
        className="text-primary"
      />
      
      {/* Folded corner */}
      <path
        d="M60 10V25C60 27.5 62.5 30 65 30H80"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinejoin="round"
        fill="none"
        className="text-primary"
      />
      
      {/* Animated text lines */}
      <g className="animate-text-appear">
        <line x1="30" y1="45" x2="70" y2="45" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className="text-primary">
          <animate attributeName="x2" values="30;70" dur="1s" fill="freeze" />
        </line>
        <line x1="30" y1="55" x2="65" y2="55" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className="text-primary opacity-80">
          <animate attributeName="x2" values="30;65" dur="1s" begin="0.2s" fill="freeze" />
        </line>
        <line x1="30" y1="65" x2="60" y2="65" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className="text-primary opacity-60">
          <animate attributeName="x2" values="30;60" dur="1s" begin="0.4s" fill="freeze" />
        </line>
        <line x1="30" y1="75" x2="68" y2="75" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className="text-primary opacity-40">
          <animate attributeName="x2" values="30;68" dur="1s" begin="0.6s" fill="freeze" />
        </line>
      </g>
    </svg>
  );
};

export default DocumentIcon;
