import React, { useEffect, useState } from "react";
import { getUserProfile, getDocumentHistory } from "../services/apiClient";

const ProfilePage = ({
  user,
}) => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDocuments = async () => {
      setLoading(true);
      setError("");
      try {
        const docs = await getDocumentHistory();
        setDocuments(docs);
      } catch (err) {
        setError("Failed to load history.");
        setDocuments([]);
      }
      setLoading(false);
    };
    fetchDocuments();
  }, []);
  return (
    <main className="max-w-3xl mx-auto px-8 py-12">
      <div className="glass-card">
        <div className="flex flex-col items-center gap-6 py-8">
          <div className="w-24 h-24 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-white text-3xl font-bold shadow-lg overflow-hidden">
            <span>
              {user.email ? user.email.charAt(0).toUpperCase() : "?"}
            </span>
          </div>
          <div className="text-lg text-white font-semibold">
            {user.email}
          </div>
        </div>
        <div className="mt-8">
          <h3 className="text-xl font-bold text-white mb-4">Past Document Analyses</h3>
          {loading ? (
            <div className="text-gray-300">Loading...</div>
          ) : error ? (
            <div className="text-red-400">{error}</div>
          ) : documents.length === 0 ? (
            <div className="text-gray-300">No document history found.</div>
          ) : (
            <ul className="space-y-3">
              {documents.map((doc) => (
                <li key={doc.id} className="bg-white/5 border border-white/10 rounded-lg p-4 text-white">
                  <div className="font-semibold">{doc.filename}</div>
                  <div className="text-sm text-gray-300">Scanned: {doc.created_at ? doc.created_at.split("T")[0] : "-"}</div>
                  <div className="text-sm text-primary">File type: {doc.file_type}</div>
                  <div className="text-sm text-gray-300">Size: {doc.file_size} bytes</div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </main>
  );
};

export default ProfilePage;
