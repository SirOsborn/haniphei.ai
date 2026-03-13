const API_BASE_URL = import.meta.env.VITE_API_URL || "";
// Check if API_BASE_URL is set in production
if (import.meta.env.PROD && !API_BASE_URL) {
  console.warn("VITE_API_URL is not defined in production build!");
}

export const scanDocument = async (formData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/scan`, {
      method: "POST",
      body: formData,
      credentials: "include"
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Scan failed");
    }

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};

export const loginUser = async (email, password) => {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
    credentials: "include"
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Login failed");
  }

  return response.json();
};

export const signupUser = async (email, password) => {
  const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
    credentials: "include"
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Signup failed");
  }

  return response.json();
};

export const getUserProfile = async () => {
  const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
    credentials: "include"
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to get profile");
  }

  return response.json();
};

export const getDocumentHistory = async () => {
  const response = await fetch(`${API_BASE_URL}/api/documents`, {
    credentials: "include"
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to load history");
  }

  const data = await response.json();
  return data.documents || [];
};

export const deleteDocument = async (documentId) => {
  const response = await fetch(`${API_BASE_URL}/api/documents/${documentId}`, {
    method: "DELETE",
    credentials: "include"
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to delete document");
  }

  return true;
};