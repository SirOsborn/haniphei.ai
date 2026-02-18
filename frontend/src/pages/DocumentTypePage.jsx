import React, { useEffect, useRef } from "react";
import SecurityNotice from "../components/SecurityNotice";
import { DOCUMENT_TYPES } from "../constants";

const DocumentTypePage = ({ documentType, showDropdown, onSelectType, onToggleDropdown, onBack, onNext }) => {
  const dropdownRef = useRef(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        if (showDropdown) {
          onToggleDropdown();
        }
      }
    };

    if (showDropdown) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [showDropdown, onToggleDropdown]);

  return (
    <main className="max-w-2xl mx-auto px-8 py-12">
      <div className="overflow-visible">
        <h2 className="text-2xl font-bold text-white mb-6">Document Type</h2>

        <div className="relative mb-6" ref={dropdownRef}>
          <button
            onClick={onToggleDropdown}
            type="button"
            className="w-full text-left flex items-center justify-between px-4 py-3 rounded-lg bg-white/10 border border-white/20 hover:border-primary/50 transition-all cursor-pointer"
          >
            <span className="text-white capitalize font-medium">
              {documentType}
            </span>
            <svg
              className={`w-5 h-5 text-white transition-transform ${
                showDropdown ? "rotate-180" : ""
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </button>

          {showDropdown && (
            <div 
              className="absolute top-full left-0 right-0 mt-2 rounded-xl shadow-2xl border-2 border-primary/50 py-2 max-h-80 overflow-y-auto" 
              style={{ 
                zIndex: 9999,
                background: 'linear-gradient(135deg, rgba(24, 23, 46, 0.95) 0%, rgba(27, 32, 74, 0.95) 100%)',
                boxShadow: '0 12px 36px 0 rgba(30, 27, 75, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.08)'
              }}
            >
              {DOCUMENT_TYPES.map((type) => (
                <button
                  key={type}
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    onSelectType(type);
                  }}
                  className={`w-full text-left px-5 py-3 transition-all font-medium text-base cursor-pointer ${
                    documentType === type
                      ? "bg-primary text-white shadow-lg"
                      : "text-white hover:bg-primary/30 hover:text-white"
                  }`}
                >
                  <span className="capitalize">{type}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="flex gap-4">
          <button onClick={onBack} className="btn-secondary flex-1">
            Back
          </button>
          <button
            onClick={onNext}
            className="btn-primary flex-1 flex items-center justify-center gap-2"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
            Scan URL
          </button>
        </div>
      </div>

      <SecurityNotice />
    </main>
  );
};

export default DocumentTypePage;
