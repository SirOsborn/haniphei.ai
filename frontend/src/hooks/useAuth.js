import { useState } from "react";
import { loginUser, signupUser } from "../services/apiClient";

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Function: Handle login
  const login = async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const response = await loginUser(email, password);
      setToken(response.access_token);
      localStorage.setItem("token", response.access_token);
      setUser(response.user);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Function: Handle signup
  const signup = async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const response = await signupUser(email, password);
      setToken(response.access_token);
      localStorage.setItem("token", response.access_token);
      setUser(response.user);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Function: Logout
  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token");
  };

  // Return: state and functions
  return { user, token, loading, error, login, signup, logout };
};