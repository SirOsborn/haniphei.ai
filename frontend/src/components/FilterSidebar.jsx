import React from "react";

const FilterSidebar = ({ findings, selectedCategory, onSelectCategory, totalRisks }) => {
  return (
    <div className="glass-card">
      <h3 className="text-lg font-semibold text-white mb-4">
        Filter by Category
      </h3>
      <div className="space-y-2">
        <button
          onClick={() => onSelectCategory("all")}
          className={`w-full text-left px-4 py-3 rounded-lg transition-all ${
            selectedCategory === "all"
              ? "bg-primary text-white"
              : "text-gray-300 hover:bg-white/10"
          }`}
        >
          All Findings ({totalRisks})
        </button>
        {findings.map((finding) => (
          <button
            key={finding.id}
            onClick={() => onSelectCategory(finding.category)}
            className={`w-full text-left px-4 py-3 rounded-lg transition-all ${
              selectedCategory === finding.category
                ? "bg-primary text-white"
                : "text-gray-300 hover:bg-white/10"
            }`}
          >
            <div className="text-sm">
              {finding.category} ({finding.count})
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default FilterSidebar;
