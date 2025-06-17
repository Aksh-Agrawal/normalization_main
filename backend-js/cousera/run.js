
const { scrapeCoureraProfile } = require('./coursera_scraper');
const bonusCalculator = require('../bonus_calculatorF/bonus_calculator');

async function runInteractive(profileUrl) {
  try {
    console.log("\n=== Coursera Profile Analyzer ===");
    console.log("This tool extracts information from public Coursera profiles");
    console.log("and calculates bonus points for each course based on multiple factors.");
    
    // Run the scraper to get profile data
    const profileData = await runScraper(profileUrl);
    
    if (profileData) {
      // Calculate bonus points
      console.log("\n=== Calculating Bonus Points ===");
      console.log("Analyzing courses for their career value and market relevance...");
      const enhancedData = bonusCalculator.calculateFromScraperResult(profileData);
      
      // Print bonus summary
      bonusCalculator.printBonusSummary(enhancedData);
      
      console.log("\nThank you for using the Coursera Profile Analyzer!");
      return enhancedData;
    }
    
  } catch (error) {
    console.error("Error during analysis:", error.message);
    return null;
  }
}

async function runScraper(profileUrl) {
  const { scrapeCoureraProfile, validateCoureraUrl } = require('./coursera_scraper');
  
  try {
    console.log("\n=== Coursera Profile Scraper ===");
    
    let url = profileUrl.trim();
    
    // If empty, use demo profile
    if (!url) {
      url = "https://www.coursera.org/user/example123";
      console.log(`Using demo profile: ${url}`);
    }
    
    let useMock = url.includes("example123");
    
    // Validate URL
    if (!validateCoureraUrl(url)) {
      console.log(`\nInvalid Coursera profile URL: ${url}`);
      url = "https://www.coursera.org/user/example123";
      console.log(`Using demo profile: ${url}`);
      useMock = true;
    }
    
    // Scrape the profile
    console.log(`\nScraping profile: ${url}...`);
    const result = await scrapeCoureraProfile(url, useMock);
    
    // Display basic profile info
    console.log("\nProfile successfully scraped!");
    if (result.user_info && result.user_info.name) {
      console.log(`User: ${result.user_info.name}`);
    }
    
    if (result.completed_courses) {
      console.log(`Courses found: ${result.completed_courses.length}`);
    }
    
    return result;
  } catch (error) {
    console.error("Error during scraping:", error.message);
    // If there's an error, return mock data for the demo profile
    console.log("Using demo profile due to error");
    return await scrapeCoureraProfile("https://www.coursera.org/user/example123", true);
  }
}

module.exports = { runInteractive, runScraper };
