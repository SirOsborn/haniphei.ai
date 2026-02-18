import React from "react";
import FilterSidebar from "../components/FilterSidebar";
import RiskCard from "../components/RiskCard";
import SecurityNotice from "../components/SecurityNotice";
import { findings, riskDetails } from "../constants/mockData";

const ResultsPage = ({ selectedCategory, expandedRisk, onSelectCategory, onToggleRisk, onReset }) => {
  const totalRisks = findings.reduce((sum, f) => sum + f.count, 0);

  return (
    <main className="max-w-7xl mx-auto px-8 py-8">
      {/* Results Header */}
      <div className="glass-card mb-6 bg-gradient-to-r from-primary/20 to-transparent">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-white mb-2">
              We help you notice what you might miss.
            </h2>
            <p className="text-gray-300">
              No scores. No 'safe/unsafe' labels - just clear guidance.
            </p>
          </div>
          <div className="glass-card bg-white/10 px-6 py-4 text-center">
            <div className="text-4xl font-bold text-danger mb-1">
              {totalRisks}
            </div>
            <div className="text-sm text-white">Findings Risks</div>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-4 gap-6">
        {/* Sidebar - Filter Categories */}
        <div className="md:col-span-1">
          <FilterSidebar
            findings={findings}
            selectedCategory={selectedCategory}
            onSelectCategory={onSelectCategory}
            totalRisks={totalRisks}
          />
        </div>

        {/* Main Content - Detected Findings */}
        <div className="md:col-span-3">
          <div className="glass-card">
            <h3 className="text-xl font-semibold text-white mb-4">
              Detected Findings
            </h3>

            {/* Scrollable Findings List */}
            <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
              {findings.map((finding) => (
                <RiskCard
                  key={finding.id}
                  risk={finding}
                  expandedRisk={expandedRisk}
                  onToggle={onToggleRisk}
                  riskDetails={riskDetails}
                />
              ))}
            </div>
          </div>

          <div className="mt-6 flex gap-4">
            <button onClick={onReset} className="btn-primary">
              Scan Another Document
            </button>
            <button className="btn-secondary">Export Report</button>
          </div>
        </div>
      </div>

      <SecurityNotice />
    </main>
  );
};

export default ResultsPage;
