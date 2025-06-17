
let totalBonusSum = 0.0;

// Institution reputation scores
const INSTITUTION_SCORES = {
  // Top Tier Universities (9-10)
  "Stanford University": 10,
  "Harvard University": 10,
  "Massachusetts Institute of Technology": 10,
  "California Institute of Technology": 10,
  "University of Oxford": 10,
  "University of Cambridge": 10,
  "ETH Zurich": 9.5,
  "Yale University": 9.5,
  "Princeton University": 9.5,
  "Imperial College London": 9,
  "University of Chicago": 9,
  "Columbia University": 9,
  "Technical University of Munich": 9,
  "National University of Singapore": 9,
  
  // Strong Universities (8-8.9)
  "University of California, Berkeley": 8.8,
  "University of California, Los Angeles": 8.5,
  "University of California": 8.5,
  "University of Michigan": 8.5,
  "Johns Hopkins University": 8.5,
  "Cornell University": 8.5,
  "University of Pennsylvania": 8.5,
  "University of Toronto": 8.3,
  "University of Washington": 8.3,
  "New York University": 8.2,
  "University of Edinburgh": 8.2,
  "University of Texas at Austin": 8.2,
  "Georgia Institute of Technology": 8.2,
  "Carnegie Mellon University": 8.8,
  "Duke University": 8.3,
  "Northwestern University": 8.2,
  "University of British Columbia": 8.0,
  "University of Illinois Urbana-Champaign": 8.0,
  
  // Top Tech Companies (8-9.5)
  "Google": 9.2,
  "Meta": 9.0,
  "OpenAI": 9.5,
  "Microsoft": 8.8,
  "Amazon Web Services": 8.5,
  "Apple": 8.6,
  "IBM": 8.3,
  "NVIDIA": 8.7,
  "Salesforce": 8.0,
  "Intel": 8.0,
  "Adobe": 8.0,
  "Oracle": 7.8,
  
  // AI/ML Specialized Organizations
  "deeplearning.ai": 9.3,
  "Hugging Face": 8.8,
  "NVIDIA Deep Learning Institute": 8.7,
  
  // Coursera Entities
  "Coursera": 6.5,
  "Coursera Project Network": 6.0,
  
  // Default for unlisted institutions
  "default": 5.5
};

// Field scores based on industry demand
const FIELD_SCORES = {
  // AI and Machine Learning (9-10)
  "artificial intelligence": 10,
  "machine learning": 10,
  "deep learning": 10,
  "neural networks": 9.8,
  "natural language processing": 9.7,
  "computer vision": 9.5,
  "reinforcement learning": 9.3,
  "generative ai": 10,
  "prompt engineering": 9.5,
  "llm": 9.8,
  "large language models": 9.8,
  "gpt": 9.5,
  "transformers": 9.6,
  
  // Data Science and Analytics (8-9.5)
  "data science": 9.5,
  "big data": 9.0,
  "data analytics": 9.0,
  "data mining": 8.7,
  "predictive analytics": 8.8,
  "business intelligence": 8.5,
  "data visualization": 8.7,
  "tableau": 8.5,
  "power bi": 8.4,
  
  // Programming and Development (7.5-9)
  "programming": 8.5,
  "software engineering": 8.7,
  "software development": 8.7,
  "web development": 8.2,
  "mobile development": 8.3,
  "app development": 8.3,
  "python": 9.0,
  "javascript": 8.5,
  "java": 8.0,
  "react": 8.5,
  "node.js": 8.3,
  
  // Cloud and Infrastructure (8.5-9.5)
  "cloud computing": 9.2,
  "aws": 9.0,
  "amazon web services": 9.0,
  "azure": 8.8,
  "google cloud": 8.8,
  "kubernetes": 9.0,
  "docker": 8.8,
  "microservices": 8.7,
  "serverless": 8.8,
  
  // Default for unlisted fields
  "default": 6.0
};

// Skill value scores
const SKILL_SCORES = {
  // AI and Machine Learning (9-10)
  "artificial intelligence": 10,
  "machine learning": 10,
  "deep learning": 10,
  "neural networks": 9.7,
  "natural language processing": 9.8,
  "nlp": 9.8,
  "computer vision": 9.5,
  "generative ai": 10,
  "large language models": 9.9,
  "llm": 9.9,
  "gpt": 9.6,
  "transformers": 9.7,
  "tensorflow": 9.2,
  "pytorch": 9.4,
  "keras": 9.1,
  "scikit-learn": 9.0,
  
  // Data Science and Analytics (8-9.5)
  "data science": 9.5,
  "data analysis": 9.0,
  "data analytics": 9.0,
  "data visualization": 8.5,
  "data mining": 8.7,
  "big data": 8.8,
  "predictive analytics": 9.0,
  "statistical analysis": 8.7,
  "business intelligence": 8.5,
  "tableau": 8.6,
  "power bi": 8.5,
  
  // Programming Languages (7.5-9.5)
  "programming": 8.5,
  "python": 9.5,
  "r programming": 8.5,
  "javascript": 9.0,
  "typescript": 9.1,
  "java": 8.5,
  "react": 9.2,
  "node.js": 9.0,
  "sql": 8.7,
  
  // Cloud Computing (8.5-9.5)
  "cloud computing": 9.2,
  "aws": 9.2,
  "azure": 9.0,
  "google cloud": 8.8,
  "docker": 9.0,
  "kubernetes": 9.2,
  
  // Default for unlisted skills
  "default": 6.0
};

function calculateCourseBonus(course) {
  const result = { ...course };
  
  let totalPoints = 0;
  const bonusBreakdown = {};
  
  // 1. Institution reputation (0-10 points)
  const institution = (course.institution || "").trim();
  const institutionScore = INSTITUTION_SCORES[institution] || INSTITUTION_SCORES["default"];
  totalPoints += institutionScore;
  bonusBreakdown.institution = institutionScore;
  
  // 2. Course duration (0-5 points)
  const duration = course.duration || "";
  let durationPoints = 0;
  
  if (typeof duration === 'string') {
    const durationLower = duration.toLowerCase();
    
    if (durationLower.includes('week')) {
      const weeks = parseInt(duration.match(/\d+/)?.[0] || '0');
      if (weeks >= 10) durationPoints = 5;
      else if (weeks >= 6) durationPoints = 4;
      else if (weeks >= 4) durationPoints = 3;
      else if (weeks >= 2) durationPoints = 2;
      else durationPoints = 1;
    } else if (durationLower.includes('month')) {
      const months = parseInt(duration.match(/\d+/)?.[0] || '0');
      if (months >= 6) durationPoints = 5;
      else if (months >= 3) durationPoints = 4;
      else if (months >= 2) durationPoints = 3;
      else durationPoints = 2;
    } else if (durationLower.includes('hour')) {
      const hours = parseInt(duration.match(/\d+/)?.[0] || '0');
      if (hours >= 40) durationPoints = 3;
      else if (hours >= 20) durationPoints = 2;
      else durationPoints = 1;
    } else {
      durationPoints = 2;
    }
  }
  
  totalPoints += durationPoints;
  bonusBreakdown.duration = durationPoints;
  
  // 3. Course topic/field (0-10 points)
  const title = (course.title || "").toLowerCase();
  let fieldPoints = 0;
  
  for (const [field, score] of Object.entries(FIELD_SCORES)) {
    if (title.includes(field)) {
      fieldPoints = Math.max(fieldPoints, score);
    }
  }
  
  if (fieldPoints === 0) {
    fieldPoints = FIELD_SCORES["default"];
  }
  
  totalPoints += fieldPoints;
  bonusBreakdown.field = fieldPoints;
  
  // 4. Skills covered (0-20 points)
  const skills = course.skills || [];
  let skillPoints = 0;
  
  if (skills.length > 0) {
    const skillScores = skills.map(skill => {
      const skillLower = skill.toLowerCase();
      return SKILL_SCORES[skillLower] || SKILL_SCORES["default"];
    });
    
    skillScores.sort((a, b) => b - a);
    const topSkills = skillScores.slice(0, Math.min(3, skillScores.length));
    const avgSkillScore = topSkills.reduce((a, b) => a + b, 0) / topSkills.length;
    
    skillPoints = avgSkillScore * 2;
  }
  
  totalPoints += skillPoints;
  bonusBreakdown.skills = skillPoints;
  
  // Calculate final bonus percentage
  const maxPossiblePoints = 45;
  const bonusPercentage = (totalPoints / maxPossiblePoints) * 100;
  
  result.bonus_points = Math.round(totalPoints * 10) / 10;
  result.bonus_percentage = Math.round(bonusPercentage * 10) / 10;
  result.bonus_breakdown = bonusBreakdown;
  
  console.log(`\nTotal Bonus Points: ${totalPoints.toFixed(1)} / ${maxPossiblePoints} (${bonusPercentage.toFixed(1)}%)`);
  console.log("Bonus Breakdown:");
  console.log(`  Institution: ${bonusBreakdown.institution.toFixed(1)}`);
  console.log(`  Duration: ${bonusBreakdown.duration.toFixed(1)}`);
  console.log(`  Field: ${bonusBreakdown.field.toFixed(1)}`);
  console.log(`  Skills: ${bonusBreakdown.skills.toFixed(1)}`);
  
  return result;
}

function calculateProfileBonus(profileData) {
  const result = { ...profileData };
  
  totalBonusSum = 0.0;
  const coursesWithBonus = [];
  
  for (const course of profileData.completed_courses || []) {
    const courseWithBonus = calculateCourseBonus(course);
    coursesWithBonus.append(courseWithBonus);
    totalBonusSum += courseWithBonus.bonus_points || 0;
  }
  
  console.log(`\nTotal Sum of All Bonus Points: ${totalBonusSum.toFixed(1)}`);
  
  coursesWithBonus.sort((a, b) => (b.bonus_points || 0) - (a.bonus_points || 0));
  result.completed_courses = coursesWithBonus;
  
  if (coursesWithBonus.length > 0) {
    const totalBonusPoints = coursesWithBonus.reduce((sum, course) => sum + (course.bonus_points || 0), 0);
    const avgBonusPoints = totalBonusPoints / coursesWithBonus.length;
    const maxBonusPoints = Math.max(...coursesWithBonus.map(course => course.bonus_points || 0));
    
    result.profile_metrics = {
      total_bonus_points: Math.round(totalBonusPoints * 10) / 10,
      average_bonus_points: Math.round(avgBonusPoints * 10) / 10,
      max_bonus_points: Math.round(maxBonusPoints * 10) / 10,
      course_count: coursesWithBonus.length
    };
  }
  
  return result;
}

function calculateFromScraperResult(profileData) {
  return calculateProfileBonus(profileData);
}

function getTotalBonusSum() {
  return totalBonusSum;
}

function printBonusSummary(profileData) {
  console.log("\n=== Coursera Profile Bonus Summary ===");
  
  const userInfo = profileData.user_info || {};
  console.log(`Profile: ${userInfo.name || 'Unknown User'}`);
  
  const metrics = profileData.profile_metrics || {};
  if (Object.keys(metrics).length > 0) {
    console.log(`\nTotal Courses: ${metrics.course_count || 0}`);
    console.log(`Total Bonus Points: ${metrics.total_bonus_points || 0}`);
    console.log(`Average Bonus Points: ${metrics.average_bonus_points || 0}`);
  }
  
  const courses = profileData.completed_courses || [];
  if (courses.length > 0) {
    console.log("\nCourses by Bonus Points:");
    courses.forEach((course, i) => {
      const title = course.title || "Unknown Course";
      const institution = course.institution || "Unknown Institution";
      const points = course.bonus_points || 0;
      const percentage = course.bonus_percentage || 0;
      console.log(`${i + 1}. ${title} (${institution})`);
      console.log(`   Bonus: ${points.toFixed(1)} points (${percentage.toFixed(1)}%)`);
    });
  }
}

module.exports = {
  calculateCourseBonus,
  calculateProfileBonus,
  calculateFromScraperResult,
  getTotalBonusSum,
  printBonusSummary,
  totalBonusSum
};
