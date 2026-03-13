import React from "react";
import FileUploadZone from "../components/FileUploadZone";
import SecurityNotice from "../components/SecurityNotice";

const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(1) + " MB";
};

const ScanUploadPage = ({ files, onFileChange, textInput, onTextChange, onBack, onNext }) => {
  return (
    <main className="max-w-4xl mx-auto px-8 py-12">
      <h2 className="text-2xl font-bold text-white mb-6">Analyze Document</h2>
      
      <div className="glass-card mb-8">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          Option 1: Upload File
        </h3>
        
        {files.length === 0 ? (
          <FileUploadZone onFileChange={onFileChange} />
        ) : (
          <div className="flex flex-col items-center gap-6 py-6 border-b border-white/10 mb-6">
            <div className="w-16 h-16 rounded-full bg-green-500/20 flex items-center justify-center">
              <svg className="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div className="w-full space-y-3">
              {Array.from(files).map((file, index) => (
                <div key={index} className="flex items-center gap-4 px-4 py-3 rounded-xl bg-white/5 border border-white/10">
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-medium truncate">{file.name}</p>
                    <p className="text-gray-400 text-sm">{formatFileSize(file.size)}</p>
                  </div>
                  <button onClick={() => onFileChange({ target: { files: [] } })} className="text-gray-500 hover:text-red-400">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="glass-card mb-8">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Option 2: Quick Text Scan
        </h3>
        <textarea
          value={textInput}
          onChange={(e) => onTextChange(e.target.value)}
          placeholder="Paste contract text, legal clauses, or any text you want to analyze for risks..."
          className="w-full h-48 bg-white/5 border border-white/10 rounded-xl p-4 text-white placeholder-gray-500 focus:outline-none focus:border-primary/50 transition-colors resize-none mb-4"
          disabled={files.length > 0}
        />
        {files.length > 0 && (
          <p className="text-amber-400/80 text-sm italic">
            * Text input is disabled when a file is uploaded.
          </p>
        )}
      </div>

      <div className="flex gap-4 max-w-md mx-auto">
        <button onClick={onBack} className="btn-secondary flex-1">Back</button>
        <button
          onClick={onNext}
          disabled={files.length === 0 && !textInput.trim()}
          className="btn-primary flex-1 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Continue
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <SecurityNotice />
    </main>
  );
};

export default ScanUploadPage;
