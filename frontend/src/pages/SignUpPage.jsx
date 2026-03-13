import React, { useState } from "react";
import ShieldIcon from "../components/icons/ShieldIcon";
import { useAuth } from "../hooks/useAuth";

const SignUpPage = ({ onGoHome, onGoToSignIn }) => {
  const [form, setForm] = useState({
    email: "",
    password: "",
    confirm: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const { signup, loading, error: authError } = useAuth();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.email || !form.password || !form.confirm) {
      setError("Please fill in all fields.");
      return;
    }
    if (form.password !== form.confirm) {
      setError("Passwords do not match.");
      return;
    }
    if (form.password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }
    try {
      await signup(form.email, form.password);
      onGoHome();
    } catch (err) {
      setError(err.message || "Registration failed. Please try again.");
    }
  };

  const inputStyle = {
    background: "rgba(255,255,255,0.08)",
    border: "1px solid rgba(255,255,255,0.15)",
    borderRadius: "10px",
    padding: "12px 16px",
    color: "#fff",
    fontSize: "15px",
    outline: "none",
    width: "100%",
    boxSizing: "border-box",
    transition: "border-color 0.15s ease",
  };

  const labelStyle = {
    color: "rgba(255,255,255,0.7)",
    fontSize: "13px",
    fontWeight: 600,
    letterSpacing: "0.04em",
  };

  return (
    <div
      style={{
        minHeight: "calc(100vh - 88px)",
        display: "flex",
        alignItems: "flex-start",
        justifyContent: "center",
        padding: "48px 24px 40px",
        overflow: "auto",
      }}
    >
      <div style={{ width: "100%", maxWidth: "440px" }}>
        {/* Logo mark */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            marginBottom: "32px",
            gap: "12px",
          }}
        >
          <ShieldIcon className="w-12 h-12" riskLevel="low" />
          <h1
            style={{
              color: "#fff",
              fontSize: "26px",
              fontWeight: 700,
              margin: 0,
            }}
          >
            Create account
          </h1>
          <p
            style={{
              color: "rgba(255,255,255,0.5)",
              fontSize: "14px",
              margin: 0,
            }}
          >
            Start analyzing documents with Haniphei.ai
          </p>
        </div>

        {/* Card */}
        <div
          style={{
            background: "rgba(255,255,255,0.05)",
            border: "1px solid rgba(255,255,255,0.1)",
            borderRadius: "20px",
            padding: "36px 32px",
            backdropFilter: "blur(16px)",
          }}
        >
          <form
            onSubmit={handleSubmit}
            style={{ display: "flex", flexDirection: "column", gap: "18px" }}
          >
            {/* ...existing code... */}

            {/* Email */}
            <div
              style={{ display: "flex", flexDirection: "column", gap: "8px" }}
            >
              <label style={labelStyle}>EMAIL ADDRESS</label>
              <input
                type="email"
                name="email"
                value={form.email}
                onChange={handleChange}
                placeholder="you@example.com"
                autoComplete="email"
                style={inputStyle}
                onFocus={(e) =>
                  (e.target.style.borderColor = "rgba(99,102,241,0.7)")
                }
                onBlur={(e) =>
                  (e.target.style.borderColor = "rgba(255,255,255,0.15)")
                }
              />
            </div>

            {/* Password */}
            <div
              style={{ display: "flex", flexDirection: "column", gap: "8px" }}
            >
              <label style={labelStyle}>PASSWORD</label>
              <div style={{ position: "relative" }}>
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  placeholder="Min. 8 characters"
                  autoComplete="new-password"
                  style={{ ...inputStyle, paddingRight: "44px" }}
                  onFocus={(e) =>
                    (e.target.style.borderColor = "rgba(99,102,241,0.7)")
                  }
                  onBlur={(e) =>
                    (e.target.style.borderColor = "rgba(255,255,255,0.15)")
                  }
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  style={{
                    position: "absolute",
                    right: "12px",
                    top: "50%",
                    transform: "translateY(-50%)",
                    background: "none",
                    border: "none",
                    cursor: "pointer",
                    color: "rgba(255,255,255,0.4)",
                    padding: 0,
                    display: "flex",
                  }}
                >
                  {showPassword ? (
                    <svg
                      width="18"
                      height="18"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                      />
                    </svg>
                  ) : (
                    <svg
                      width="18"
                      height="18"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                      />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            {/* Confirm Password */}
            <div
              style={{ display: "flex", flexDirection: "column", gap: "8px" }}
            >
              <label style={labelStyle}>CONFIRM PASSWORD</label>
              <input
                type={showPassword ? "text" : "password"}
                name="confirm"
                value={form.confirm}
                onChange={handleChange}
                placeholder="Re-enter password"
                autoComplete="new-password"
                style={inputStyle}
                onFocus={(e) =>
                  (e.target.style.borderColor = "rgba(99,102,241,0.7)")
                }
                onBlur={(e) =>
                  (e.target.style.borderColor = "rgba(255,255,255,0.15)")
                }
              />
            </div>

            {/* Error */}
            {error && (
              <p
                style={{
                  color: "#f87171",
                  fontSize: "13px",
                  margin: 0,
                  textAlign: "center",
                }}
              >
                {error}
              </p>
            )}

            {/* Submit */}
            <button
              type="submit"
              className="btn-primary"
              style={{
                width: "100%",
                padding: "13px",
                fontSize: "15px",
                fontWeight: 600,
                marginTop: "4px",
              }}
            >
              Create Account
            </button>
          </form>

          {/* Divider */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "12px",
              margin: "24px 0",
            }}
          >
            <div
              style={{
                flex: 1,
                height: "1px",
                background: "rgba(255,255,255,0.1)",
              }}
            />
            <span style={{ color: "rgba(255,255,255,0.3)", fontSize: "13px" }}>
              or
            </span>
            <div
              style={{
                flex: 1,
                height: "1px",
                background: "rgba(255,255,255,0.1)",
              }}
            />
          </div>

          {/* Sign in link */}
          <p
            style={{
              textAlign: "center",
              color: "rgba(255,255,255,0.5)",
              fontSize: "14px",
              margin: 0,
            }}
          >
            Already have an account?{" "}
            <button
              type="button"
              onClick={onGoToSignIn}
              style={{
                background: "none",
                border: "none",
                color: "rgba(99,102,241,0.95)",
                fontWeight: 600,
                cursor: "pointer",
                fontSize: "14px",
                padding: 0,
              }}
            >
              Sign In
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignUpPage;
