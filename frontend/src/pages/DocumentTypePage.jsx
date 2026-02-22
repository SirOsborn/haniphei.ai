import React, { useEffect, useRef } from "react";
import SecurityNotice from "../components/SecurityNotice";
import { DOCUMENT_TYPES } from "../constants";

const DocumentTypePage = ({
  documentType,
  showDropdown,
  onSelectType,
  onToggleDropdown,
  onBack,
  onNext,
}) => {
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
    <main
      style={{
        height: "calc(100vh - 88px)",
        display: "flex",
        alignItems: "flex-start",
        justifyContent: "center",
        paddingTop: "80px",
        padding: "0 24px",
        overflow: "hidden",
      }}
    >
      <div style={{ width: "100%", maxWidth: "560px" }}>
        <h2 className="text-2xl font-bold text-white mb-6">Document Type</h2>

        {/* Fixed-height row so buttons below NEVER move */}
        <div
          className="mb-8"
          style={{ height: "52px", position: "relative" }}
          ref={dropdownRef}
        >
          {/* Trigger */}
          <button
            onClick={onToggleDropdown}
            type="button"
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              padding: "0 16px",
              borderRadius: "8px",
              background: "rgba(255,255,255,0.1)",
              border: "1px solid rgba(255,255,255,0.2)",
              cursor: "pointer",
              width: "100%",
            }}
          >
            <span
              style={{
                color: "#fff",
                fontWeight: 600,
                textTransform: "capitalize",
              }}
            >
              {documentType}
            </span>
            <svg
              style={{
                width: 20,
                height: 20,
                color: "#fff",
                flexShrink: 0,
                transform: showDropdown ? "rotate(180deg)" : "rotate(0deg)",
                transition: "transform 0.2s ease",
                willChange: "transform",
              }}
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

          {/* Dropdown — absolute, opacity-only animation, zero layout impact */}
          <div
            style={{
              position: "absolute",
              top: "calc(100% + 8px)",
              left: 0,
              right: 0,
              zIndex: 9999,
              background: "#16152e",
              borderRadius: "12px",
              border: "1px solid rgba(99,102,241,0.45)",
              boxShadow: "0 20px 50px rgba(0,0,0,0.85)",
              overflow: "hidden",
              opacity: showDropdown ? 1 : 0,
              pointerEvents: showDropdown ? "auto" : "none",
              visibility: showDropdown ? "visible" : "hidden",
              transition: "opacity 0.15s ease",
              willChange: "opacity",
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
                style={{
                  display: "block",
                  width: "100%",
                  textAlign: "left",
                  padding: "12px 20px",
                  fontSize: "15px",
                  fontWeight: 500,
                  cursor: "pointer",
                  color: "#fff",
                  background:
                    documentType === type
                      ? "rgba(99,102,241,0.8)"
                      : "transparent",
                  border: "none",
                  textTransform: "capitalize",
                }}
                onMouseEnter={(e) => {
                  if (documentType !== type)
                    e.currentTarget.style.background = "rgba(255,255,255,0.08)";
                }}
                onMouseLeave={(e) => {
                  if (documentType !== type)
                    e.currentTarget.style.background = "transparent";
                }}
              >
                {type}
              </button>
            ))}
          </div>
        </div>

        {/* Action buttons — locked in place, completely unaffected by dropdown */}
        <div className="flex gap-4">
          <button onClick={onBack} className="btn-secondary flex-1">
            Back
          </button>
          <button
            onClick={onNext}
            className="btn-primary flex-1 flex items-center justify-center gap-2"
          >
            Analyze Document
          </button>
        </div>

        <SecurityNotice />
      </div>
    </main>
  );
};

export default DocumentTypePage;
