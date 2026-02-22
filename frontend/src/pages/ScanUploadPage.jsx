import React from "react";
import FileUploadZone from "../components/FileUploadZone";
import SecurityNotice from "../components/SecurityNotice";

const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(1) + " MB";
};

const ScanUploadPage = ({ files, onFileChange, onBack, onNext }) => {
  return (
    <main className="max-w-4xl mx-auto px-8 py-12">
      <h2 className="text-2xl font-bold text-white mb-6">Upload Document</h2>
      <div className="glass-card mb-6">
        {files.length === 0 ? (
          <FileUploadZone onFileChange={onFileChange} />
        ) : (
          <div className="flex flex-col items-center gap-6 py-6">
            {/* Success icon */}
            <div className="w-20 h-20 rounded-full bg-green-500/20 flex items-center justify-center">
              <svg
                className="w-10 h-10 text-green-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>

            <div className="text-center">
              <p className="text-green-400 font-semibold text-lg mb-1">
                File ready!
              </p>
              <p className="text-gray-400 text-sm">
                Your document has been loaded successfully
              </p>
            </div>

            {/* File list */}
            <div className="w-full space-y-3">
              {Array.from(files).map((file, index) => (
                <div
                  key={index}
                  className="flex items-center gap-4 px-4 py-3 rounded-xl bg-white/5 border border-white/10"
                >
                  <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center flex-shrink-0">
                    <svg
                      className="w-5 h-5 text-primary"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                      />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-medium truncate">
                      {file.name}
                    </p>
                    <p className="text-gray-400 text-sm">
                      {formatFileSize(file.size)}
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => onFileChange({ target: { files: [] } })}
                    className="text-gray-500 hover:text-red-400 transition-colors flex-shrink-0"
                    title="Remove file"
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
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>
              ))}
            </div>

            {/* Actions */}
            <div className="flex gap-4 w-full">
              <button onClick={onBack} className="btn-secondary flex-1">
                Back
              </button>
              <button
                onClick={onNext}
                className="btn-primary flex-1 flex items-center justify-center gap-2"
              >
                Continue to Document Type
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
          </div>
        )}
      </div>

      <SecurityNotice />
    </main>
  );
};

export default ScanUploadPage;
