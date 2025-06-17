import React, { useState } from "react";
import ProfileViewer from './ProfileViewer';
import ProfileAnalyzer from './ProfileAnalyzer';
import HeatmapViewer from './HeatmapViewer';
import Results from './Results';

function App() {
  const [activeTab, setActiveTab] = useState("analyzer");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalysisComplete = (data) => {
    setResults(data);
    setActiveTab("results");
  };

  return (
    <div>
      <header>
        <h1
          style={{
            fontSize: "2.5rem",
            fontWeight: "bold",
            color: "white",
            textShadow: "2px 2px 4px rgba(0,0,0,0.3)",
            marginBottom: "10px",
          }}
        >
          🚀 Coding Profile Analyzer
        </h1>
        <p
          style={{
            fontSize: "1.2rem",
            color: "rgba(255,255,255,0.9)",
            textShadow: "1px 1px 2px rgba(0,0,0,0.3)",
          }}
        >
          Unified rating system for competitive programming platforms
        </p>
      </header>

      <nav className="tabs">
        <div
          className={`tab ${activeTab === "analyzer" ? "active" : ""}`}
          onClick={() => setActiveTab("analyzer")}
        >
          📊 Profile Analyzer
        </div>
        <div
          className={`tab ${activeTab === "heatmap" ? "active" : ""}`}
          onClick={() => setActiveTab("heatmap")}
        >
          🔥 Activity Heatmap
        </div>
        <div
          className={`tab ${activeTab === "profile" ? "active" : ""}`}
          onClick={() => setActiveTab("profile")}
        >
          👤 Profile Viewer
        </div>
        {results && (
          <div
            className={`tab ${activeTab === "results" ? "active" : ""}`}
            onClick={() => setActiveTab("results")}
          >
            📈 Results
          </div>
        )}
      </nav>

      <main>
        {activeTab === "analyzer" && (
          <ProfileAnalyzer
            onAnalysisComplete={handleAnalysisComplete}
            loading={loading}
            setLoading={setLoading}
          />
        )}

        {activeTab === "heatmap" && <HeatmapViewer />}

        {activeTab === "profile" && <ProfileViewer />}

        {activeTab === "results" && results && <Results data={results} />}
      </main>

      <footer
        style={{
          textAlign: "center",
          marginTop: "50px",
          color: "rgba(255,255,255,0.8)",
          fontSize: "0.9rem",
        }}
      >
        <p>
          Built with React & Node.js • Analyze your coding journey across
          platforms
        </p>
      </footer>
    </div>
  );
}

export default App;
