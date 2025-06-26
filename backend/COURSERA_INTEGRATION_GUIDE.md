# Coursera Integration Guide

## 🌐 New Feature: Coursera Profile Scraping

The Unified Ranking System now includes automatic Coursera profile scraping functionality that extracts course data and calculates bonus points based on multiple factors.

## ✨ Features

### 🔍 What it extracts:

- **Course Names**: Complete course titles from your Coursera profile
- **Institutions**: University/organization offering the course
- **Completion Dates**: When you completed each course
- **Automatic Bonus Calculation**: AI-powered bonus point calculation based on:
  - Institution prestige (Harvard, Stanford, MIT get higher scores)
  - Course duration and depth
  - Field relevance (AI, Data Science, Programming get higher scores)
  - Skills market value

### 📊 Bonus Point System:

- **Maximum possible**: 45 points per course
- **Institution Factor**: 0-10 points based on university ranking
- **Duration Factor**: 0-5 points based on course length
- **Field Factor**: 0-10 points based on subject relevance
- **Skills Factor**: 0-20 points based on market demand

## 🚀 How to Use

### Option 1: Using the Unified Launcher (Recommended)

```bash
start.bat
```

1. Choose option "1" for Simple Version (recommended) or "2" for Advanced Version
2. Login or register
3. Choose "2. 📚 Add Course Data"
4. Choose "1. 🌐 Scrape from Coursera profile URL"
5. Enter your Coursera profile URL (e.g., https://www.coursera.org/user/your-username)

### Option 2: Direct Python Execution

```bash
python main_simple.py
# or
python main_oop_fixed.py
```

## 📋 Requirements

### Coursera Profile Setup:

1. **Public Profile**: Your Coursera profile must be public
2. **Profile URL Format**: https://www.coursera.org/user/your-username
3. **Completed Courses**: Only completed courses with certificates are extracted

### How to Make Profile Public:

1. Go to your Coursera profile
2. Click "Edit Profile"
3. Set visibility to "Public"
4. Make sure "Certificates" section is visible

## 🎯 Example Usage

### Input:

```
Enter your Coursera profile URL: https://www.coursera.org/user/john-doe
```

### Sample Output:

```
🔄 Scraping profile: https://www.coursera.org/user/john-doe
✅ Profile successfully scraped!
👤 User: John Doe
📚 Found 3 completed courses

🔄 Calculating course bonus points...
✅ Saved: Machine Learning by Stanford University (+44.1 bonus)
✅ Saved: Deep Learning Specialization by DeepLearning.AI (+39.2 bonus)
✅ Saved: Python for Data Science by IBM (+31.5 bonus)

🎉 Successfully saved 3 courses!
💰 Total bonus points: 114.8

🏆 Top courses by bonus points:
  1. Machine Learning by Stanford University (+44.1)
  2. Deep Learning Specialization by DeepLearning.AI (+39.2)
  3. Python for Data Science by IBM (+31.5)
```

## 🔧 Troubleshooting

### Common Issues:

**"❌ Invalid Coursera profile URL"**

- Make sure URL format is: https://www.coursera.org/user/username
- Don't use course URLs or other Coursera pages

**"❌ Failed to scrape profile or no data found"**

- Check if your profile is set to public
- Verify you have completed courses with certificates
- Try again after a few minutes (rate limiting)

**"📚 No completed courses found"**

- Make sure your certificates are visible on your public profile
- Only courses with certificates are detected

### Mock Data Testing:

If you want to test the functionality without a real profile:

```python
python test_coursera_integration.py
```

## 🔄 Integration Details

### Files Modified:

- `main_simple.py`: Added Coursera scraping option to course data menu
- `main_oop_fixed.py`: Added Coursera scraping option to course data menu
- Both files now import and use:
  - `cousera.coursera_scraper.scrape_coursera_profile`
  - `cousera.coursera_scraper.validate_coursera_url`
  - `bonus_calculatorF.bonus_calculator.calculate_from_scraper_result`

### Database Storage:

Each scraped course is automatically saved to your user profile with:

- Course name
- Institution name
- Completion date
- Calculated bonus points

### Bonus Calculation:

The system uses sophisticated algorithms to evaluate:

- **Institution Prestige**: Based on global university rankings
- **Course Depth**: Estimated from duration and complexity
- **Market Relevance**: Based on current job market demands
- **Skills Value**: Weighted by industry demand and salary impact

## ✅ Recent Fixes (June 26, 2025)

### 🐛 Fixed: Course Name Extraction

- **Issue**: Courses were being saved as "Unknown Course" instead of actual course names
- **Root Cause**: Application was looking for `course.name` but scraper provided `course.title`
- **Fix**: Updated both applications to use `course.title` as primary field, with `course.name` as fallback
- **Result**: Courses now save with proper names like "Deep Learning Specialization", "Data Science: R Basics"

### 🧹 Database Cleanup

- Removed all previous "Unknown Course" entries from database
- Fresh start with proper course name handling
- Existing users can re-scrape their profiles to get correct course names

## 💡 Tips for Maximum Bonus Points

1. **Choose Prestigious Institutions**: Courses from top universities (Stanford, MIT, Harvard) get higher scores
2. **Focus on In-Demand Fields**: AI, Machine Learning, Data Science, and Programming courses score higher
3. **Complete Longer Courses**: Specializations and longer courses get higher duration bonuses
4. **Update Regularly**: Re-run the scraper as you complete new courses

## 🎉 Success Metrics

After integration, users can now:

- ✅ Extract all Coursera course data automatically
- ✅ Get intelligent bonus point calculations
- ✅ Save multiple courses with one URL
- ✅ See course rankings by value
- ✅ Integrate course achievements into unified ranking system

This feature significantly enhances the platform's ability to provide comprehensive skill assessment combining coding platform performance with educational achievements.
