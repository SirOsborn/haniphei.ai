import React from 'react';

const ShieldIcon = ({ className = "w-12 h-12", riskLevel = "high" }) => {
  const getRiskColor = () => {
    switch (riskLevel) {
      case 'high': return 'text-danger';
      case 'medium': return 'text-warning';
      case 'low': return 'text-success';
      default: return 'text-primary';
    }
  };

  return (
    <svg 
      className={className}
      viewBox="0 0 100 100" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Shield outline */}
      <path
        d="M50 10L20 25V45C20 65 35 80 50 90C65 80 80 65 80 45V25L50 10Z"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinejoin="round"
        fill="none"
        className={getRiskColor()}
      />
      
      {/* Animated pulse ring */}
      <path
        d="M50 10L20 25V45C20 65 35 80 50 90C65 80 80 65 80 45V25L50 10Z"
        stroke="currentColor"
        strokeWidth="1"
        strokeLinejoin="round"
        fill="none"
        className={`${getRiskColor()} opacity-40`}
      >
        <animate
          attributeName="stroke-width"
          values="1;4;1"
          dur="2s"
          repeatCount="indefinite"
        />
        <animate
          attributeName="opacity"
          values="0.4;0.1;0.4"
          dur="2s"
          repeatCount="indefinite"
        />
      </path>
      
      {/* Alert symbol */}
      {riskLevel === 'high' && (
        <g className="animate-pulse">
          <line x1="50" y1="35" x2="50" y2="55" stroke="currentColor" strokeWidth="3" strokeLinecap="round" className={getRiskColor()} />
          <circle cx="50" cy="65" r="2.5" fill="currentColor" className={getRiskColor()} />
        </g>
      )}
      
      {/* Checkmark */}
      {riskLevel === 'low' && (
        <g className="animate-check-draw">
          <path
            d="M35 50L45 60L65 40"
            stroke="currentColor"
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
            className={getRiskColor()}
          />
        </g>
      )}
      
      {/* Warning triangle */}
      {riskLevel === 'medium' && (
        <g className="animate-pulse">
          <path d="M50 38L60 58H40L50 38Z" stroke="currentColor" strokeWidth="2.5" fill="none" className={getRiskColor()} />
          <line x1="50" y1="45" x2="50" y2="52" stroke="currentColor" strokeWidth="2" className={getRiskColor()} />
          <circle cx="50" cy="56" r="1.5" fill="currentColor" className={getRiskColor()} />
        </g>
      )}
    </svg>
  );
};

export default ShieldIcon;
