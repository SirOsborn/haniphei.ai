import { useState } from "react";

export const useRiskAnalysis = () => {
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [expandedRisk, setExpandedRisk] = useState(null);

  const selectCategory = (category) => {
    setSelectedCategory(category);
  };

  const toggleRisk = (riskId) => {
    setExpandedRisk(expandedRisk === riskId ? null : riskId);
  };

  const reset = () => {
    setSelectedCategory("all");
    setExpandedRisk(null);
  };

  return {
    selectedCategory,
    expandedRisk,
    selectCategory,
    toggleRisk,
    reset,
  };
};
