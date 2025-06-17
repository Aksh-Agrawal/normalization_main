
const axios = require('axios');
const cheerio = require('cheerio');
const moment = require('moment');

async function getLeetCodeHeatmap(username) {
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
    const response = await axios.post("https://leetcode.com/graphql", query);
    const data = response.data;

    const submissionData = data.data.matchedUser.userCalendar.submissionCalendar;
    const heatmap = {};
    
    const submissions = JSON.parse(submissionData);
    Object.entries(submissions).forEach(([timestamp, count]) => {
      const date = moment.unix(parseInt(timestamp)).format('YYYY-MM-DD');
      heatmap[date] = parseInt(count);
    });
    
    return heatmap;
  } catch (error) {
    console.log("LeetCode user not found or no data.");
    return {};
  }
}

async function getCodeForcesHeatmap(username) {
  const url = `https://codeforces.com/api/user.status?handle=${username}&from=1&count=10000`;
  
  try {
    const response = await axios.get(url);
    const data = response.data;
    
    const heatmap = {};
    if (data.status !== 'OK') {
      console.log("Codeforces user not found or error.");
      return {};
    }
    
    data.result.forEach(sub => {
      const date = moment.unix(sub.creationTimeSeconds).format('YYYY-MM-DD');
      heatmap[date] = (heatmap[date] || 0) + 1;
    });
    
    return heatmap;
  } catch (error) {
    console.log("Error fetching Codeforces data:", error.message);
    return {};
  }
}

async function getCodeChefHeatmap(username) {
  const url = `https://www.codechef.com/users/${username}`;
  
  try {
    const response = await axios.get(url);
    const $ = cheerio.load(response.data);
    
    const heatmap = {};
    
    // Look for activity data in script tags
    $('script').each((i, script) => {
      const content = $(script).html();
      if (content && content.includes('activityData')) {
        const match = content.match(/activityData\s*=\s*(\{.*?\});/s);
        if (match) {
          try {
            const data = JSON.parse(match[1]);
            data.data.forEach(entry => {
              const date = entry.date;
              const count = entry.value;
              heatmap[date] = (heatmap[date] || 0) + count;
            });
          } catch (parseError) {
            console.log("Error parsing CodeChef activity data");
          }
        }
      }
    });
    
    return heatmap;
  } catch (error) {
    console.log("CodeChef activityData not found.");
    return {};
  }
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

function generateGitHubStyleHeatmapData(heatmapData) {
  const today = moment();
  const startDate = moment().subtract(365, 'days');
  
  const dateRange = [];
  const current = moment(startDate);
  
  while (current.isSameOrBefore(today)) {
    dateRange.push(current.format('YYYY-MM-DD'));
    current.add(1, 'day');
  }
  
  const heatmapArray = dateRange.map(date => ({
    date,
    count: heatmapData[date] || 0
  }));
  
  // Calculate statistics
  const totalContributions = heatmapArray.reduce((sum, day) => sum + day.count, 0);
  const activeDays = heatmapArray.filter(day => day.count > 0).length;
  
  // Calculate streaks
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
  
  return {
    heatmapData: heatmapArray,
    stats: {
      totalContributions,
      activeDays,
      maxStreak,
      currentStreak
    }
  };
}

module.exports = {
  getLeetCodeHeatmap,
  getCodeForcesHeatmap,
  getCodeChefHeatmap,
  combineHeatmaps,
  generateGitHubStyleHeatmapData
};
