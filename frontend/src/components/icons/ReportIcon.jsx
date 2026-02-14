import React from 'react';

const ReportIcon = ({ className = "w-12 h-12" }) => {
  return (
    <svg 
      className={className}
      viewBox="0 0 100 100" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Document with chart */}
      <rect 
        x="20" 
        y="15" 
        width="60" 
        height="70" 
        rx="4" 
        stroke="currentColor" 
        strokeWidth="2.5"
        fill="none"
        className="text-primary"
      />
      
      {/* Animated bar chart */}
      <g className="animate-chart-grow">
        <rect x="30" y="55" width="8" height="20" fill="currentColor" className="text-danger">
          <animate attributeName="height" values="20;25;20" dur="2s" repeatCount="indefinite" />
          <animate attributeName="y" values="55;50;55" dur="2s" repeatCount="indefinite" />
        </rect>
        <rect x="42" y="45" width="8" height="30" fill="currentColor" className="text-warning">
          <animate attributeName="height" values="30;35;30" dur="2s" begin="0.3s" repeatCount="indefinite" />
          <animate attributeName="y" values="45;40;45" dur="2s" begin="0.3s" repeatCount="indefinite" />
        </rect>
        <rect x="54" y="35" width="8" height="40" fill="currentColor" className="text-success">
          <animate attributeName="height" values="40;45;40" dur="2s" begin="0.6s" repeatCount="indefinite" />
          <animate attributeName="y" values="35;30;35" dur="2s" begin="0.6s" repeatCount="indefinite" />
        </rect>
        <rect x="66" y="50" width="8" height="25" fill="currentColor" className="text-info">
          <animate attributeName="height" values="25;30;25" dur="2s" begin="0.9s" repeatCount="indefinite" />
          <animate attributeName="y" values="50;45;50" dur="2s" begin="0.9s" repeatCount="indefinite" />
        </rect>
      </g>
      
      {/* Chart baseline */}
      <line x1="28" y1="76" x2="76" y2="76" stroke="currentColor" strokeWidth="2" className="text-primary" />
      
      {/* Document header lines */}
      <line x1="30" y1="25" x2="55" y2="25" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className="text-primary" />
      <line x1="30" y1="32" x2="70" y2="32" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" className="text-primary opacity-60" />
    </svg>
  );
};

export default ReportIcon;
