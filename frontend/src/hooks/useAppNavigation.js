import { useState } from "react";
import { STEPS } from "../constants";

export const useAppNavigation = () => {
  const [step, setStep] = useState(STEPS.LANDING);
  const [showProfile, setShowProfile] = useState(false);
  const [showAbout, setShowAbout] = useState(false);

  const goToStep = (newStep) => {
    setStep(newStep);
    setShowProfile(false);
    setShowAbout(false);
  };

  const goBack = () => {
    if (step > STEPS.LANDING) {
      setStep(step - 1);
    }
  };

  const goToHome = () => {
    setStep(STEPS.LANDING);
    setShowProfile(false);
    setShowAbout(false);
  };

  const toggleProfile = () => {
    setShowProfile(!showProfile);
    setShowAbout(false);
  };

  const reset = () => {
    setStep(STEPS.LANDING);
    setShowProfile(false);
    setShowAbout(false);
  };

  return {
    step,
    showProfile,
    showAbout,
    goToStep,
    goBack,
    goToHome,
    toggleProfile,
    reset,
  };
};
