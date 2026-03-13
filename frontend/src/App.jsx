import React, { useState } from "react";
import { useAuth } from "./hooks/useAuth";
import BackgroundEffects from "./components/BackgroundEffects";
import Header from "./components/Header";
import CookieConsent from "./components/CookieConsent";
import LandingPage from "./pages/LandingPage";
import ScanUploadPage from "./pages/ScanUploadPage";
import DocumentTypePage from "./pages/DocumentTypePage";
import ResultsPage from "./pages/ResultsPage";
import ProfilePage from "./pages/ProfilePage";
import SignInPage from "./pages/SignInPage";
import SignUpPage from "./pages/SignUpPage";
import { useAppNavigation } from "./hooks/useAppNavigation";
import { useFileUpload } from "./hooks/useFileUpload";
import { useDocumentType } from "./hooks/useDocumentType";
import { useProfile } from "./hooks/useProfile";
import { useRiskAnalysis } from "./hooks/useRiskAnalysis";
import { scanDocument } from "./services/apiClient";
import { STEPS } from "./constants";

function App() {
  // Custom hooks for state management
  const navigation = useAppNavigation();
  const fileUpload = useFileUpload();
  const documentType = useDocumentType();
  const riskAnalysis = useRiskAnalysis();
  const { user, logout } = useAuth();

  const [scanResult, setScanResult] = useState(null);
  const [scanError, setScanError] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [textInput, setTextInput] = useState("");

  // Navigation handlers
  const handleScanDocument = () => {
    navigation.goToStep(STEPS.SCAN);
  };

  const handleScrollDown = () => {
    const target = document.getElementById("about");
    if (target) {
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  const handleNext = async () => {
    if (navigation.step === STEPS.SCAN) {
      if ((!fileUpload.files || fileUpload.files.length === 0) && !textInput.trim()) {
        setScanError("Please upload a file or enter text to scan.");
        return;
      }
      setScanError(null);
      navigation.goToStep(STEPS.DOCUMENT_TYPE);
      return;
    }

    if (navigation.step === STEPS.DOCUMENT_TYPE) {
      // Perform scan by calling backend
      setIsScanning(true);
      setScanError(null);
      navigation.goToStep(STEPS.RESULTS);

      try {
        const formData = new FormData();
        if (fileUpload.files && fileUpload.files.length > 0) {
          formData.append("file", fileUpload.files[0]);
        } else if (textInput.trim()) {
          formData.append("text", textInput);
        }
        
        formData.append("document_type", documentType.documentType);

        const result = await scanDocument(formData);
        setScanResult(result);
      } catch (err) {
        console.error("Scan error:", err);
        setScanError(err.message || "An error occurred during document analysis.");
      } finally {
        setIsScanning(false);
      }
    }
  };

  const handleReset = () => {
    navigation.goToStep(STEPS.LANDING);
    fileUpload.reset();
    documentType.reset();
    riskAnalysis.reset();
    setScanResult(null);
    setScanError(null);
    setIsScanning(false);
    setTextInput("");
  };

  return (
    <div className="relative">
      <BackgroundEffects />
      <Header
        onGoHome={navigation.goToHome}
        onToggleProfile={navigation.toggleProfile}
        onBack={navigation.goBack}
        showBackButton={navigation.step > STEPS.LANDING}
        showScanButton={
          navigation.step === STEPS.LANDING &&
          !navigation.showProfile &&
          !navigation.showSignIn &&
          !navigation.showSignUp
        }
        onScanDocument={handleScanDocument}
        onGoToSignIn={navigation.goToSignIn}
        onGoToSignUp={navigation.goToSignUp}
        showAuthButtons={
          navigation.step === STEPS.LANDING &&
          !navigation.showProfile &&
          !navigation.showSignIn &&
          !navigation.showSignUp && !user
        }
        user={user}
        onLogout={logout}
      />
      <div className="relative z-10 overflow-x-hidden">
        {/* Profile Page */}
        {user && navigation.showProfile && (
          <ProfilePage
            user={user}
          />
        )}
        {/* Sign In Page */}
        {!user && navigation.showSignIn && (
          <SignInPage
            onGoHome={navigation.goToHome}
            onGoToSignUp={navigation.goToSignUp}
          />
        )}
        {/* Sign Up Page */}
        {!user && navigation.showSignUp && (
          <SignUpPage
            onGoHome={navigation.goToHome}
            onGoToSignIn={navigation.goToSignIn}
          />
        )}
        {/* Step 1: Landing Page */}
        {navigation.step === STEPS.LANDING &&
          !navigation.showProfile &&
          !navigation.showAbout &&
          !navigation.showSignIn &&
          !navigation.showSignUp && (
            <LandingPage
              onScanDocument={handleScanDocument}
              onScrollDown={handleScrollDown}
            />
          )}
        {/* Step 2: Scan/Upload Page */}
        {navigation.step === STEPS.SCAN &&
          !navigation.showProfile &&
          !navigation.showAbout &&
          !navigation.showSignIn &&
          !navigation.showSignUp && (
            <ScanUploadPage
              files={fileUpload.files}
              onFileChange={fileUpload.handleFileChange}
              textInput={textInput}
              onTextChange={setTextInput}
              onBack={navigation.goBack}
              onNext={handleNext}
            />
          )}
        {/* Step 3: Document Type Selection */}
        {navigation.step === STEPS.DOCUMENT_TYPE &&
          !navigation.showProfile &&
          !navigation.showAbout && (
            <DocumentTypePage
              documentType={documentType.documentType}
              showDropdown={documentType.showDropdown}
              onSelectType={documentType.selectType}
              onToggleDropdown={documentType.toggleDropdown}
              onBack={navigation.goBack}
              onNext={handleNext}
            />
          )}
        {/* Step 4: Results Page */}
        {navigation.step === STEPS.RESULTS &&
          !navigation.showProfile &&
          !navigation.showAbout && (
            <ResultsPage
              scanResult={scanResult}
              selectedCategory={riskAnalysis.selectedCategory}
              expandedRisk={riskAnalysis.expandedRisk}
              onSelectCategory={riskAnalysis.selectCategory}
              onToggleRisk={riskAnalysis.toggleRisk}
              onReset={handleReset}
              documentType={documentType.documentType}
              isScanning={isScanning}
              scanError={scanError}
            />
          )}
      </div>
      {/* Cookie Consent Banner */}
      <CookieConsent />
    </div>
  );
}
export default App;
