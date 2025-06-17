import React, { useState } from "react";
import axios from "axios";
import CalendarHeatmap from "react-calendar-heatmap";
import "react-calendar-heatmap/dist/styles.css";

const HeatmapViewer = () => {
  const [formData, setFormData] = useState({
    codeforces: "",
    leetcode: "",
    codechef: "",
  });
  const [heatmapData, setHeatmapData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [stats, setStats] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const hasData = Object.values(formData).some(
      (value) => value.trim() !== ""
    );
    if (!hasData) {
      setError("Please provide at least one platform username.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await axios.post("/api/heatmap", formData);

      if (response.data.success) {
        const combined = response.data.combined;

        // Convert to format expected by react-calendar-heatmap
        const today = new Date();
        const oneYearAgo = new Date(
          today.getFullYear() - 1,
          today.getMonth(),
          today.getDate()
        );

        const heatmapArray = [];
        const currentDate = new Date(oneYearAgo);

        while (currentDate <= today) {
          const dateStr = currentDate.toISOString().split("T")[0];
          heatmapArray.push({
            date: dateStr,
            count: combined[dateStr] || 0,
          });
          currentDate.setDate(currentDate.getDate() + 1);
        }

        setHeatmapData(heatmapArray);

        // Calculate stats
        const totalContributions = heatmapArray.reduce(
          (sum, day) => sum + day.count,
          0
        );
        const activeDays = heatmapArray.filter((day) => day.count > 0).length;

        // Calculate max streak
        let maxStreak = 0;
        let currentStreak = 0;
        let tempStreak = 0;

        heatmapArray.forEach((day, index) => {
          if (day.count > 0) {
            tempStreak++;
            maxStreak = Math.max(maxStreak, tempStreak);
            if (index === heatmapArray.length - 1) {
              currentStreak = tempStreak;
            }
          } else {
            if (index === heatmapArray.length - 1) {
              currentStreak = 0;
            }
            tempStreak = 0;
          }
        });

        setStats({
          totalContributions,
          activeDays,
          maxStreak,
          currentStreak,
        });
      } else {
        setError(response.data.error || "Failed to generate heatmap");
      }
    } catch (err) {
      console.error("Heatmap error:", err);
      setError(
        err.response?.data?.error ||
          "Failed to generate heatmap. Please try again."
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
    });
  };

  return (
    <div className="card">
      <h2 style={{ marginBottom: "20px", color: "#333" }}>
        🔥 Coding Activity Heatmap
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
                Generating...
              </>
            ) : (
              "📊 Generate Heatmap"
            )}
          </button>
        </div>
      </form>

      {stats && (
        <div style={{ marginTop: "30px" }}>
          <h3 style={{ marginBottom: "20px", color: "#333" }}>
            📈 Activity Statistics
          </h3>
          <div className="grid">
            <div className="metric">
              <div className="metric-value">{stats.totalContributions}</div>
              <div className="metric-label">Total Contributions</div>
            </div>
            <div className="metric">
              <div className="metric-value">{stats.activeDays}</div>
              <div className="metric-label">Active Days</div>
            </div>
            <div className="metric">
              <div className="metric-value">{stats.maxStreak}</div>
              <div className="metric-label">Longest Streak</div>
            </div>
            <div className="metric">
              <div className="metric-value">{stats.currentStreak}</div>
              <div className="metric-label">Current Streak</div>
            </div>
          </div>
        </div>
      )}

      {heatmapData && (
        <div className="heatmap-container">
          <h3 className="heatmap-title">📅 Your Coding Journey (Past Year)</h3>
          <div
            style={{
              overflow: "auto",
              padding: "20px",
              background: "#f8f9fa",
              borderRadius: "8px",
            }}
          >
            <CalendarHeatmap
              startDate={
                new Date(
                  new Date().getFullYear() - 1,
                  new Date().getMonth(),
                  new Date().getDate()
                )
              }
              endDate={new Date()}
              values={heatmapData}
              classForValue={(value) => {
                if (!value || value.count === 0) {
                  return "color-empty";
                }
                if (value.count < 4) {
                  return "color-scale-1";
                }
                if (value.count < 8) {
                  return "color-scale-2";
                }
                if (value.count < 12) {
                  return "color-scale-3";
                }
                return "color-scale-4";
              }}
              tooltipDataAttrs={(value) => {
                return {
                  "data-tip": `${value.date}: ${value.count} contribution${
                    value.count !== 1 ? "s" : ""
                  }`,
                };
              }}
              showWeekdayLabels={true}
            />
          </div>

          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              marginTop: "20px",
              fontSize: "0.9rem",
              color: "#666",
            }}
          >
            <span style={{ marginRight: "10px" }}>Less</span>
            <div style={{ display: "flex", gap: "2px" }}>
              {[0, 1, 2, 3, 4].map((level) => (
                <div
                  key={level}
                  style={{
                    width: "12px",
                    height: "12px",
                    backgroundColor:
                      level === 0
                        ? "#ebedf0"
                        : level === 1
                        ? "#9be9a8"
                        : level === 2
                        ? "#40c463"
                        : level === 3
                        ? "#30a14e"
                        : "#216e39",
                    border: "1px solid rgba(27,31,35,0.06)",
                    borderRadius: "2px",
                  }}
                />
              ))}
            </div>
            <span style={{ marginLeft: "10px" }}>More</span>
          </div>
        </div>
      )}

      <style jsx>{`
        .react-calendar-heatmap .color-empty {
          fill: #ebedf0;
        }
        .react-calendar-heatmap .color-scale-1 {
          fill: #9be9a8;
        }
        .react-calendar-heatmap .color-scale-2 {
          fill: #40c463;
        }
        .react-calendar-heatmap .color-scale-3 {
          fill: #30a14e;
        }
        .react-calendar-heatmap .color-scale-4 {
          fill: #216e39;
        }
      `}</style>
    </div>
  );
};

export default HeatmapViewer;
