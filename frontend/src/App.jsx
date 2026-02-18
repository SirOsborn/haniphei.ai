import React from "react";
import BackgroundEffects from "./components/BackgroundEffects";
import Header from "./components/Header";
import CookieConsent from "./components/CookieConsent";
import LandingPage from "./pages/LandingPage";
import ScanUploadPage from "./pages/ScanUploadPage";
import DocumentTypePage from "./pages/DocumentTypePage";
import ResultsPage from "./pages/ResultsPage";
import ProfilePage from "./pages/ProfilePage";
import { useAppNavigation } from "./hooks/useAppNavigation";
import { useFileUpload } from "./hooks/useFileUpload";
import { useDocumentType } from "./hooks/useDocumentType";
import { useProfile } from "./hooks/useProfile";
import { useRiskAnalysis } from "./hooks/useRiskAnalysis";
import { STEPS } from "./constants";

function App() {
  // Custom hooks for state management
  const navigation = useAppNavigation();
  const fileUpload = useFileUpload();
  const documentType = useDocumentType();
  const profile = useProfile();
  const riskAnalysis = useRiskAnalysis();

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

  const handleNext = () => {
    if (navigation.step === STEPS.SCAN) {
      navigation.goToStep(STEPS.DOCUMENT_TYPE);
    } else if (navigation.step === STEPS.DOCUMENT_TYPE) {
      navigation.goToStep(STEPS.RESULTS);
    }
  };

  const handleReset = () => {
    navigation.reset();
    fileUpload.reset();
    documentType.reset();
    riskAnalysis.reset();
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background Effects */}
      <BackgroundEffects />

      {/* Header - Outside main content for proper stacking */}
      <Header
        onGoHome={navigation.goToHome}
        onToggleProfile={navigation.toggleProfile}
        onBack={navigation.goBack}
        showBackButton={navigation.step > STEPS.LANDING}
        showScanButton={
          navigation.step === STEPS.LANDING && !navigation.showProfile
        }
        onScanDocument={handleScanDocument}
      />

      {/* Main content */}
      <div className="relative z-10">

        {/* Profile Page */}
        {navigation.showProfile && (
          <ProfilePage
            profileData={profile.profileData}
            profilePhoto={profile.profilePhoto}
            isEditingProfile={profile.isEditingProfile}
            onUpdate={profile.updateProfile}
            onPhotoUpload={profile.handlePhotoUpload}
            onStartEdit={profile.startEditing}
            onCancel={profile.cancelEditing}
            onSave={profile.saveProfile}
          />
        )}

        {/* Step 1: Landing Page */}
        {navigation.step === STEPS.LANDING &&
          !navigation.showProfile &&
          !navigation.showAbout && (
            <LandingPage
              activeTab={fileUpload.activeTab}
              url={fileUpload.url}
              files={fileUpload.files}
              onTabSwitch={fileUpload.switchTab}
              onUrlChange={fileUpload.handleUrlChange}
              onFileChange={fileUpload.handleFileChange}
              onScanDocument={handleScanDocument}
              onScrollDown={handleScrollDown}
            />
          )}

        {/* Step 2: Scan/Upload Page */}
        {navigation.step === STEPS.SCAN &&
          !navigation.showProfile &&
          !navigation.showAbout && (
            <ScanUploadPage
              activeTab={fileUpload.activeTab}
              url={fileUpload.url}
              files={fileUpload.files}
              onTabSwitch={fileUpload.switchTab}
              onUrlChange={fileUpload.handleUrlChange}
              onFileChange={fileUpload.handleFileChange}
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
              selectedCategory={riskAnalysis.selectedCategory}
              expandedRisk={riskAnalysis.expandedRisk}
              onSelectCategory={riskAnalysis.selectCategory}
              onToggleRisk={riskAnalysis.toggleRisk}
              onReset={handleReset}
            />
          )}
      </div>

      {/* Cookie Consent Banner */}
      <CookieConsent />
    </div>
  );
}

export default App;
