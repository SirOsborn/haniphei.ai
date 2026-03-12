import React from "react";
import FilterSidebar from "../components/FilterSidebar";
import RiskCard from "../components/RiskCard";
import SecurityNotice from "../components/SecurityNotice";
import { exportToPDF } from "../utils/exportPDF";

const ResultsPage = ({
  scanResult,
  selectedCategory,
  expandedRisk,
  onSelectCategory,
  onToggleRisk,
  onReset,
  documentType,
  isScanning,
  scanError,
}) => {
  const risks = scanResult?.risks || [];

  // Group by category to create sidebar summaries
  const categoryMap = risks.reduce((acc, risk) => {
    const category = risk.category || "Other";
    if (!acc[category]) {
      acc[category] = { id: category, category, count: 0, detail: null };
    }
    acc[category].count += 1;

    // Save a representative detail for the category (first risk)
    if (!acc[category].detail) {
      acc[category].detail = {
        title: category,
        riskLevel: "Medium Risk",
        description: risk.context || risk.risk || "No detail provided.",
        excerpts: [
          {
            text: risk.context || "",
            highlight: "",
            section: "",
          },
        ],
      };
    }

    return acc;
  }, {});

  const findings = Object.values(categoryMap);
  const totalRisks = risks.length;

  // Build a riskDetails map keyed by category
  const riskDetails = findings.reduce((acc, f) => {
    acc[f.id] = f.detail;
    return acc;
  }, {});

  return (
    <main className="max-w-7xl mx-auto px-8 py-8">
      {/* Scan status */}
      {(isScanning || scanError) && (
        <div className="glass-card mb-6 p-4">
          {isScanning && (
            <div className="text-sm text-white">Analyzing document… please wait.</div>
          )}
          {scanError && (
            <div className="text-sm text-red-300">Error: {scanError}</div>
          )}
        </div>
      )}

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
            <button
              className="btn-secondary"
              onClick={() =>
                exportToPDF({
                  findings,
                  riskDetails,
                  documentType: documentType || "Legal Document",
                })
              }
            >
              Export Report
            </button>
          </div>
        </div>
      </div>

      <SecurityNotice />
    </main>
  );
};

export default ResultsPage;
