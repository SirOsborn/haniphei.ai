import React, { useState } from "react";
import ScanIcon from "./components/icons/ScanIcon";
import UploadIcon from "./components/icons/UploadIcon";
import AnalyzeIcon from "./components/icons/AnalyzeIcon";
import ReportIcon from "./components/icons/ReportIcon";
import ShieldIcon from "./components/icons/ShieldIcon";
import DocumentIcon from "./components/icons/DocumentIcon";
import CookieConsent from "./components/CookieConsent";

function App() {
  const [step, setStep] = useState(1); // 1: landing, 2: scan, 3: document type, 4: results
  const [activeTab, setActiveTab] = useState("url");
  const [url, setUrl] = useState("");
  const [files, setFiles] = useState([]);
  const [documentType, setDocumentType] = useState("contract");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [showDropdown, setShowDropdown] = useState(false);
  const [expandedRisk, setExpandedRisk] = useState(null);
  const [showProfile, setShowProfile] = useState(false);
  const [showAbout, setShowAbout] = useState(false);
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [profilePhoto, setProfilePhoto] = useState(null);
  const [profileData, setProfileData] = useState({
    firstName: "John",
    lastName: "Doe",
    email: "john.doe@example.com",
    userType: "freelancer"
  });

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);
  };

  const handleNext = () => {
    if (step === 2) {
      setStep(3);
    } else if (step === 3) {
      setStep(4);
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
      // Close dropdown when going back
      setShowDropdown(false);
    }
  };

  const handleScanDocument = () => {
    setStep(2);
  };

  const handleReset = () => {
    setStep(1);
    setFiles([]);
    setUrl("");
    setDocumentType("contract");
    setShowDropdown(false);
    setSelectedCategory("all");
  };

  const handlePhotoUpload = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setProfilePhoto(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const findings = [
    { id: 1, category: "Hidden Financial Risk", count: 1 },
    { id: 2, category: "Unfair Obligation", count: 0 },
    { id: 3, category: "Termination & Exist Risk", count: 1 },
    { id: 4, category: "Ambiguous or Vague Language", count: 1 },
    { id: 5, category: "Legal Protection Gaps", count: 1 },
    { id: 6, category: "Suspicious or Buried Clauses", count: 0 },
  ];

  // Mock document excerpts for each risk
  const riskDetails = {
    1: {
      title: "Hidden Financial Risk",
      riskLevel: "High Risk",
      description:
        "The contract contains clauses that may impose unexpected financial obligations or penalties that are not immediately apparent.",
      excerpts: [
        {
          text: "In the event of early termination by the Client, the Client shall be liable for all fees that would have been payable for the remainder of the contract term, plus a penalty fee equal to 25% of such remaining fees. Additionally, the Client agrees to reimburse the Company for any third-party costs incurred, including but not limited to subcontractor fees, licensing costs, and administrative expenses.",
          highlight:
            "shall be liable for all fees that would have been payable for the remainder of the contract term, plus a penalty fee equal to 25%",
          section: "Section 4.2: Termination Penalties",
        },
      ],
    },
    3: {
      title: "Termination & Exit Risk",
      riskLevel: "Medium Risk",
      description:
        "Restrictive termination clauses that may limit your ability to exit the agreement or impose significant penalties for early termination.",
      excerpts: [
        {
          text: "Either party may terminate this Agreement upon ninety (90) days written notice. However, Client must provide written justification deemed acceptable by the Company. The Company reserves the right to reject termination requests that do not meet criteria outlined in Appendix C (not included in this document).",
          highlight:
            "Client must provide written justification deemed acceptable by the Company. The Company reserves the right to reject termination requests",
          section: "Section 4.1: Termination Conditions",
        },
      ],
    },
    4: {
      title: "Ambiguous or Vague Language",
      riskLevel: "Low Risk",
      description:
        "Unclear language or undefined terms that could lead to different interpretations and potential disputes.",
      excerpts: [
        {
          text: "The Company will deliver services in a timely manner according to industry standards. All deliverables shall meet reasonable quality expectations. The Client agrees that timelines may be adjusted as necessary to ensure optimal results.",
          highlight:
            "timely manner according to industry standards... reasonable quality expectations... adjusted as necessary",
          section: "Section 2.3: Service Delivery Standards",
        },
      ],
    },
    5: {
      title: "Legal Protection Gaps",
      riskLevel: "Medium Risk",
      description:
        "Missing or inadequate legal protections that may leave you vulnerable in case of disputes or contract breaches.",
      excerpts: [
        {
          text: "The Company provides services 'as is' and makes no warranties, express or implied, regarding the services or deliverables. The Company's liability is limited to the fees paid in the preceding three (3) months. The Company shall not be liable for any indirect, incidental, or consequential damages.",
          highlight:
            "services 'as is' and makes no warranties... shall not be liable for any indirect, incidental, or consequential damages",
          section: "Section 7: Limitation of Liability",
        },
      ],
    },
  };

  const totalRisks = findings.reduce((sum, f) => sum + f.count, 0);

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Animated living background */}
      <div className="orb orb-1"></div>
      <div className="orb orb-2"></div>
      <div className="orb orb-3"></div>
      <div className="orb orb-4"></div>
      <div className="orb orb-5"></div>

      {/* Floating particles for lively effect */}
      <div className="particle particle-1"></div>
      <div className="particle particle-2"></div>
      <div className="particle particle-3"></div>
      <div className="particle particle-4"></div>
      <div className="particle particle-5"></div>
      <div className="particle particle-6"></div>
      <div className="particle particle-7"></div>
      <div className="particle particle-8"></div>

      {/* Additional sparkle effects */}
      <div className="sparkle sparkle-1"></div>
      <div className="sparkle sparkle-2"></div>
      <div className="sparkle sparkle-3"></div>
      <div className="sparkle sparkle-4"></div>

      {/* Main content */}
      <div className="relative z-10">
        {/* Header */}
        <header className="py-6 px-8">
          <nav className="max-w-7xl mx-auto flex items-center justify-between glass-navbar">
            <div className="flex items-center gap-3">
              <ShieldIcon className="w-10 h-10" riskLevel="low" />
              <h1
                className="text-2xl font-bold text-white cursor-pointer hover:opacity-80 transition-opacity"
                onClick={handleReset}
              >
                Haniphei.ai
              </h1>
            </div>
            <div className="flex gap-4">
              <button 
                onClick={() => {
                  setStep(1);
                  setShowProfile(false);
                  setShowAbout(false);
                }}
                className="btn-secondary"
              >
                Home
              </button>
              <button 
                onClick={() => {
                  setShowProfile(!showProfile);
                  setShowAbout(false);
                }}
                className="btn-secondary"
              >
                Profile
              </button>
              {step === 1 && !showProfile && (
                <button onClick={handleScanDocument} className="btn-primary">
                  Scan Document
                </button>
              )}
              {step > 1 && (
                <button
                  onClick={handleBack}
                  className="btn-secondary flex items-center gap-2"
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
                      d="M15 19l-7-7 7-7"
                    />
                  </svg>
                  Back
                </button>
              )}
            </div>
          </nav>
        </header>

        {/* Profile Page */}
        {showProfile && (
          <main className="max-w-3xl mx-auto px-8 py-12">
            <div className="glass-card">
              <div className="flex items-center justify-between mb-8">
                <h2 className="text-2xl font-bold text-white">Account Information</h2>
                {!isEditingProfile && (
                  <button 
                    onClick={() => setIsEditingProfile(true)}
                    className="btn-secondary text-sm"
                  >
                    Edit Profile
                  </button>
                )}
              </div>

              <div className="flex flex-col md:flex-row gap-8">
                {/* Profile Picture */}
                <div className="flex flex-col items-center gap-3">
                  <div className="w-24 h-24 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-white text-3xl font-bold shadow-lg overflow-hidden">
                    {profilePhoto ? (
                      <img src={profilePhoto} alt="Profile" className="w-full h-full object-cover" />
                    ) : (
                      <span>{profileData.firstName.charAt(0)}{profileData.lastName.charAt(0)}</span>
                    )}
                  </div>
                  {isEditingProfile && (
                    <div>
                      <input
                        type="file"
                        id="photo-upload"
                        accept="image/*"
                        onChange={handlePhotoUpload}
                        className="hidden"
                      />
                      <label htmlFor="photo-upload" className="btn-secondary text-xs py-1.5 px-3 cursor-pointer inline-block">
                        Upload Photo
                      </label>
                    </div>
                  )}
                </div>

                {/* Profile Form */}
                <div className="flex-1 space-y-5">
                  {/* First Name & Last Name */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-white text-sm font-semibold mb-2">
                        First Name
                      </label>
                      <input
                        type="text"
                        value={profileData.firstName}
                        onChange={(e) => setProfileData({...profileData, firstName: e.target.value})}
                        disabled={!isEditingProfile}
                        className="glass-input disabled:opacity-60 disabled:cursor-not-allowed"
                      />
                    </div>
                    <div>
                      <label className="block text-white text-sm font-semibold mb-2">
                        Last Name
                      </label>
                      <input
                        type="text"
                        value={profileData.lastName}
                        onChange={(e) => setProfileData({...profileData, lastName: e.target.value})}
                        disabled={!isEditingProfile}
                        className="glass-input disabled:opacity-60 disabled:cursor-not-allowed"
                      />
                    </div>
                  </div>

                  {/* Email Address */}
                  <div>
                    <label className="block text-white text-sm font-semibold mb-2">
                      Email Address
                    </label>
                    <input
                      type="email"
                      value={profileData.email}
                      disabled
                      className="glass-input disabled:opacity-60 disabled:cursor-not-allowed"
                    />
                    <p className="text-gray-300 text-xs mt-1">Email cannot be changed</p>
                  </div>

                  {/* User Type */}
                  <div>
                    <label className="block text-white text-sm font-semibold mb-2">
                      User Type
                    </label>
                    <select
                      value={profileData.userType}
                      onChange={(e) => setProfileData({...profileData, userType: e.target.value})}
                      disabled={!isEditingProfile}
                      className="glass-input disabled:opacity-60 disabled:cursor-not-allowed capitalize"
                    >
                      <option value="freelancer">Freelancer</option>
                      <option value="business">Business</option>
                      <option value="individual">Individual</option>
                      <option value="enterprise">Enterprise</option>
                    </select>
                  </div>

                  {/* Action Buttons */}
                  {isEditingProfile && (
                    <div className="flex gap-3 pt-4">
                      <button 
                        onClick={() => {
                          setIsEditingProfile(false);
                          // Here you would save the data
                        }}
                        className="btn-primary flex-1"
                      >
                        Save Changes
                      </button>
                      <button 
                        onClick={() => {
                          setIsEditingProfile(false);
                          // Here you would reset to original data
                        }}
                        className="btn-secondary flex-1"
                      >
                        Cancel
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </main>
        )}

        {/* Step 1: Landing Page */}
        {step === 1 && !showProfile && !showAbout && (
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

            {/* URL Scanner Section */}
            <div className="max-w-2xl mx-auto mb-16">
              <div className="glass-card">
                <div className="flex gap-2 mb-6">
                  <button className="flex-1 py-2 px-4 rounded-lg bg-primary text-white font-medium">
                    URL Scanner
                  </button>
                  <button className="flex-1 py-2 px-4 rounded-lg text-gray-300 hover:bg-white/5 transition-colors">
                    File Upload
                  </button>
                </div>
                <div className="mb-4">
                  <label
                    htmlFor="url-input"
                    className="block text-sm text-gray-300 mb-2"
                  >
                    Enter URL to scan
                  </label>
                  <input
                    id="url-input"
                    type="text"
                    placeholder="Any URL will work as an example for now :)"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white placeholder-gray-400 focus:outline-none focus:border-primary transition-colors"
                  />
                </div>
                <div className="flex gap-3">
                  <button
                    onClick={handleScanDocument}
                    className="flex-1 btn-primary"
                  >
                    Scan URL
                  </button>
                  <button className="flex-1 btn-secondary">Discard</button>
                </div>
                <div className="mt-4 text-center">
                  <button className="text-sm text-gray-400 hover:text-gray-300 transition-colors flex items-center justify-center gap-1 mx-auto">
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
            <div className="text-center mb-12">
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
                      Automatically flag indemnity clauses, termination terms,
                      and disclosure requirements.
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
                      Uncover implicit dependencies and unstated obligations
                      buried in the print.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* How It Works Section */}
            <div className="text-center mb-12">
              <h3 className="text-3xl font-bold text-white mb-2">
                How It Works
              </h3>
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
                <h4 className="text-xl font-semibold text-white mb-3">
                  Analyze
                </h4>
                <p className="text-gray-300">AI parses and scores risk</p>
              </div>

              <div className="glass-card text-center">
                <div className="flex justify-center mb-4">
                  <div className="p-4 rounded-2xl bg-accent-cyan/10">
                    <ReportIcon className="w-16 h-16 text-accent-cyan" />
                  </div>
                </div>
                <h4 className="text-xl font-semibold text-white mb-3">
                  Report
                </h4>
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
                  Your documents are processed securely. We never store or share
                  your data.
                </p>
              </div>
            </div>
          </main>
        )}

        {/* Step 2: Scan/Upload Page */}
        {step === 2 && !showProfile && !showAbout && (
          <main className="max-w-4xl mx-auto px-8 py-12">
            <div className="glass-card mb-6">
              <div className="flex gap-4 mb-6 border-b border-white/10 pb-4">
                <button
                  onClick={() => setActiveTab("url")}
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
                  onClick={() => setActiveTab("upload")}
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
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://example.com/document.pdf"
                    className="glass-input mb-4"
                  />
                  <p className="text-sm text-gray-400 mb-6">
                    Our AI will analyze the website for security.
                  </p>
                </div>
              ) : (
                <div>
                  <div
                    className="border-2 border-dashed border-primary/30 rounded-2xl p-12 text-center hover:border-primary/60 transition-all duration-300 glass cursor-pointer"
                    onClick={() =>
                      document.getElementById("fileUpload").click()
                    }
                  >
                    <UploadIcon className="w-20 h-20 mx-auto mb-4 text-primary" />
                    <p className="text-lg font-medium text-white mb-2">
                      Drop your legal document here
                    </p>
                    <p className="text-sm text-gray-400 mb-4">
                      or click to browse
                    </p>
                    <input
                      type="file"
                      className="hidden"
                      id="fileUpload"
                      multiple
                      onChange={handleFileChange}
                    />
                    <button className="btn-secondary inline-block">
                      Choose File
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Selected Files */}
            {(files.length > 0 || url) && (
              <div className="glass-card mb-6">
                <h3 className="text-lg font-semibold text-white mb-4">
                  Selected Files or URL
                </h3>
                <div className="space-y-3">
                  {files.map((file, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-3 rounded-lg bg-white/5 border border-white/10"
                    >
                      <div className="flex items-center gap-3">
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
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                          />
                        </svg>
                        <span className="text-white">{file.name}</span>
                      </div>
                      <span className="text-gray-400 text-sm">
                        {(file.size / 1024).toFixed(2)}KB
                      </span>
                    </div>
                  ))}
                  {url && activeTab === "url" && (
                    <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 border border-white/10">
                      <div className="flex items-center gap-3">
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
                            d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
                          />
                        </svg>
                        <span className="text-white">{url}</span>
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex gap-4 mt-6">
                  <button onClick={handleBack} className="btn-secondary">
                    Back
                  </button>
                  <button
                    onClick={handleNext}
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
              </div>
            )}

            {/* Security Notice */}
            <div className="flex items-center justify-center gap-2 text-gray-300">
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
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                />
              </svg>
              <p className="text-sm">
                Your documents are processed securely. We never store or share
                your data.
              </p>
            </div>
          </main>
        )}

        {/* Step 3: Document Type Selection */}
        {step === 3 && !showProfile && !showAbout && (
          <main className="max-w-2xl mx-auto px-8 py-12">
            <div className="glass-card">
              <h2 className="text-2xl font-bold text-white mb-6">
                Document Type
              </h2>

              <div className="relative mb-6">
                <button
                  onClick={() => setShowDropdown(!showDropdown)}
                  className="w-full text-left flex items-center justify-between px-4 py-3 rounded-lg bg-white/10 border border-white/20 hover:border-primary/50 transition-all"
                >
                  <span className="text-white capitalize font-medium">
                    {documentType}
                  </span>
                  <svg
                    className={`w-5 h-5 text-white transition-transform ${
                      showDropdown ? "rotate-180" : ""
                    }`}
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
                </button>

                {showDropdown && (
                  <div className="absolute top-full left-0 right-0 mt-2 glass-card z-20 shadow-2xl border-2 border-white/40 py-2">
                    {[
                      "contract",
                      "agreement",
                      "terms & conditions",
                      "policy",
                      "invoice",
                      "receipt",
                      "proposal",
                      "memorandum",
                      "other",
                    ].map((type) => (
                      <button
                        key={type}
                        onClick={() => {
                          setDocumentType(type);
                          setShowDropdown(false);
                        }}
                        className={`w-full text-left px-5 py-3 transition-all font-medium text-base ${
                          documentType === type
                            ? "bg-primary/90 text-white shadow-lg"
                            : "text-white hover:bg-white/20 hover:text-white"
                        }`}
                      >
                        <span className="capitalize">{type}</span>
                      </button>
                    ))}
                  </div>
                )}
              </div>

              <div className="flex gap-4">
                <button onClick={handleBack} className="btn-secondary flex-1">
                  Back
                </button>
                <button
                  onClick={handleNext}
                  className="btn-primary flex-1 flex items-center justify-center gap-2"
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
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    />
                  </svg>
                  Scan URL
                </button>
              </div>
            </div>

            {/* Security Notice */}
            <div className="flex items-center justify-center gap-2 text-gray-300 mt-6">
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
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                />
              </svg>
              <p className="text-sm">
                Your documents are processed securely. We never store or share
                your data.
              </p>
            </div>
          </main>
        )}

        {/* Step 4: Results Page */}
        {step === 4 && !showProfile && !showAbout && (
          <main className="max-w-7xl mx-auto px-8 py-8">
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
                <div className="glass-card">
                  <h3 className="text-lg font-semibold text-white mb-4">
                    Filter by Category
                  </h3>
                  <div className="space-y-2">
                    <button
                      onClick={() => setSelectedCategory("all")}
                      className={`w-full text-left px-4 py-3 rounded-lg transition-all ${
                        selectedCategory === "all"
                          ? "bg-primary text-white"
                          : "text-gray-300 hover:bg-white/10"
                      }`}
                    >
                      All Findings ({totalRisks})
                    </button>
                    {findings.map((finding) => (
                      <button
                        key={finding.id}
                        onClick={() => setSelectedCategory(finding.category)}
                        className={`w-full text-left px-4 py-3 rounded-lg transition-all ${
                          selectedCategory === finding.category
                            ? "bg-primary text-white"
                            : "text-gray-300 hover:bg-white/10"
                        }`}
                      >
                        <div className="text-sm">
                          {finding.category} ({finding.count})
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Main Content - Detected Findings */}
              <div className="md:col-span-3">
                <div className="glass-card">
                  <h3 className="text-xl font-semibold text-white mb-4">
                    Detected Findings
                  </h3>

                  {/* Scrollable Findings List */}
                  <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
                    {/* Hidden Financial Risk */}
                    {findings[0].count > 0 && (
                      <div
                        className={`border-l-4 border-danger rounded-lg bg-white/5 transition-all ${
                          expandedRisk === 1 ? "ring-2 ring-danger/50" : ""
                        }`}
                      >
                        <div
                          className="p-4 cursor-pointer"
                          onClick={() =>
                            setExpandedRisk(expandedRisk === 1 ? null : 1)
                          }
                        >
                          <div className="flex items-start justify-between mb-3">
                            <h4 className="text-lg font-semibold text-white">
                              Hidden Financial Risk (1)
                            </h4>
                            <div className="flex items-center gap-2">
                              <span className="badge-high-risk">High Risk</span>
                              <svg
                                className={`w-5 h-5 text-white transition-transform ${
                                  expandedRisk === 1 ? "rotate-180" : ""
                                }`}
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
                            </div>
                          </div>
                          <p className="text-gray-300 mb-3">
                            The contract contains clauses that may impose
                            unexpected financial obligations or penalties that
                            are not immediately apparent.
                          </p>
                        </div>

                        {/* Expanded Content */}
                        {expandedRisk === 1 && riskDetails[1] && (
                          <div className="px-4 pb-4 border-t border-white/10 pt-4 animate-fadeIn">
                            {riskDetails[1].excerpts.map((excerpt, idx) => (
                              <div key={idx} className="mb-4">
                                <div className="flex items-center gap-2 mb-2">
                                  <svg
                                    className="w-4 h-4 text-danger"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                  >
                                    <path
                                      fillRule="evenodd"
                                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                                      clipRule="evenodd"
                                    />
                                  </svg>
                                  <span className="text-sm font-semibold text-danger">
                                    {excerpt.section}
                                  </span>
                                </div>
                                <div className="glass-card bg-white/15 p-4 border border-white/20">
                                  <p className="text-white text-sm leading-relaxed font-medium">
                                    {excerpt.text
                                      .split(excerpt.highlight)
                                      .map((part, i, arr) => (
                                        <React.Fragment key={i}>
                                          {part}
                                          {i < arr.length - 1 && (
                                            <mark className="bg-danger/40 text-white px-1.5 py-0.5 rounded font-semibold">
                                              {excerpt.highlight}
                                            </mark>
                                          )}
                                        </React.Fragment>
                                      ))}
                                  </p>
                                </div>
                              </div>
                            ))}
                            <div className="flex gap-2 mt-4">
                              <button className="btn-secondary text-sm">
                                Explain Risk
                              </button>
                              <button className="btn-secondary text-sm">
                                Suggest Changes
                              </button>
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Termination & Exit Risk */}
                    {findings[2].count > 0 && (
                      <div
                        className={`border-l-4 border-warning rounded-lg bg-white/5 transition-all ${
                          expandedRisk === 3 ? "ring-2 ring-warning/50" : ""
                        }`}
                      >
                        <div
                          className="p-4 cursor-pointer"
                          onClick={() =>
                            setExpandedRisk(expandedRisk === 3 ? null : 3)
                          }
                        >
                          <div className="flex items-start justify-between mb-3">
                            <h4 className="text-lg font-semibold text-white">
                              Termination & Exit Risk (1)
                            </h4>
                            <div className="flex items-center gap-2">
                              <span className="px-3 py-1 bg-warning/20 text-warning rounded-full text-sm font-medium">
                                Medium Risk
                              </span>
                              <svg
                                className={`w-5 h-5 text-white transition-transform ${
                                  expandedRisk === 3 ? "rotate-180" : ""
                                }`}
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
                            </div>
                          </div>
                          <p className="text-gray-300 mb-3">
                            Restrictive termination clauses that may limit your
                            ability to exit the agreement or impose significant
                            penalties for early termination.
                          </p>
                        </div>

                        {/* Expanded Content */}
                        {expandedRisk === 3 && riskDetails[3] && (
                          <div className="px-4 pb-4 border-t border-white/10 pt-4 animate-fadeIn">
                            {riskDetails[3].excerpts.map((excerpt, idx) => (
                              <div key={idx} className="mb-4">
                                <div className="flex items-center gap-2 mb-2">
                                  <svg
                                    className="w-4 h-4 text-warning"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                  >
                                    <path
                                      fillRule="evenodd"
                                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                                      clipRule="evenodd"
                                    />
                                  </svg>
                                  <span className="text-sm font-semibold text-warning">
                                    {excerpt.section}
                                  </span>
                                </div>
                                <div className="glass-card bg-white/15 p-4 border border-white/20">
                                  <p className="text-white text-sm leading-relaxed font-medium">
                                    {excerpt.text
                                      .split(excerpt.highlight)
                                      .map((part, i, arr) => (
                                        <React.Fragment key={i}>
                                          {part}
                                          {i < arr.length - 1 && (
                                            <mark className="bg-warning/40 text-white px-1.5 py-0.5 rounded font-semibold">
                                              {excerpt.highlight}
                                            </mark>
                                          )}
                                        </React.Fragment>
                                      ))}
                                  </p>
                                </div>
                              </div>
                            ))}
                            <div className="flex gap-2 mt-4">
                              <button className="btn-secondary text-sm">
                                Explain Risk
                              </button>
                              <button className="btn-secondary text-sm">
                                Suggest Changes
                              </button>
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Ambiguous or Vague Language */}
                    {findings[3].count > 0 && (
                      <div
                        className={`border-l-4 border-info rounded-lg bg-white/5 transition-all ${
                          expandedRisk === 4 ? "ring-2 ring-info/50" : ""
                        }`}
                      >
                        <div
                          className="p-4 cursor-pointer"
                          onClick={() =>
                            setExpandedRisk(expandedRisk === 4 ? null : 4)
                          }
                        >
                          <div className="flex items-start justify-between mb-3">
                            <h4 className="text-lg font-semibold text-white">
                              Ambiguous or Vague Language (1)
                            </h4>
                            <div className="flex items-center gap-2">
                              <span className="px-3 py-1 bg-info/20 text-info rounded-full text-sm font-medium">
                                Low Risk
                              </span>
                              <svg
                                className={`w-5 h-5 text-white transition-transform ${
                                  expandedRisk === 4 ? "rotate-180" : ""
                                }`}
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
                            </div>
                          </div>
                          <p className="text-gray-300 mb-3">
                            Unclear language or undefined terms that could lead
                            to different interpretations and potential disputes.
                          </p>
                        </div>

                        {/* Expanded Content */}
                        {expandedRisk === 4 && riskDetails[4] && (
                          <div className="px-4 pb-4 border-t border-white/10 pt-4 animate-fadeIn">
                            {riskDetails[4].excerpts.map((excerpt, idx) => (
                              <div key={idx} className="mb-4">
                                <div className="flex items-center gap-2 mb-2">
                                  <svg
                                    className="w-4 h-4 text-info"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                  >
                                    <path
                                      fillRule="evenodd"
                                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                                      clipRule="evenodd"
                                    />
                                  </svg>
                                  <span className="text-sm font-semibold text-info">
                                    {excerpt.section}
                                  </span>
                                </div>
                                <div className="glass-card bg-white/15 p-4 border border-white/20">
                                  <p className="text-white text-sm leading-relaxed font-medium">
                                    {excerpt.text
                                      .split(excerpt.highlight)
                                      .map((part, i, arr) => (
                                        <React.Fragment key={i}>
                                          {part}
                                          {i < arr.length - 1 && (
                                            <mark className="bg-info/40 text-white px-1.5 py-0.5 rounded font-semibold">
                                              {excerpt.highlight}
                                            </mark>
                                          )}
                                        </React.Fragment>
                                      ))}
                                  </p>
                                </div>
                              </div>
                            ))}
                            <div className="flex gap-2 mt-4">
                              <button className="btn-secondary text-sm">
                                Explain Risk
                              </button>
                              <button className="btn-secondary text-sm">
                                Suggest Changes
                              </button>
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Legal Protection Gaps */}
                    {findings[4].count > 0 && (
                      <div
                        className={`border-l-4 border-warning rounded-lg bg-white/5 transition-all ${
                          expandedRisk === 5 ? "ring-2 ring-warning/50" : ""
                        }`}
                      >
                        <div
                          className="p-4 cursor-pointer"
                          onClick={() =>
                            setExpandedRisk(expandedRisk === 5 ? null : 5)
                          }
                        >
                          <div className="flex items-start justify-between mb-3">
                            <h4 className="text-lg font-semibold text-white">
                              Legal Protection Gaps (1)
                            </h4>
                            <div className="flex items-center gap-2">
                              <span className="px-3 py-1 bg-warning/20 text-warning rounded-full text-sm font-medium">
                                Medium Risk
                              </span>
                              <svg
                                className={`w-5 h-5 text-white transition-transform ${
                                  expandedRisk === 5 ? "rotate-180" : ""
                                }`}
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
                            </div>
                          </div>
                          <p className="text-gray-300 mb-3">
                            Missing or inadequate legal protections that may
                            leave you vulnerable in case of disputes or contract
                            breaches.
                          </p>
                        </div>

                        {/* Expanded Content */}
                        {expandedRisk === 5 && riskDetails[5] && (
                          <div className="px-4 pb-4 border-t border-white/10 pt-4 animate-fadeIn">
                            {riskDetails[5].excerpts.map((excerpt, idx) => (
                              <div key={idx} className="mb-4">
                                <div className="flex items-center gap-2 mb-2">
                                  <svg
                                    className="w-4 h-4 text-warning"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                  >
                                    <path
                                      fillRule="evenodd"
                                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                                      clipRule="evenodd"
                                    />
                                  </svg>
                                  <span className="text-sm font-semibold text-warning">
                                    {excerpt.section}
                                  </span>
                                </div>
                                <div className="glass-card bg-white/15 p-4 border border-white/20">
                                  <p className="text-white text-sm leading-relaxed font-medium">
                                    {excerpt.text
                                      .split(excerpt.highlight)
                                      .map((part, i, arr) => (
                                        <React.Fragment key={i}>
                                          {part}
                                          {i < arr.length - 1 && (
                                            <mark className="bg-warning/40 text-white px-1.5 py-0.5 rounded font-semibold">
                                              {excerpt.highlight}
                                            </mark>
                                          )}
                                        </React.Fragment>
                                      ))}
                                  </p>
                                </div>
                              </div>
                            ))}
                            <div className="flex gap-2 mt-4">
                              <button className="btn-secondary text-sm">
                                Explain Risk
                              </button>
                              <button className="btn-secondary text-sm">
                                Suggest Changes
                              </button>
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                <div className="mt-6 flex gap-4">
                  <button onClick={handleReset} className="btn-primary">
                    Scan Another Document
                  </button>
                  <button className="btn-secondary">Export Report</button>
                </div>
              </div>
            </div>

            {/* Security Notice */}
            <div className="flex items-center justify-center gap-2 text-gray-300 mt-6">
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
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                />
              </svg>
              <p className="text-sm">
                Your documents are processed securely. We never store or share
                your data.
              </p>
            </div>
          </main>
        )}
      </div>

      {/* Cookie Consent Banner */}
      <CookieConsent />
    </div>
  );
}

export default App;
