const express = require("express");
const cors = require("cors");
const path = require("path");
const { UnifiedRankingSystem } = require("./logic_formulas/formula_main");
const { fetchCodeForcesProfile } = require("./rating_scraper_api/codeforces_api");
const { fetchLeetCodeProfile } = require("./rating_scraper_api/leetcode_api");
const { fetchCodeChefProfile } = require("./rating_scraper_api/codechef_api");
const { runInteractive } = require("./cousera/run");
const bonusCalculator = require("./bonus_calculatorF/bonus_calculator");
const heatmapUtils = require("./heatmap/heat_map");

const app = express();
const PORT = process.env.PORT || 5001;

// Middleware
app.use(cors());
app.use(express.json());

// Analyze Profile Route
app.post("/api/analyze-profile", async (req, res) => {
  try {
    const { codeforces, leetcode, codechef, coursera } = req.body;

    const rankingSystem = new UnifiedRankingSystem();
    let userId = null;

    // Add platforms
    rankingSystem.addPlatform("Codeforces", 3000);
    rankingSystem.addPlatform("Leetcode", 2500);
    rankingSystem.addPlatform("Atcoder", 2800);  // Placeholder
    rankingSystem.addPlatform("CodeChef", 1800);

    // Codeforces
    if (codeforces) {
      const cfData = await fetchCodeForcesProfile(codeforces);
      if (cfData && cfData.rating !== "N/A") {
        userId = codeforces;
        rankingSystem.addUser(userId);
        rankingSystem.updatePlatformStats("Codeforces", 2100, 0.8, {
          [userId]: parseInt(cfData.rating),
        });
      }
    }

    // Leetcode
    if (leetcode) {
      const lcData = await fetchLeetCodeProfile(leetcode);
      if (lcData && lcData.rating !== "N/A") {
        if (!userId) {
          userId = leetcode;
          rankingSystem.addUser(userId);
        }
        rankingSystem.updatePlatformStats("Leetcode", 2100, 0.8, {
          [userId]: parseInt(lcData.rating),
        });
      }
    }

    // Codechef
    if (codechef) {
      const ccData = await fetchCodeChefProfile(codechef);
      if (ccData && ccData.rating !== "N/A") {
        if (!userId) {
          userId = codechef;
          rankingSystem.addUser(userId);
        }
        rankingSystem.updatePlatformStats("CodeChef", 3100, 0.5, {
          [userId]: parseInt(ccData.rating),
        });
      }
    }

    // Coursera Bonus
    let courseBonus = 0;
    if (coursera) {
      const courseData = await runInteractive(coursera);
      courseBonus = bonusCalculator.getTotalBonusSum();
    }

    // Get final rankings
    const rankings = rankingSystem.getRankings();

    res.json({
      success: true,
      userId,
      rankings,
      courseBonus,
      platformWeights: rankingSystem.finalWeights,
    });
  } catch (error) {
    console.error("Error analyzing profile:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Heatmap Route
app.post("/api/heatmap", async (req, res) => {
  try {
    const { codeforces, leetcode, codechef } = req.body;
    const useMock = !codeforces && !leetcode && !codechef;

    const heatmaps = {
      leetcode: leetcode ? await heatmapUtils.getLeetCodeHeatmap(leetcode, useMock) : {},
      codeforces: codeforces ? await heatmapUtils.getCodeForcesHeatmap(codeforces, useMock) : {},
      codechef: codechef ? await heatmapUtils.getCodeChefHeatmap(codechef, useMock) : {},
    };

    const combined = heatmapUtils.combineHeatmaps(
      heatmaps.leetcode,
      heatmaps.codeforces,
      heatmaps.codechef
    );

    res.json({
      success: true,
      leetcode: heatmaps.leetcode,
      codeforces: heatmaps.codeforces,
      codechef: heatmaps.codechef,
      combined,
    });
  } catch (error) {
    console.error("Error generating heatmap:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Serve React build
app.use(express.static(path.join(__dirname, "../frontend/build")));

// React fallback for SPA routing
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "../frontend/build/index.html"));
});

// Start server
app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server running on port ${PORT}`);
});
