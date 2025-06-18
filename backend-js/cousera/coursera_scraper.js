
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
        title: 'Machine Learning Specialization',
        institution: 'Stanford University',
        completion_date: 'December 2023',
        certificate_url: 'https://coursera.org/verify/ML123'
      },
      {
        title: 'Deep Learning Specialization',
        institution: 'DeepLearning.AI',
        completion_date: 'November 2023',
        certificate_url: 'https://coursera.org/verify/DL456'
      }
    ],
    totalCourses: 2,
    scrapedAt: new Date().toISOString(),
    isMockData: true
  };
}

async function extractCoursesDirectly($) {
  const courses = [];
  const courseHeaders = [];

  // Find all potential course section headers
  $('h1, h2, h3, h4, div, span').each((_, elem) => {
    const text = $(elem).text().trim().toLowerCase();
    if (!text) return;

    if (
      (text.includes('course') || text.includes('learning') || 
       text.includes('certificate') || text.includes('completed')) &&
      !text.includes('explore') && !text.includes('browse') && 
      !text.includes('find') && !text.includes('search')
    ) {
      courseHeaders.push(elem);
    }
  });

  // If no specific headers found, try main content
  if (courseHeaders.length === 0) {
    const mainContent = $('main');
    if (mainContent.length) {
      mainContent.find('h1, h2, h3').each((_, elem) => {
        courseHeaders.push(elem);
      });
    }
  }

  // Process each course section
  courseHeaders.forEach(header => {
    let container = $(header);
    for (let i = 0; i < 3 && container.length; i++) {
      container = container.parent();
      if (!container.length) break;

      // Find potential course cards
      const cardCandidates = [];
      container.find('div, li, article').each((_, elem) => {
        const cardHtml = $(elem).html();
        if (cardHtml && cardHtml.length > 150 && cardHtml.length < 5000) {
          cardCandidates.push(elem);
        }
      });

      // Process each potential card
      cardCandidates.forEach(card => {
        let titleElem = null;
        const $card = $(card);

        // Find course title
        ['h3', 'h4', 'strong', 'div'].some(tag => {
          return $card.find(tag).each((_, elem) => {
            const text = $(elem).text().trim();
            if (text && text.length >= 10 && text.length <= 120 &&
                !text.toLowerCase().includes('menu') &&
                !text.toLowerCase().includes('search') &&
                !text.toLowerCase().includes('browse')) {
              titleElem = elem;
              return false; // break the each loop
            }
          });
        });

        if (!titleElem) return;

        const courseTitle = $(titleElem).text().trim();

        // Find institution
        let institution = null;
        $card.find('span, div, p, img').each((_, elem) => {
          let text = $(elem).text().trim();
          if (!text && elem.tagName === 'img' && $(elem).attr('alt')) {
            text = $(elem).attr('alt');
          }

          if (text && text !== courseTitle &&
              /university|institute|ibm|google|amazon|microsoft|meta|coursera/i.test(text)) {
            institution = text;
            return false;
          }
        });

        // Find completion date
        let completionDate = null;
        $card.find('span, div, p').each((_, elem) => {
          const text = $(elem).text().trim();
          if (text && (
              text.toLowerCase().includes('completed') ||
              /january|february|march|april|may|june|july|august|september|october|november|december/i.test(text)
          )) {
            completionDate = text.toLowerCase().includes('completed') ?
              text.toLowerCase().replace('completed', '').trim() : text;
            return false;
          }
        });

        // Find certificate URL
        let certificateUrl = null;
        $card.find('a').each((_, elem) => {
          const href = $(elem).attr('href');
          const linkText = $(elem).text().trim().toLowerCase();
          if (href && (
              href.toLowerCase().includes('certificate') ||
              linkText.includes('certificate') ||
              linkText.includes('view')
          )) {
            certificateUrl = href.startsWith('/') ?
              `https://www.coursera.org${href}` : href;
            return false;
          }
        });

        courses.push({
          title: courseTitle,
          institution,
          completion_date: completionDate,
          certificate_url: certificateUrl
        });
      });
    }
  });

  return courses;
}

async function scrapeCoureraProfile(url, useMock = false) {
  if (useMock) return generateMockData();
  
  if (!validateCoureraUrl(url)) {
    throw new Error('Invalid Coursera profile URL');
  }

  try {
    const response = await axios.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.coursera.org/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
      }
    });
    
    const $ = cheerio.load(response.data);
    const courses = await extractCoursesDirectly($);
    
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
