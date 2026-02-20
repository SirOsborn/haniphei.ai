import React from "react";
import ShieldIcon from "./icons/ShieldIcon";

const Header = ({
  onGoHome,
  onToggleProfile,
  onBack,
  showBackButton,
  showScanButton,
  onScanDocument,
}) => {
  return (
    <header className="sticky top-0 py-4 px-8 z-[100] backdrop-blur-xl bg-[#06060A]/95 border-b border-white/5">
      <nav className="max-w-7xl mx-auto flex items-center justify-between glass-navbar">
        <div className="flex items-center gap-3">
          <ShieldIcon className="w-10 h-10" riskLevel="low" />
          <h1
            className="text-2xl font-bold text-white cursor-pointer hover:opacity-80 transition-opacity"
            onClick={onGoHome}
          >
            Haniphei.ai
          </h1>
        </div>
        <div className="flex gap-4">
          <button onClick={onGoHome} className="btn-secondary">
            Home
          </button>
          <button onClick={onToggleProfile} className="btn-secondary">
            Profile
          </button>
          {showScanButton && (
            <button onClick={onScanDocument} className="btn-primary">
              Scan Document
            </button>
          )}
          {showBackButton && (
            <button
              onClick={onBack}
              className="btn-secondary flex items-center gap-2"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 19l-7-7 7-7"
                />
              </svg>
              Back
            </button>
          )}
        </div>
      </nav>
    </header>
  );
};

export default Header;
