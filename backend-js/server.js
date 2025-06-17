
const express = require('express');
const cors = require('cors');
const path = require('path');
const { UnifiedRankingSystem } = require('./logic_formulas/formula_main');
const { fetchCodeForcesProfile } = require('./rating_scraper_api/codeforces_api');
const { fetchLeetCodeProfile } = require('./rating_scraper_api/leetcode_api');
const { fetchCodeChefProfile } = require('./rating_scraper_api/codechef_api');
const { runInteractive } = require('./cousera/run');
const bonusCalculator = require('./bonus_calculatorF/bonus_calculator');
const heatmapUtils = require('./heatmap/heat_map');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Serve static files from the React app build directory
app.use(express.static('../frontend/build'));

// Catch all handler: send back React's index.html file for any non-API routes
app.get('*', (req, res) => {
  if (!req.path.startsWith('/api')) {
    res.sendFile(path.join(__dirname, '../frontend/build', 'index.html'));
  }
});

// Main analysis endpoint
app.post('/api/analyze-profile', async (req, res) => {
  try {
    const { codeforces, leetcode, codechef, coursera } = req.body;
    
    const rankingSystem = new UnifiedRankingSystem();
    let userId = null;

    // Add platforms
    rankingSystem.addPlatform("Codeforces", 3000);
    rankingSystem.addPlatform("Leetcode", 2500);
    rankingSystem.addPlatform("Atcoder", 2800);
    rankingSystem.addPlatform("CodeChef", 1800);

    // Process each platform
    if (codeforces) {
      const cfData = await fetchCodeForcesProfile(codeforces);
      if (cfData && cfData.rating !== 'N/A') {
        userId = codeforces;
        rankingSystem.addUser(userId);
        rankingSystem.updatePlatformStats("Codeforces", 2100, 0.8, { [userId]: parseInt(cfData.rating) });
      }
    }

    if (leetcode) {
      const lcData = await fetchLeetCodeProfile(leetcode);
      if (lcData && lcData.rating !== 'N/A') {
        if (!userId) {
          userId = leetcode;
          rankingSystem.addUser(userId);
        }
        rankingSystem.updatePlatformStats("Leetcode", 2100, 0.8, { [userId]: parseInt(lcData.rating) });
      }
    }

    if (codechef) {
      const ccData = await fetchCodeChefProfile(codechef);
      if (ccData && ccData.rating !== 'N/A') {
        if (!userId) {
          userId = codechef;
          rankingSystem.addUser(userId);
        }
        rankingSystem.updatePlatformStats("CodeChef", 3100, 0.5, { [userId]: parseInt(ccData.rating) });
      }
    }

    // Get course bonus if Coursera profile provided
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
      platformWeights: rankingSystem.finalWeights
    });

  } catch (error) {
    console.error('Error analyzing profile:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Heatmap endpoint
app.post('/api/heatmap', async (req, res) => {
  try {
    const { codeforces, leetcode, codechef } = req.body;
    
    const heatmaps = {};
    
    if (codeforces) {
      heatmaps.codeforces = await heatmapUtils.getCodeForcesHeatmap(codeforces);
    }
    
    if (leetcode) {
      heatmaps.leetcode = await heatmapUtils.getLeetCodeHeatmap(leetcode);
    }
    
    if (codechef) {
      heatmaps.codechef = await heatmapUtils.getCodeChefHeatmap(codechef);
    }
    
    const combined = heatmapUtils.combineHeatmaps(Object.values(heatmaps));
    
    res.json({
      success: true,
      heatmaps,
      combined
    });
    
  } catch (error) {
    console.error('Error generating heatmap:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});
