import React, { useState, useEffect } from "react";

function CookieConsent() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Check if user has already given consent
    const hasConsent = localStorage.getItem("cookieConsent");
    if (!hasConsent) {
      // Show banner after a short delay for better UX
      setTimeout(() => setIsVisible(true), 1000);
    }
  }, []);

  const handleAccept = () => {
    localStorage.setItem("cookieConsent", "true");
    setIsVisible(false);
  };

  const handleDecline = () => {
    localStorage.setItem("cookieConsent", "false");
    setIsVisible(false);
  };

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 p-4 animate-slide-up">
      <div className="max-w-5xl mx-auto glass-card">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-start gap-4 flex-1">
            <div className="p-2 rounded-lg bg-primary/20">
              <svg
                className="w-6 h-6 text-primary"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"
                />
              </svg>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">
                We Value Your Privacy
              </h3>
              <p className="text-gray-300 text-sm">
                We use cookies and similar technologies to improve your
                experience, analyze website traffic, and provide personalized
                content. By clicking "Accept", you consent to our use of
                cookies. Your document data is never stored or shared with third
                parties.
              </p>
            </div>
          </div>
          <div className="flex gap-3 flex-shrink-0">
            <button
              onClick={handleDecline}
              className="btn-secondary whitespace-nowrap"
            >
              Decline
            </button>
            <button
              onClick={handleAccept}
              className="btn-primary whitespace-nowrap"
            >
              Accept
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CookieConsent;
