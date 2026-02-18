import React from "react";

const RiskCard = ({ risk, expandedRisk, onToggle, riskDetails }) => {
  const riskId = risk.id;
  const isExpanded = expandedRisk === riskId;
  const detail = riskDetails[riskId];

  if (!detail || risk.count === 0) {
    return null;
  }

  const getRiskColor = (level) => {
    if (level === "High Risk") return { border: "danger", bg: "danger" };
    if (level === "Medium Risk") return { border: "warning", bg: "warning" };
    return { border: "info", bg: "info" };
  };

  const colors = getRiskColor(detail.riskLevel);

  return (
    <div
      className={`border-l-4 border-${colors.border} rounded-lg bg-white/5 transition-all ${
        isExpanded ? `ring-2 ring-${colors.border}/50` : ""
      }`}
    >
      <div
        className="p-4 cursor-pointer"
        onClick={() => onToggle(riskId)}
      >
        <div className="flex items-start justify-between mb-3">
          <h4 className="text-lg font-semibold text-white">
            {detail.title} ({risk.count})
          </h4>
          <div className="flex items-center gap-2">
            <span
              className={`px-3 py-1 bg-${colors.bg}/20 text-${colors.bg} rounded-full text-sm font-medium ${
                detail.riskLevel === "High Risk" ? "badge-high-risk" : ""
              }`}
            >
              {detail.riskLevel}
            </span>
            <svg
              className={`w-5 h-5 text-white transition-transform ${
                isExpanded ? "rotate-180" : ""
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
          </div>
        </div>
        <p className="text-gray-300 mb-3">{detail.description}</p>
      </div>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="px-4 pb-4 border-t border-white/10 pt-4 animate-fadeIn">
          {detail.excerpts.map((excerpt, idx) => (
            <div key={idx} className="mb-4">
              <div className="flex items-center gap-2 mb-2">
                <svg
                  className={`w-4 h-4 text-${colors.bg}`}
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                    clipRule="evenodd"
                  />
                </svg>
                <span className={`text-sm font-semibold text-${colors.bg}`}>
                  {excerpt.section}
                </span>
              </div>
              <div className="glass-card bg-white/15 p-4 border border-white/20">
                <p className="text-white text-sm leading-relaxed font-medium">
                  {excerpt.text.split(excerpt.highlight).map((part, i, arr) => (
                    <React.Fragment key={i}>
                      {part}
                      {i < arr.length - 1 && (
                        <mark
                          className={`bg-${colors.bg}/40 text-white px-1.5 py-0.5 rounded font-semibold`}
                        >
                          {excerpt.highlight}
                        </mark>
                      )}
                    </React.Fragment>
                  ))}
                </p>
              </div>
            </div>
          ))}
          <div className="flex gap-2 mt-4">
            <button className="btn-secondary text-sm">Explain Risk</button>
            <button className="btn-secondary text-sm">Suggest Changes</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RiskCard;
