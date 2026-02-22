import React from "react";
import ScanIcon from "../components/icons/ScanIcon";
import UploadIcon from "../components/icons/UploadIcon";
import AnalyzeIcon from "../components/icons/AnalyzeIcon";
import ReportIcon from "../components/icons/ReportIcon";
import ShieldIcon from "../components/icons/ShieldIcon";
import DocumentIcon from "../components/icons/DocumentIcon";

const LandingPage = ({ onScanDocument, onScrollDown }) => {
  return (
    <main className="max-w-7xl mx-auto px-8 py-12">
      <div className="text-center mb-16">
        <div className="flex justify-center mb-6">
          <ScanIcon className="w-24 h-24" />
        </div>
        <h2 className="text-5xl font-bold text-white mb-4">
          Protect Yourself with AI-Powered Risk Analysis
        </h2>
        <p className="text-xl text-gray-200 max-w-2xl mx-auto">
          Transform legal documents to identify, categorize, and highlight
          potential risks.
        </p>
      </div>

      {/* Upload Section */}
      <div className="max-w-2xl mx-auto mb-16">
        <div className="glass-card text-center">
          <p className="text-gray-300 mb-6">
            Upload your legal document to get started with AI-powered risk
            analysis.
          </p>
          <button
            onClick={onScanDocument}
            className="btn-primary px-10 py-4 text-lg flex items-center gap-3 mx-auto"
          >
            <svg
              className="w-6 h-6"
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
            Upload Document
          </button>

          <div className="mt-4 text-center">
            <button
              type="button"
              onClick={onScrollDown}
              className="text-sm text-gray-400 hover:text-gray-300 transition-colors flex items-center justify-center gap-1 mx-auto"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
              Scroll down
            </button>
          </div>
        </div>
      </div>

      {/* Who We Are Section */}
      <div id="about" className="text-center mb-12">
        <h3 className="text-3xl font-bold text-white mb-2">Who We are</h3>
        <div className="w-24 h-1 bg-gradient-to-r from-primary to-accent-purple mx-auto rounded-full"></div>
      </div>

      <div className="grid md:grid-cols-2 gap-8 mb-16">
        <div className="glass-card">
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-2xl bg-danger/10">
              <ShieldIcon className="w-12 h-12" riskLevel="high" />
            </div>
            <div>
              <h4 className="text-xl font-semibold text-white mb-2">
                Detect Critical Risks
              </h4>
              <p className="text-gray-300">
                Automatically flag indemnity clauses, termination terms, and
                disclosure requirements.
              </p>
            </div>
          </div>
        </div>

        <div className="glass-card">
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-2xl bg-info/10">
              <DocumentIcon className="w-12 h-12" />
            </div>
            <div>
              <h4 className="text-xl font-semibold text-white mb-2">
                Reveal Hidden Assumptions
              </h4>
              <p className="text-gray-300">
                Uncover implicit dependencies and unstated obligations buried in
                the print.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="text-center mb-12">
        <h3 className="text-3xl font-bold text-white mb-2">How It Works</h3>
        <div className="w-24 h-1 bg-gradient-to-r from-primary to-accent-purple mx-auto rounded-full"></div>
      </div>

      <div className="grid md:grid-cols-3 gap-8 mb-16">
        <div className="glass-card text-center">
          <div className="flex justify-center mb-4">
            <div className="p-4 rounded-2xl bg-primary/10">
              <UploadIcon className="w-16 h-16 text-primary" />
            </div>
          </div>
          <h4 className="text-xl font-semibold text-white mb-3">
            Scan or Upload
          </h4>
          <p className="text-gray-300">
            Drop your legal document or paste a URL
          </p>
        </div>

        <div className="glass-card text-center">
          <div className="flex justify-center mb-4">
            <div className="p-4 rounded-2xl bg-accent-purple/10">
              <AnalyzeIcon className="w-16 h-16 text-accent-purple" />
            </div>
          </div>
          <h4 className="text-xl font-semibold text-white mb-3">Analyze</h4>
          <p className="text-gray-300">AI parses and scores risk</p>
        </div>

        <div className="glass-card text-center">
          <div className="flex justify-center mb-4">
            <div className="p-4 rounded-2xl bg-accent-cyan/10">
              <ReportIcon className="w-16 h-16 text-accent-cyan" />
            </div>
          </div>
          <h4 className="text-xl font-semibold text-white mb-3">Report</h4>
          <p className="text-gray-300">Get structured insights</p>
        </div>
      </div>

      {/* Security Notice */}
      <div className="glass-card max-w-3xl mx-auto">
        <div className="flex items-center gap-3">
          <svg
            className="w-6 h-6 text-primary flex-shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
            />
          </svg>
          <p className="text-gray-300">
            Your documents are processed securely. We never store or share your
            data.
          </p>
        </div>
      </div>
    </main>
  );
};

export default LandingPage;
