
const axios = require('axios');
const cheerio = require('cheerio');

function validateCoureraUrl(url) {
  if (!url || typeof url !== 'string') return false;
  return url.includes('coursera.org/user/');
}

function generateMockData() {
  return {
    courses: [
      {
        name: 'Machine Learning Specialization',
        completion: '2023-12-15',
        grade: 'Pass with Distinction',
        certificate: 'https://coursera.org/verify/ML123'
      },
      {
        name: 'Deep Learning Specialization',
        completion: '2023-11-30',
        grade: 'Pass',
        certificate: 'https://coursera.org/verify/DL456'
      }
    ],
    totalCourses: 2,
    scrapedAt: new Date().toISOString(),
    isMockData: true
  };
}

async function scrapeCoureraProfile(url, useMock = false) {
  if (useMock) return generateMockData();
  
  if (!validateCoureraUrl(url)) {
    throw new Error('Invalid Coursera profile URL');
  }

  try {
    const response = await axios.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    
    const $ = cheerio.load(response.data);
    const courses = [];
    
    $('.course-item').each((i, elem) => {
      const course = {
        name: $(elem).find('.course-name').text().trim(),
        completion: $(elem).find('.completion-date').text().trim(),
        grade: $(elem).find('.grade').text().trim() || 'N/A',
        certificate: $(elem).find('.certificate-link').attr('href') || null
      };
      courses.push(course);
    });
    
    return {
      courses,
      totalCourses: courses.length,
      scrapedAt: new Date().toISOString(),
      isMockData: false
    };
  } catch (error) {
    console.error('Error scraping Coursera profile:', error.message);
    return null;
  }
}

module.exports = {
  scrapeCoureraProfile,
  validateCoureraUrl,
  generateMockData
};
