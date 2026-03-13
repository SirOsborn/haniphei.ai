import React, { useState, useEffect } from "react";
import { getDocumentHistory } from "../services/apiClient";

const AccountDropdown = ({ user, onLogout, onToggleProfile }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      const fetchDocs = async () => {
        setLoading(true);
        try {
          const docs = await getDocumentHistory();
          setDocuments(docs.slice(0, 5)); // Show only latest 5
        } catch (err) {
          console.error("Failed to fetch history:", err);
        } finally {
          setLoading(false);
        }
      };
      fetchDocs();
    }
  }, [isOpen]);

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 btn-secondary py-2 px-4 rounded-full border border-white/10 hover:border-white/20 transition-all"
      >
        <div className="w-6 h-6 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-[10px] font-bold">
          {user.email.charAt(0).toUpperCase()}
        </div>
        <span className="text-sm font-medium">Account</span>
        <svg
          className={`w-4 h-4 transition-transform ${isOpen ? "rotate-180" : ""}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          ></div>
          <div className="absolute right-0 mt-3 w-80 z-50 glass-card p-4 shadow-2xl animate-in fade-in zoom-in duration-200">
            <div className="flex flex-col gap-4">
              <div className="pb-3 border-b border-white/5">
                <p className="text-xs text-gray-400 uppercase tracking-wider font-semibold">Registered Email</p>
                <p className="text-sm text-white font-medium truncate">{user.email}</p>
              </div>

              <div>
                <div className="flex items-center justify-between mb-3">
                  <p className="text-xs text-gray-400 uppercase tracking-wider font-semibold">Recent Scans</p>
                  <button 
                    onClick={() => {
                        setIsOpen(false);
                        onToggleProfile();
                    }}
                    className="text-[10px] text-primary hover:underline"
                  >
                    View All
                  </button>
                </div>
                
                {loading ? (
                  <div className="py-4 text-center">
                    <div className="inline-block w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
                  </div>
                ) : documents.length > 0 ? (
                  <div className="space-y-2 max-h-48 overflow-y-auto pr-1 custom-scrollbar">
                    {documents.map((doc) => (
                      <div key={doc.id} className="p-2 rounded-lg bg-white/5 border border-white/5 hover:bg-white/10 transition-colors group cursor-default">
                        <p className="text-xs text-white font-medium truncate">{doc.filename}</p>
                        <p className="text-[10px] text-gray-400">{new Date(doc.created_at).toLocaleDateString()}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="py-4 text-center text-xs text-gray-500 italic">No recent scans found.</p>
                )}
              </div>

              <div className="pt-3 border-t border-white/5 flex flex-col gap-2">
                <button
                  onClick={() => {
                      setIsOpen(false);
                      onToggleProfile();
                  }}
                  className="w-full text-left p-2 rounded-lg hover:bg-white/5 text-xs text-gray-300 transition-colors"
                >
                  Manage Profile
                </button>
                <button
                  onClick={onLogout}
                  className="w-full text-left p-2 rounded-lg hover:bg-red-500/10 text-xs text-red-400 transition-colors"
                >
                  Sign Out
                </button>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default AccountDropdown;
