import React, { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

const Results = ({ data }) => {
  const [activeSection, setActiveSection] = useState("overview");

  if (!data || !data.success) {
    return (
      <div className="card" style={{ background: "white" }}>
        <div className="error">
          ⚠️ No results to display. Please run an analysis first.
        </div>
      </div>
    );
  }

  const { userId, rankings, courseBonus, platformWeights } = data;

  // Prepare chart data
  const platformData = Object.entries(platformWeights || {}).map(
    ([platform, weight]) => ({
      platform,
      weight: (weight * 100).toFixed(2),
    })
  );

  const COLORS = ["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe"];

  const renderOverview = () => (
    <div>
      <div className="card">
        <h2 style={{ marginBottom: "20px", color: "#333" }}>
          🎯 Analysis Summary for {userId}
        </h2>

        {rankings && rankings.length > 0 && (
          <div>
            <div className="grid">
              <div className="metric">
                <div className="metric-value">{rankings[0][1].toFixed(1)}</div>
                <div className="metric-label">Platform Rating</div>
              </div>
              <div className="metric">
                <div className="metric-value">
                  {courseBonus ? courseBonus.toFixed(1) : "0.0"}
                </div>
                <div className="metric-label">Course Bonus</div>
              </div>
              <div className="metric">
                <div className="metric-value">{rankings[0][3].toFixed(1)}</div>
                <div className="metric-label">Total Rating</div>
              </div>
              <div className="metric">
                <div className="metric-value">
                  {rankings.length > 1
                    ? `#${rankings.findIndex((r) => r[0] === userId) + 1}`
                    : "#1"}
                </div>
                <div className="metric-label">Rank</div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <h3 style={{ marginBottom: "20px", color: "#333" }}>
          📊 Platform Weight Distribution
        </h3>
        {platformData.length > 0 ? (
          <div style={{ height: "300px" }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={platformData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ platform, weight }) => `${platform}: ${weight}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="weight"
                >
                  {platformData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <div className="error">
            No platform data available for visualization.
          </div>
        )}
      </div>
    </div>
  );

  const renderPlatforms = () => (
    <div className="card">
      <h2 style={{ marginBottom: "20px", color: "#333" }}>
        🏆 Platform Breakdown
      </h2>

      {platformData.length > 0 ? (
        <div>
          <div style={{ height: "400px", marginBottom: "30px" }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={platformData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="platform" />
                <YAxis />
                <Tooltip formatter={(value) => [`${value}%`, "Weight"]} />
                <Bar dataKey="weight" fill="#667eea" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div>
            <h3 style={{ marginBottom: "16px", color: "#333" }}>
              Platform Details
            </h3>
            {platformData.map((platform, index) => (
              <div key={platform.platform} className="platform-card">
                <div className="platform-name">{platform.platform}</div>
                <div className="platform-rating">
                  Weight: {platform.weight}%
                </div>
                <div
                  style={{
                    fontSize: "0.9rem",
                    color: "#666",
                    marginTop: "4px",
                  }}
                >
                  This platform contributes {platform.weight}% to your unified
                  rating
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="error">No platform data available.</div>
      )}
    </div>
  );

  const renderCourses = () => (
    <div className="card">
      <h2 style={{ marginBottom: "20px", color: "#333" }}>
        🎓 Course Bonus Analysis
      </h2>

      {courseBonus > 0 ? (
        <div>
          <div className="success">
            🎉 Great job! You earned {courseBonus.toFixed(1)} bonus points from
            your Coursera courses.
          </div>

          <div style={{ marginTop: "20px" }}>
            <h3 style={{ color: "#333", marginBottom: "16px" }}>
              Bonus Breakdown
            </h3>
            <div className="metric">
              <div className="metric-value">{courseBonus.toFixed(1)}</div>
              <div className="metric-label">Total Course Bonus Points</div>
            </div>

            <div
              style={{
                marginTop: "20px",
                padding: "16px",
                background: "#f8f9fa",
                borderRadius: "8px",
              }}
            >
              <h4 style={{ marginBottom: "12px", color: "#333" }}>
                How Course Bonus is Calculated:
              </h4>
              <ul style={{ listStyle: "none", padding: 0, color: "#666" }}>
                <li>
                  🏛️ <strong>Institution Reputation:</strong> Top universities
                  and tech companies get higher scores
                </li>
                <li>
                  ⏱️ <strong>Course Duration:</strong> Longer, more intensive
                  courses earn more points
                </li>
                <li>
                  🔥 <strong>Field Relevance:</strong> AI, Machine Learning, and
                  Data Science courses are highly valued
                </li>
                <li>
                  💡 <strong>Skills Market Value:</strong> In-demand skills like
                  Python, React, and Cloud Computing boost your score
                </li>
              </ul>
            </div>
          </div>
        </div>
      ) : (
        <div>
          <div className="error">
            No course bonus detected. Add your Coursera profile URL to get bonus
            points!
          </div>

          <div
            style={{
              marginTop: "20px",
              padding: "16px",
              background: "#f8f9fa",
              borderRadius: "8px",
            }}
          >
            <h4 style={{ marginBottom: "12px", color: "#333" }}>
              💡 Boost Your Rating with Courses:
            </h4>
            <p style={{ color: "#666", marginBottom: "12px" }}>
              Complete courses from top institutions to earn bonus points:
            </p>
            <ul style={{ listStyle: "none", padding: 0, color: "#666" }}>
              <li>🎯 Focus on AI, Machine Learning, and Data Science</li>
              <li>
                🏛️ Choose courses from Stanford, MIT, Google, or other top
                institutions
              </li>
              <li>
                ⏱️ Longer specializations and certificate programs earn more
                points
              </li>
              <li>
                💪 Build in-demand skills like Python, Cloud Computing, and
                DevOps
              </li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );

  return (
    <div>
      <div style={{ marginBottom: "20px" }}>
        <div className="tabs">
          <div
            className={`tab ${activeSection === "overview" ? "active" : ""}`}
            onClick={() => setActiveSection("overview")}
          >
            📊 Overview
          </div>
          <div
            className={`tab ${activeSection === "platforms" ? "active" : ""}`}
            onClick={() => setActiveSection("platforms")}
          >
            🏆 Platforms
          </div>
          <div
            className={`tab ${activeSection === "courses" ? "active" : ""}`}
            onClick={() => setActiveSection("courses")}
          >
            🎓 Courses
          </div>
        </div>
      </div>

      {activeSection === "overview" && renderOverview()}
      {activeSection === "platforms" && renderPlatforms()}
      {activeSection === "courses" && renderCourses()}

      <div className="card" style={{ marginTop: "30px" }}>
        <h3 style={{ marginBottom: "16px", color: "#333" }}>🚀 What's Next?</h3>
        <div style={{ color: "#666", lineHeight: "1.6" }}>
          <p style={{ marginBottom: "12px" }}>
            <strong>Improve Your Unified Rating:</strong>
          </p>
          <ul style={{ listStyle: "none", padding: 0 }}>
            <li>📈 Continue solving problems on your strongest platforms</li>
            <li>
              🎯 Focus on platforms with higher weights in the calculation
            </li>
            <li>🎓 Complete relevant courses to boost your bonus points</li>
            <li>🔥 Maintain consistent coding activity across all platforms</li>
            <li>📊 Check back regularly to track your progress</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Results;
