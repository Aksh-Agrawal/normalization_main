
const axios = require('axios');
const moment = require('moment');
const cheerio = require('cheerio');

async function getLeetCodeHeatmap(username, useMock = false) {
  if (useMock) return generateMockHeatmap();
  if (!username) return {};

  const query = {
    query: `
      query userCalendar($username: String!) {
        matchedUser(username: $username) {
          userCalendar {
            submissionCalendar
          }
        }
      }
    `,
    variables: { username }
  };

  try {
    const response = await axios.post("https://leetcode.com/graphql", query, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      }
    });
    const submissionData = response.data?.data?.matchedUser?.userCalendar?.submissionCalendar;
    
    if (!submissionData) {
      console.log("LeetCode user not found or no data.");
      return {};
    }

    const heatmap = {};
    const submissions = JSON.parse(submissionData);
    
    Object.entries(submissions).forEach(([timestamp, count]) => {
      const date = moment.unix(parseInt(timestamp)).format('YYYY-MM-DD');
      heatmap[date] = parseInt(count);
    });
    
    return heatmap;
  } catch (error) {
    console.error("LeetCode heatmap error:", error.message);
    return {};
  }
}

async function getCodeForcesHeatmap(username, useMock = false) {
  if (useMock) return generateMockHeatmap();
  if (!username) return {};

  try {
    const response = await axios.get(`https://codeforces.com/api/user.status?handle=${username}&from=1&count=10000`, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      }
    });
    
    if (response.data?.status !== 'OK') {
      console.log("Codeforces user not found or error.");
      return {};
    }

    const submissions = response.data.result;
    const heatmap = {};

    submissions.forEach(submission => {
      const date = moment.unix(submission.creationTimeSeconds).format('YYYY-MM-DD');
      heatmap[date] = (heatmap[date] || 0) + 1;
    });

    return heatmap;
  } catch (error) {
    console.error("CodeForces heatmap error:", error.message);
    return {};
  }
}

async function getCodeChefHeatmap(username, useMock = false) {
  if (useMock) return generateMockHeatmap();
  if (!username) return {};

  try {
    const response = await axios.get(`https://www.codechef.com/users/${username}`, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
      },
      timeout: 15000
    });

    const $ = cheerio.load(response.data);
    let scriptContent = '';
    
    // Find script containing activityData
    $('script').each((i, elem) => {
      const content = $(elem).html();
      if (content && content.includes('activityData')) {
        scriptContent = content;
      }
    });

    if (!scriptContent) {
      console.log("CodeChef activityData not found.");
      return generateMockHeatmap();
    }

    // Extract activityData JSON
    const match = scriptContent.match(/activityData\s*=\s*({[\s\S]*?});/);
    if (!match) {
      console.log("CodeChef activityData parse error.");
      return generateMockHeatmap();
    }

    const data = JSON.parse(match[1]);
    const heatmap = {};

    if (data.data && Array.isArray(data.data)) {
      data.data.forEach(entry => {
        if (entry.date && entry.value) {
          heatmap[entry.date] = (heatmap[entry.date] || 0) + entry.value;
        }
      });
    }

    return heatmap;
  } catch (error) {
    console.error("CodeChef heatmap error:", error.message);
    return generateMockHeatmap();
  }
}

function generateMockHeatmap() {
  const heatmap = {};
  const startDate = moment().subtract(1, 'year');
  
  for (let i = 0; i < 365; i++) {
    const date = moment(startDate).add(i, 'days').format('YYYY-MM-DD');
    if (Math.random() > 0.5) {
      heatmap[date] = Math.floor(Math.random() * 5) + 1;
    }
  }
  
  return heatmap;
}

function combineHeatmaps(...heatmaps) {
  const combined = {};
  heatmaps.forEach(heatmap => {
    Object.entries(heatmap).forEach(([date, count]) => {
      combined[date] = (combined[date] || 0) + count;
    });
  });
  return combined;
}

module.exports = {
  getLeetCodeHeatmap,
  getCodeForcesHeatmap,
  getCodeChefHeatmap,
  generateMockHeatmap,
  combineHeatmaps
};
