
const { scrapeCoureraProfile } = require('./coursera_scraper');
const bonusCalculator = require('../bonus_calculatorF/bonus_calculator');

async function runInteractive(profileUrl) {
  try {
    // Determine if we should use mock data
    const useMock = !profileUrl || profileUrl.includes('example') || profileUrl.includes('demo');
    
    // Run the scraper to get profile data
    const profileData = await scrapeCoureraProfile(profileUrl, useMock);
    
    if (!profileData) {
      console.error('Failed to fetch profile data');
      return null;
    }

    // Calculate bonus points
    const enhancedData = bonusCalculator.calculateFromScraperResult(profileData);
    
    if (enhancedData) {
      console.log(`Successfully processed ${enhancedData.courses?.length || 0} courses`);
      return enhancedData;
    }

    return null;
  } catch (error) {
    console.error('Error during analysis:', error.message);
    return null;
  }
}

module.exports = { runInteractive };
