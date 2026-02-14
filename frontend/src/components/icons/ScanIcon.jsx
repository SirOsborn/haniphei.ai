import React from 'react';

const ScanIcon = ({ className = "w-16 h-16" }) => {
  return (
    <svg 
      className={className}
      viewBox="0 0 100 100" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Animated scanning beam */}
      <g className="animate-scan">
        <line 
          x1="20" 
          y1="50" 
          x2="80" 
          y2="50" 
          stroke="url(#scanGradient)" 
          strokeWidth="2"
          strokeLinecap="round"
        >
          <animate
            attributeName="y1"
            values="30;70;30"
            dur="2s"
            repeatCount="indefinite"
          />
          <animate
            attributeName="y2"
            values="30;70;30"
            dur="2s"
            repeatCount="indefinite"
          />
        </line>
      </g>
      
      {/* Document outline */}
      <rect 
        x="25" 
        y="20" 
        width="50" 
        height="60" 
        rx="3" 
        stroke="currentColor" 
        strokeWidth="2.5"
        fill="none"
        className="text-primary"
      />
      
      {/* Document lines */}
      <line x1="35" y1="35" x2="60" y2="35" stroke="currentColor" strokeWidth="2" className="text-primary opacity-60" />
      <line x1="35" y1="45" x2="65" y2="45" stroke="currentColor" strokeWidth="2" className="text-primary opacity-60" />
      <line x1="35" y1="55" x2="55" y2="55" stroke="currentColor" strokeWidth="2" className="text-primary opacity-60" />
      
      {/* Magnifying glass */}
      <circle 
        cx="65" 
        cy="65" 
        r="12" 
        stroke="currentColor" 
        strokeWidth="2.5" 
        fill="none"
        className="text-primary"
      />
      <line 
        x1="74" 
        y1="74" 
        x2="82" 
        y2="82" 
        stroke="currentColor" 
        strokeWidth="2.5" 
        strokeLinecap="round"
        className="text-primary"
      />
      
      <defs>
        <linearGradient id="scanGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#2563EB" stopOpacity="0" />
          <stop offset="50%" stopColor="#2563EB" stopOpacity="1" />
          <stop offset="100%" stopColor="#2563EB" stopOpacity="0" />
        </linearGradient>
      </defs>
    </svg>
  );
};

export default ScanIcon;
