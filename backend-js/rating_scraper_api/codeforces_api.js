
const axios = require('axios');

async function fetchCodeForcesProfile(handle) {
  const url = `https://codeforces.com/api/user.info?handles=${handle}`;
  const headers = {
    'User-Agent': 'Mozilla/5.0'
  };

  try {
    const response = await axios.get(url, { headers, timeout: 10000 });
    const data = response.data;
    
    if (data.status !== 'OK') {
      console.log(`API error: ${data.comment || 'Unknown error'}`);
      return { error: data.comment || 'Unknown error', rating: 'N/A', handle };
    }
    
    const user = data.result[0];
    return {
      rating: user.rating ? user.rating.toString() : 'N/A',
      handle,
      rank: user.rank || 'N/A',
      maxRating: user.maxRating ? user.maxRating.toString() : 'N/A'
    };
  } catch (error) {
    console.error(`Error fetching profile via API: ${error.message}`);
    return { error: error.message, rating: 'N/A', handle };
  }
}

function printProfile(profile) {
  if (!profile) {
    console.log("Unable to fetch Codeforces profile.");
  } else {
    console.log(`Codeforces Rating: ${profile.rating}`);
  }
}

module.exports = { fetchCodeForcesProfile, printProfile };
