
const axios = require('axios');
const cheerio = require('cheerio');

async function fetchCodeChefProfile(username) {
  const url = `https://www.codechef.com/users/${username}`;
  const headers = {
    'User-Agent': 'Mozilla/5.0'
  };
  
  try {
    const response = await axios.get(url, { headers, timeout: 10000 });
    
    if (response.status !== 200) {
      return { error: `Failed to fetch profile. HTTP ${response.status}` };
    }
    
    const html = response.data;
    const $ = cheerio.load(html);
    
    // Rating
    const ratingElement = $(".rating-number");
    const rating = ratingElement.length ? ratingElement.text().trim() : "N/A";

    // Stars
    const starsElement = $("span.rating");
    const stars = starsElement.length ? starsElement.text().trim() : "N/A";

    // Global Rank
    let globalRank = "N/A";
    $('td').each((i, elem) => {
      if ($(elem).text().includes("Global Rank")) {
        const nextTd = $(elem).next('td');
        if (nextTd.length) {
          globalRank = nextTd.text().trim();
        }
      }
    });

    // Fully Solved
    let fullySolved = "N/A";
    const fullySolvedMatch = html.match(/Fully Solved\s*\((\d+)\)/);
    if (fullySolvedMatch) {
      fullySolved = fullySolvedMatch[1];
    }

    const activityMap = extractActivityHeatmap(html, $);

    return {
      username,
      rating,
      stars,
      global_rank: globalRank,
      fully_solved: fullySolved,
      activity_map: activityMap
    };
  } catch (error) {
    if (error.code === 'ECONNABORTED') {
      return { error: 'Connection timeout' };
    }
    return { error: `Unexpected error: ${error.message}` };
  }
}

function extractActivityHeatmap(html, $ = null) {
  if (!$) {
    $ = cheerio.load(html);
  }

  const activityGrid = {};

  try {
    $('svg rect[data-date]').each((i, rect) => {
      const date = $(rect).attr('data-date');
      const count = parseInt($(rect).attr('data-count') || '0');
      const level = parseInt($(rect).attr('data-level') || '0');
      if (date) {
        activityGrid[date] = { count, level };
      }
    });

    if (Object.keys(activityGrid).length === 0) {
      return { error: 'No activity data found' };
    }

    return {
      cells: activityGrid
    };
  } catch (error) {
    return { error: `Heatmap extraction error: ${error.message}` };
  }
}

function printCodeChefProfile(profile) {
  if (profile.error) {
    console.log(`\nError: ${profile.error}`);
    return;
  }

  console.log(`\n👤 CodeChef Profile: @${profile.username}`);
  console.log(`⭐ Rating        : ${profile.rating}`);
  console.log(`🌟 Stars         : ${profile.stars}`);
  console.log(`🌍 Global Rank   : ${profile.global_rank}`);
  console.log(`✅ Fully Solved  : ${profile.fully_solved}`);

  const activityMap = profile.activity_map;
  if (!activityMap || activityMap.error) {
    console.log("\n📉 Activity Map: Not available or error in parsing.");
    return;
  }

  const cells = activityMap.cells;
  const activeDays = Object.values(cells).filter(d => d.count > 0).length;
  const totalDays = Object.keys(cells).length;
  const percent = totalDays > 0 ? (activeDays / totalDays) * 100 : 0;

  console.log("\n📊 Activity Summary:");
  console.log(`  Active Days     : ${activeDays}/${totalDays} (${percent.toFixed(1)}%)`);
}

module.exports = { fetchCodeChefProfile, extractActivityHeatmap, printCodeChefProfile };
