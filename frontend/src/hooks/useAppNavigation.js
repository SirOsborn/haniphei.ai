import { useState } from "react";
import { STEPS } from "../constants";

export const useAppNavigation = () => {
  const [step, setStep] = useState(STEPS.LANDING);
  const [showProfile, setShowProfile] = useState(false);
  const [showAbout, setShowAbout] = useState(false);
  const [showSignIn, setShowSignIn] = useState(false);
  const [showSignUp, setShowSignUp] = useState(false);

  const clearOverlays = () => {
    setShowProfile(false);
    setShowAbout(false);
    setShowSignIn(false);
    setShowSignUp(false);
  };

  const goToStep = (newStep) => {
    setStep(newStep);
    clearOverlays();
  };

  const goBack = () => {
    if (step > STEPS.LANDING) {
      setStep(step - 1);
    }
  };

  const goToHome = () => {
    setStep(STEPS.LANDING);
    clearOverlays();
  };

  const toggleProfile = () => {
    const next = !showProfile;
    clearOverlays();
    setShowProfile(next);
  };

  const goToSignIn = () => {
    clearOverlays();
    setShowSignIn(true);
  };

  const goToSignUp = () => {
    clearOverlays();
    setShowSignUp(true);
  };

  const reset = () => {
    setStep(STEPS.LANDING);
    clearOverlays();
  };

  return {
    step,
    showProfile,
    showAbout,
    showSignIn,
    showSignUp,
    goToStep,
    goBack,
    goToHome,
    toggleProfile,
    goToSignIn,
    goToSignUp,
    reset,
  };
};
