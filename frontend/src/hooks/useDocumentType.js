import { useState, useCallback } from "react";

export const useDocumentType = (initialType = "contract") => {
  const [documentType, setDocumentType] = useState(initialType);
  const [showDropdown, setShowDropdown] = useState(false);

  const selectType = useCallback((type) => {
    setDocumentType(type);
    setShowDropdown(false);
  }, []);

  const toggleDropdown = useCallback(() => {
    setShowDropdown((prev) => !prev);
  }, []);

  const closeDropdown = useCallback(() => {
    setShowDropdown(false);
  }, []);

  const reset = useCallback(() => {
    setDocumentType(initialType);
    setShowDropdown(false);
  }, [initialType]);

  return {
    documentType,
    showDropdown,
    selectType,
    toggleDropdown,
    closeDropdown,
    reset,
  };
};
