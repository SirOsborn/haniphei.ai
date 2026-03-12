import { useState } from "react";
import { scanDocument } from "../services/apiClient";

export const useScanSubmission = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);

  // Function: Submit scan
  const submitScan = async (file, text, token) => {
    setLoading(true);
    setError(null);

    try {
      // Create FormData object
      // Add file to FormData if provided
      // Add text to FormData if provided
      
      // Call scanDocument from apiClient
      // Get back: { scan_id, risks, source, timestamp }
      
      // Save results to state
      return results;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Return: state and functions
  return { loading, error, results, submitScan };
};