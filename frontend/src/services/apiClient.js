const API_BASE_URL = "http://localhost:8000";

export const scanDocument = async (formData, token) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/scan`, {
      method: "POST",
      body: formData,
      headers: {
        "Authorization": `Bearer ${token}`,
      },
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
  const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
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

export const getUserProfile = async (token) => {
  const response = await fetch(`${API_BASE_URL}/api/profile`, {
    headers: {
      "Authorization": `Bearer ${token}`,
    },
    credentials: "include"
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to get profile");
  }

  return response.json();
};