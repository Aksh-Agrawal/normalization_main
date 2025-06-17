
const axios = require('axios');
const cheerio = require('cheerio');

function validateCoureraUrl(url) {
  if (!url || typeof url !== 'string') {
    return false;
  }
  
  try {
    const urlObj = new URL(url);
    
    // Check if domain is coursera.org
    if (!urlObj.hostname || !urlObj.hostname.endsWith('coursera.org')) {
      return false;
    }
    
    // Check if path contains /user/ or /~
    if (!urlObj.pathname || (!urlObj.pathname.includes('/user/') && !urlObj.pathname.includes('/~'))) {
      return false;
    }
    
    return true;
  } catch (error) {
    return false;
  }
}

function generateMockData(profileUrl) {
  console.log(`Using mock data instead of scraping ${profileUrl}`);
  
  // Extract user ID from URL
  const userId = profileUrl.split('/').pop();
  
  // Generate user info
  const userInfo = {
    name: "Alex Martinez",
    bio: "Lifelong learner interested in AI, Public Health, and Cloud Computing.",
    location: "Austin, TX",
    profile_picture_url: `https://www.coursera.org/static/images/user-profiles/${Math.floor(Math.random() * 1000)}.jpg`,
    learning_info: {
      courses_completed: 21,
      specializations_completed: 2
    }
  };
  
  // Generate completed courses
  const completedCourses = [
    {
      title: "Deep Learning Specialization",
      institution: "deeplearning.ai",
      completion_date: "April 2025",
      duration: "10 weeks",
      certificate_url: "https://www.coursera.org/verify/certification/861397",
      course_url: `https://www.coursera.org/learn/${Math.floor(Math.random() * 10000)}`,
      skills: ["Deep Learning", "Neural Networks", "Machine Learning"]
    },
    {
      title: "Data Science: R Basics",
      institution: "Harvard University",
      completion_date: "December 2024",
      duration: "Approximately 24 hours",
      certificate_url: "https://www.coursera.org/verify/certification/809641",
      course_url: `https://www.coursera.org/learn/${Math.floor(Math.random() * 10000)}`,
      skills: ["R Programming", "Data Science", "Statistics"]
    },
    {
      title: "Music Production",
      institution: "Berklee College of Music",
      completion_date: "August 2023",
      duration: "4 months",
      certificate_url: "https://www.coursera.org/verify/certification/804377",
      course_url: `https://www.coursera.org/learn/${Math.floor(Math.random() * 10000)}`,
      skills: ["Music Production", "Audio Engineering", "Digital Audio Workstations"]
    }
  ];
  
  return {
    profile_url: profileUrl,
    user_info: userInfo,
    completed_courses: completedCourses,
    scraped_successfully: true,
    is_mock_data: true
  };
}

function extractUserInfo($) {
  const userInfo = {
    name: "Unknown",
    bio: null,
    location: null,
    profile_picture_url: null,
    learning_info: {
      courses_completed: 0,
      specializations_completed: 0
    }
  };
  
  try {
    // Check if profile exists
    const pageText = $.text();
    if (pageText.includes("profile you're looking for can't be found")) {
      userInfo.name = "Profile not found";
      userInfo.profile_exists = false;
      return userInfo;
    }
    
    // Extract name
    $('h1, h2, h3').each((i, elem) => {
      const text = $(elem).text().trim();
      if (text && text.length > 0) {
        const skipPhrases = ["coursera", "home", "browse", "log in", "sign in", "join", "page not found"];
        if (!skipPhrases.some(phrase => text.toLowerCase().includes(phrase))) {
          userInfo.name = text;
          return false; // break
        }
      }
    });
    
    // Extract bio
    $('p, div').slice(0, 15).each((i, elem) => {
      const text = $(elem).text().trim();
      if (text && text.length >= 20 && text.length <= 1000) {
        const skipPhrases = ["home", "sign in", "log in", "join", "browse", "for business", "copyright"];
        if (!skipPhrases.some(phrase => text.toLowerCase().includes(phrase))) {
          userInfo.bio = text;
          return false; // break
        }
      }
    });
    
    // Extract location
    $('span, small, div').slice(0, 20).each((i, elem) => {
      const text = $(elem).text().trim();
      if (text && text.length >= 3 && text.length <= 50 && text.includes(',')) {
        const skipPhrases = ["copyright", "terms", "privacy"];
        if (!skipPhrases.some(phrase => text.toLowerCase().includes(phrase))) {
          userInfo.location = text;
          return false; // break
        }
      }
    });
    
    // Extract profile picture
    $('img').slice(0, 15).each((i, elem) => {
      const src = $(elem).attr('src');
      if (src && (src.toLowerCase().includes('profile') || src.toLowerCase().includes('avatar') || src.toLowerCase().includes('user'))) {
        userInfo.profile_picture_url = src;
        return false; // break
      }
    });
    
    // Extract course count
    const textContent = $.text().toLowerCase();
    const coursePatterns = [
      /(\d+)\s*course[s]?\s*completed/,
      /completed\s*(\d+)\s*course[s]?/,
      /(\d+)\s*course[s]?\s*[\w\s]{0,20}certificate/
    ];
    
    for (const pattern of coursePatterns) {
      const match = textContent.match(pattern);
      if (match) {
        const count = parseInt(match[1]);
        if (count > 0 && count < 1000) {
          userInfo.learning_info.courses_completed = count;
          break;
        }
      }
    }
    
  } catch (error) {
    console.error("Error extracting user info:", error.message);
  }
  
  return userInfo;
}

function extractCompletedCourses($) {
  const completedCourses = [];
  
  try {
    // Method 1: Look for course sections
    const courseSections = [];
    
    $('h2, h3').each((i, elem) => {
      const text = $(elem).text();
      if (text && ['course', 'learning', 'certificate', 'completed'].some(keyword => 
        text.toLowerCase().includes(keyword))) {
        const parent = $(elem).parent();
        if (parent.length) {
          const container = parent.find('div, section').first();
          if (container.length) {
            courseSections.push(container);
          }
        }
      }
    });
    
    // If no specific sections found, try main content
    if (courseSections.length === 0) {
      const mainContent = $('main');
      if (mainContent.length) {
        courseSections.push(mainContent);
      } else {
        $('div, section').each((i, elem) => {
          if ($(elem).html().length > 1000) {
            courseSections.push($(elem));
          }
        });
      }
    }
    
    // Process each section
    courseSections.forEach(section => {
      // Look for course items
      let courseItems = section.find('div, article, li').filter((i, elem) => {
        const classes = $(elem).attr('class') || '';
        return ['course', 'card', 'item', 'listing', 'entry', 'row'].some(keyword =>
          classes.toLowerCase().includes(keyword));
      });
      
      if (courseItems.length === 0) {
        courseItems = section.find('div').filter((i, elem) => $(elem).html().length > 100);
      }
      
      courseItems.each((i, item) => {
        const $item = $(item);
        
        // Look for title
        let titleElem = null;
        $item.find('h3, h4, strong, div, span, p').slice(0, 5).each((j, candidate) => {
          const text = $(candidate).text().trim();
          if (text && text.length > 5 && text.length < 150) {
            const navTerms = ['menu', 'search', 'browse', 'login', 'sign in', 'technical skills'];
            if (!navTerms.some(term => text.toLowerCase().includes(term))) {
              titleElem = $(candidate);
              return false; // break
            }
          }
        });
        
        if (titleElem) {
          const courseData = {
            title: titleElem.text().trim(),
            institution: null,
            completion_date: null,
            duration: null,
            certificate_url: null,
            course_url: null
          };
          
          // Look for institution
          $item.find('div, span, img, p').slice(0, 5).each((j, inst) => {
            const instText = $(inst).text().trim();
            const institutionKeywords = ['university', 'institute', 'ibm', 'google', 'amazon', 'aws', 
                                      'microsoft', 'meta', 'coursera', 'deeplearning', 'stanford'];
            
            if (instText && institutionKeywords.some(keyword => instText.toLowerCase().includes(keyword))) {
              if (instText !== courseData.title) {
                courseData.institution = instText;
                return false; // break
              }
            }
          });
          
          // Look for completion date
          $item.find('div, span, p').each((j, dateElem) => {
            const text = $(dateElem).text().trim();
            const dateWords = ['completed', 'january', 'february', 'march', 'april', 'may', 'june', 
                             'july', 'august', 'september', 'october', 'november', 'december'];
            
            if (text && dateWords.some(word => text.toLowerCase().includes(word))) {
              courseData.completion_date = text.replace(/completed\s*/i, '').trim();
              return false; // break
            }
          });
          
          // Look for certificate link
          $item.find('a').each((j, link) => {
            const href = $(link).attr('href') || '';
            const linkText = $(link).text().trim().toLowerCase();
            if (href.includes('certificate') || linkText.includes('certificate') || linkText.includes('view')) {
              courseData.certificate_url = href;
              return false; // break
            }
          });
          
          // Add if not duplicate
          const isDuplicate = completedCourses.some(existing => existing.title === courseData.title);
          if (!isDuplicate) {
            completedCourses.push(courseData);
          }
        }
      });
    });
    
  } catch (error) {
    console.error("Error extracting completed courses:", error.message);
  }
  
  return completedCourses;
}

async function scrapeCoureraProfile(profileUrl, useMock = false) {
  // If using mock data, return it instead of scraping
  if (useMock) {
    console.log(`Using mock data instead of scraping ${profileUrl}`);
    return generateMockData(profileUrl);
  }
  
  // Validate the URL
  if (!validateCoureraUrl(profileUrl)) {
    console.error(`Invalid Coursera profile URL: ${profileUrl}`);
    throw new Error(`Invalid Coursera profile URL: ${profileUrl}`);
  }
  
  try {
    console.log(`Scraping profile: ${profileUrl}`);
    const response = await axios.get(profileUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.coursera.org/',
      },
      timeout: 30000
    });
    
    // Parse the HTML content
    const $ = cheerio.load(response.data);
    
    // Extract profile data
    const userInfo = extractUserInfo($);
    const completedCourses = extractCompletedCourses($);
    
    // Create the final result object
    const result = {
      profile_url: profileUrl,
      user_info: userInfo,
      completed_courses: completedCourses,
      scraped_successfully: true
    };
    
    console.log(`Successfully scraped profile for ${userInfo.name || 'Unknown User'}`);
    return result;
    
  } catch (error) {
    console.error(`Error scraping profile: ${error.message}`);
    throw new Error(`Error scraping profile: ${error.message}`);
  }
}

module.exports = { scrapeCoureraProfile, validateCoureraUrl, generateMockData };
