import React, { useState } from "react";
import axios from "axios";

// Configure axios to use the backend API URL
axios.defaults.baseURL = "http://localhost:5001";

const ProfileAnalyzer = ({ onAnalysisComplete, loading, setLoading }) => {
  const [formData, setFormData] = useState({
    codeforces: "",
    leetcode: "",
    codechef: "",
    coursera: "",
  });
  const [error, setError] = useState("");

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check if at least one platform is provided
    const hasData = Object.values(formData).some(
      (value) => value.trim() !== ""
    );
    if (!hasData) {
      setError("Please provide at least one platform username or profile URL.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await axios.post("/api/analyze-profile", formData);

      if (response.data.success) {
        onAnalysisComplete(response.data);
      } else {
        setError(response.data.error || "Analysis failed");
      }
    } catch (err) {
      console.error("Analysis error:", err);
      setError(
        err.response?.data?.error ||
          "Failed to analyze profile. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDemo = () => {
    setFormData({
      codeforces: "tourist",
      leetcode: "lee215",
      codechef: "gennady.korotkevich",
      coursera: "https://www.coursera.org/user/example123",
    });
  };

  return (
    <div className="card">
      <h2 style={{ marginBottom: "20px", color: "#333" }}>
        🎯 Enter Your Platform Details
      </h2>

      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group">
            <label className="form-label">🏁 Codeforces Username</label>
            <input
              type="text"
              name="codeforces"
              value={formData.codeforces}
              onChange={handleInputChange}
              placeholder="e.g., tourist"
              className="input"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label className="form-label">💻 LeetCode Username</label>
            <input
              type="text"
              name="leetcode"
              value={formData.leetcode}
              onChange={handleInputChange}
              placeholder="e.g., lee215"
              className="input"
              disabled={loading}
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label">🍳 CodeChef Username</label>
            <input
              type="text"
              name="codechef"
              value={formData.codechef}
              onChange={handleInputChange}
              placeholder="e.g., gennady.korotkevich"
              className="input"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label className="form-label">🎓 Coursera Profile URL</label>
            <input
              type="url"
              name="coursera"
              value={formData.coursera}
              onChange={handleInputChange}
              placeholder="https://www.coursera.org/user/..."
              className="input"
              disabled={loading}
            />
          </div>
        </div>

        {error && <div className="error">⚠️ {error}</div>}

        <div
          style={{
            display: "flex",
            gap: "12px",
            justifyContent: "center",
            marginTop: "24px",
          }}
        >
          <button
            type="button"
            onClick={handleDemo}
            className="button"
            disabled={loading}
            style={{ background: "#95a5a6" }}
          >
            🎮 Try Demo Data
          </button>

          <button type="submit" className="button" disabled={loading}>
            {loading ? (
              <>
                <span
                  className="spinner"
                  style={{
                    width: "16px",
                    height: "16px",
                    marginRight: "8px",
                    border: "2px solid #ffffff40",
                    borderTop: "2px solid #ffffff",
                  }}
                ></span>
                Analyzing...
              </>
            ) : (
              "🚀 Analyze Profile"
            )}
          </button>
        </div>
      </form>

      <div
        style={{
          marginTop: "30px",
          padding: "20px",
          background: "#f8f9fa",
          borderRadius: "8px",
        }}
      >
        <h3 style={{ marginBottom: "12px", color: "#333" }}>
          ℹ️ What this tool does:
        </h3>
        <ul
          style={{
            listStyle: "none",
            padding: 0,
            color: "#666",
            lineHeight: "1.6",
          }}
        >
          <li>📈 Analyzes your performance across multiple coding platforms</li>
          <li>
            ⚖️ Calculates a unified rating using advanced normalization
            algorithms
          </li>
          <li>🎓 Adds bonus points for Coursera course completions</li>
          <li>📊 Provides detailed breakdowns and insights</li>
          <li>
            🔥 Generates activity heatmaps to visualize your coding journey
          </li>
        </ul>
      </div>
    </div>
  );
};

export default ProfileAnalyzer;
