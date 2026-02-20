import React from "react";
import FileUploadZone from "../components/FileUploadZone";
import FileList from "../components/FileList";
import SecurityNotice from "../components/SecurityNotice";

const ScanUploadPage = ({
  activeTab,
  url,
  files,
  onTabSwitch,
  onUrlChange,
  onFileChange,
  onBack,
  onNext,
}) => {
  return (
    <main className="max-w-4xl mx-auto px-8 py-12">
      <div className="glass-card mb-6">
        <div className="flex gap-4 mb-6 border-b border-white/10 pb-4">
          <button
            onClick={() => onTabSwitch("url")}
            className={`flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all duration-300 ${
              activeTab === "url"
                ? "bg-primary text-white shadow-lg"
                : "text-gray-300 hover:bg-white/10"
            }`}
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
              />
            </svg>
            URL Scanner
          </button>
          <button
            onClick={() => onTabSwitch("upload")}
            className={`flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all duration-300 ${
              activeTab === "upload"
                ? "bg-primary text-white shadow-lg"
                : "text-gray-300 hover:bg-white/10"
            }`}
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
            File Upload
          </button>
        </div>

        {activeTab === "url" ? (
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Enter URL to scan
            </label>
            <input
              type="text"
              value={url}
              onChange={onUrlChange}
              placeholder="https://example.com/document.pdf"
              className="glass-input mb-4"
            />
            <p className="text-sm text-gray-400 mb-6">
              Our AI will analyze the website for security.
            </p>
          </div>
        ) : (
          <FileUploadZone onFileChange={onFileChange} />
        )}
      </div>

      {/* Selected Files */}
      <FileList files={files} url={url} activeTab={activeTab} />

      {(files.length > 0 || url) && (
        <div className="flex gap-4 mb-6">
          <button onClick={onBack} className="btn-secondary">
            Back
          </button>
          <button
            onClick={onNext}
            className="btn-primary flex-1 flex items-center justify-center gap-2"
          >
            Next
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </button>
        </div>
      )}

      <SecurityNotice />
    </main>
  );
};

export default ScanUploadPage;
