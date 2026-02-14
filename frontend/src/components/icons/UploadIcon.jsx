import React from 'react';

const UploadIcon = ({ className = "w-12 h-12" }) => {
  return (
    <svg 
      className={className}
      viewBox="0 0 100 100" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Cloud shape */}
      <path
        d="M70 45C70 35 62 27 52 27C47 27 42.5 29 39.5 32C37 28 33 25 28 25C20 25 13 32 13 40C13 41 13.1 42 13.3 43C8.5 45 5 50 5 56C5 64 11 70 19 70H68C77 70 84 63 84 54C84 47 79 41 72 39C71.5 41.5 70.8 43.5 70 45Z"
        fill="currentColor"
        className="text-primary opacity-20"
      />
      <path
        d="M70 45C70 35 62 27 52 27C47 27 42.5 29 39.5 32C37 28 33 25 28 25C20 25 13 32 13 40C13 41 13.1 42 13.3 43C8.5 45 5 50 5 56C5 64 11 70 19 70H68C77 70 84 63 84 54C84 47 79 41 72 39C71.5 41.5 70.8 43.5 70 45Z"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="text-primary"
      />
      
      {/* Animated upload arrow */}
      <g className="animate-upload-bounce">
        <path
          d="M50 55V35"
          stroke="currentColor"
          strokeWidth="3"
          strokeLinecap="round"
          className="text-primary"
        />
        <path
          d="M42 42L50 34L58 42"
          stroke="currentColor"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="text-primary"
        />
        <animate
          attributeName="opacity"
          values="1;0.5;1"
          dur="1.5s"
          repeatCount="indefinite"
        />
      </g>
    </svg>
  );
};

export default UploadIcon;
