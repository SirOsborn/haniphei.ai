import { useState } from "react";

export const useFileUpload = () => {
  const [files, setFiles] = useState([]);
  const [url, setUrl] = useState("");
  const [activeTab, setActiveTab] = useState("url");

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);
  };

  const handleUrlChange = (e) => {
    setUrl(e.target.value);
  };

  const switchTab = (tab) => {
    setActiveTab(tab);
  };

  const reset = () => {
    setFiles([]);
    setUrl("");
    setActiveTab("url");
  };

  const hasContent = () => {
    return files.length > 0 || url.trim() !== "";
  };

  return {
    files,
    url,
    activeTab,
    handleFileChange,
    handleUrlChange,
    setUrl,
    switchTab,
    reset,
    hasContent,
  };
};
