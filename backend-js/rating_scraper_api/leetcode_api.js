
const axios = require('axios');

async function fetchLeetCodeProfile(username) {
  const apiUrl = 'https://leetcode.com/graphql/';
  const headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Referer': `https://leetcode.com/${username}/`,
    'Origin': 'https://leetcode.com'
  };

  const query = `
    query getUserProfile($username: String!) {
      userContestRanking(username: $username) {
        attendedContestsCount
        rating
        globalRanking
      }
      matchedUser(username: $username) {
        profile {
          realName
        }
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
        tagProblemCounts {
          advanced {
            tagName
            problemsSolved
          }
          intermediate {
            tagName
            problemsSolved
          }
          fundamental {
            tagName
            problemsSolved
          }
        }
      }
    }
  `;

  const variables = { username };

  try {
    const response = await axios.post(apiUrl, 
      { query, variables },
      { headers, timeout: 10000 }
    );

    if (response.status !== 200) {
      return { error: `API Error: HTTP ${response.status}` };
    }

    const data = response.data;
    
    if (data.errors) {
      return { error: 'User not found' };
    }

    const profile = data.data.matchedUser;
    const contest = data.data.userContestRanking || {};

    // Process solved problems
    const solved = {};
    profile.submitStats.acSubmissionNum.forEach(s => {
      solved[s.difficulty] = s.count;
    });

    return {
      rating: contest.rating || 'N/A',
      username
    };

  } catch (error) {
    if (error.code === 'ECONNABORTED') {
      return { error: 'Connection timeout' };
    }
    return { error: `Unexpected error: ${error.message}` };
  }
}

function printProfile(profile) {
  if (profile.error) {
    console.log(`Error: ${profile.error}`);
    return;
  }

  const rating = typeof profile.rating === 'number' ? 
    `Contest Rating: ${profile.rating.toFixed(2)}` : 
    `Contest Rating: ${profile.rating}`;
  console.log(rating);
}

module.exports = { fetchLeetCodeProfile, printProfile };
