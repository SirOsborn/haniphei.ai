import { useState } from "react";
import { scanDocument } from "../services/apiClient";

export const useScanSubmission = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);

  // Function: Submit scan
  const submitScan = async (file, text) => {
    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      if (file) formData.append("file", file);
      if (text) formData.append("text", text);
      
      const result = await scanDocument(formData);
      setResults(result);
      return result;
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