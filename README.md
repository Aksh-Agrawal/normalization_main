# 🏆 Unified Ranking System


A comprehensive coding skills assessment platform that integrates multiple programming platforms with educational achievements to provide unified rankings.
=======
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Last Updated](https://img.shields.io/badge/last%20updated-June%2017%2C%202023-brightgreen)


## 🌟 Complete Overview

The Unified Ranking System is a sophisticated Python application that revolutionizes how programmers track and assess their coding skills across multiple platforms. By combining competitive programming ratings, educational achievements, and activity patterns, it provides a holistic view of your programming prowess.

### 🎯 What It Does

- **📊 Multi-Platform Integration**: Automatically fetches ratings from CodeForces, LeetCode, CodeChef, and AtCoder
- **🎓 Educational Tracking**: Scrapes Coursera profiles to extract course completions and calculate intelligent bonus points
- **📈 Activity Visualization**: Generates GitHub-style heatmaps showing coding consistency across platforms
- **🔢 Unified Rankings**: Uses sophisticated algorithms to combine platform ratings with educational bonuses
- **👥 Multi-User Support**: Secure authentication system supporting multiple users with persistent data
- **💾 Data Persistence**: SQLite database stores all user data locally with encrypted passwords

### 🚀 Key Features

#### 🏅 Platform Rating Integration

- **CodeForces** (Max: 3000) - Competitive programming excellence
- **LeetCode** (Max: 2500) - Interview preparation mastery
- **CodeChef** (Max: 1800) - Programming contest proficiency
- **AtCoder** (Max: 2800) - Japanese competitive programming platform

**Smart Auto-Fetch System**:

- 🔄 Automatic rating retrieval via official APIs
- 🔄 Real-time data validation and error handling
- 🔄 Intelligent fallback to manual entry when needed

#### 🎓 Educational Bonus System

**Coursera Profile Scraping**:

- 📚 Automatic extraction of completed courses from public profiles
- 🏛️ Institution recognition (Harvard, Stanford, MIT get premium scores)
- 📅 Completion date tracking for timeline analysis
- 🧮 AI-powered bonus calculation based on multiple factors

**Intelligent Bonus Calculation** (Max: 45 points per course):

- **Institution Factor** (0-10): University prestige and global ranking
- **Duration Factor** (0-5): Course depth, specialization length
- **Field Factor** (0-10): Relevance to tech industry (AI, Data Science, Programming)
- **Skills Factor** (0-20): Market demand analysis and salary impact

#### 📈 Advanced Analytics

**GitHub-Style Activity Heatmaps**:

- 🟩 Daily coding activity visualization across all platforms
- 📊 Combined activity metrics from multiple sources
- 🎨 Beautiful visual progress representation
- 📅 Yearly overview with streak tracking

**Sophisticated Ranking Algorithm**:

- ⚖️ Weighted platform scores based on difficulty
- 📊 Normalized rating scales for fair comparison
- 🎯 Platform difficulty consideration in weighting
- 🎓 Seamless educational bonus integration
- 📈 Final unified ranking calculation

### 🎮 Three Application Modes

#### 1. 🔧 Simple Version (Recommended)

**Perfect for**: Beginners, most users, systems with compatibility issues

- ✅ Visible password input (universal compatibility)
- ✅ Complete feature set with intuitive interface
- ✅ Automatic platform rating fetching
- ✅ Full Coursera integration and bonus calculation
- ✅ Heatmap generation and user profiles

#### 2. 🛡️ Advanced Version (Secure)

**Perfect for**: Security-conscious users, advanced developers

- ✅ Hidden password input with enhanced security
- ✅ All Simple Version features plus security enhancements
- ✅ Advanced error handling and logging
- ✅ Object-oriented architecture for maintainability
- ✅ Enhanced data validation and sanitization

#### 3. 📊 Original Single-User Version

**Perfect for**: Quick testing, demonstration, single-session use

- ✅ No registration required - immediate access
- ✅ Direct platform input and instant calculations
- ✅ Full ranking computation and heatmap generation
- ⚠️ No data persistence between sessions
- ⚠️ Single user only (no authentication system)

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+** installed on your system
- **Internet connection** for API calls and web scraping
- **Public profiles** on coding platforms (for auto-fetch)
- **Public Coursera profile** (optional, for course bonus)

### Installation & Launch

1. **Download/Clone** this repository
2. **Navigate** to the `backend` folder
3. **Double-click** `start.bat` (Windows) or run from command line

The intelligent launcher will:

- ✅ Automatically detect Python installation
- 📦 Install required packages if missing
- 🎯 Present you with three version options
- 🛠️ Handle errors and provide guidance

## 📊 How It Works

### 🔢 Ranking Calculation

```
Total Score = (Weighted Platform Score) + (Course Bonus Points)

Where:
- Weighted Platform Score = Σ(Platform Rating × Platform Weight)
- Course Bonus Points = Σ(Individual Course Bonuses)
- Platform Weights = Dynamic based on difficulty and participation
```

### 🎓 Course Bonus Examples

- **Stanford Machine Learning**: ~40-45 points (top-tier institution + high-demand field)
- **MIT Computer Science**: ~35-40 points (prestigious institution + core programming)
- **Google Data Analytics**: ~25-30 points (industry recognition + practical skills)
- **Harvard CS50**: ~30-35 points (prestigious + comprehensive programming)

### 📈 Platform Weighting

- **Difficulty Assessment**: Harder platforms receive higher weights
- **Participation Analysis**: Active user bases get consideration
- **Rating Distribution**: Normalized across different rating scales
- **Industry Recognition**: Platform reputation in hiring processes

## 🛠️ Technical Architecture

### 🏗️ Core Components

- **Authentication System**: Secure user management with bcrypt password hashing
- **API Integration Layer**: Robust web scraping and API calls with error handling
- **Ranking Engine**: Sophisticated algorithms for unified score calculation
- **Visualization Engine**: Beautiful heatmap generation with statistical analysis
- **Data Persistence**: SQLite database with optimized queries and data integrity

### 🔧 Platform APIs

- **CodeForces API**: Official REST API for contest and user data
- **LeetCode GraphQL**: Advanced querying for comprehensive profile data
- **CodeChef Web Scraping**: Intelligent parsing with rate limiting
- **Coursera Profile Scraping**: Selenium-based extraction with mock data fallback

## 📱 User Experience Features

### 🎯 Smart Auto-Detection

- **Platform Profile Validation**: Real-time verification of usernames
- **Rating Verification**: Cross-reference with platform data
- **Course Certificate Validation**: Only certified completions count
- **Error Recovery**: Intelligent fallbacks and user guidance

### 📊 Rich Analytics

- **Progress Tracking**: Historical rating changes over time
- **Activity Patterns**: Peak coding times and consistency metrics
- **Achievement Insights**: Course completion impact on overall ranking
- **Comparative Analysis**: Performance across different platforms

### 🔒 Privacy & Security

- **Local Data Storage**: All information stays on your machine
- **No Cloud Dependencies**: Complete offline functionality
- **Encrypted Credentials**: Secure password storage with bcrypt
- **Ethical Scraping**: Respectful rate limiting and public data only

## 📚 Full Documentation

For complete setup instructions, troubleshooting, and advanced usage:

**[📖 Complete README.md](backend/README.md)**

## 📂 Project Structure

```
normalization_main/
├── backend/                        # 🎯 Main application directory
│   ├── start.bat                   # 🚀 Universal launcher
│   ├── main_simple.py             # 🔧 Simple version
│   ├── main_oop_fixed.py          # 🛡️ Advanced version
│   ├── main.py                    # 📊 Original single-user
│   ├── README.md                  # 📖 Complete documentation
│   │
│   ├── services/                  # 🏗️ Core business logic
│   │   ├── auth_service.py        #   👤 User authentication
│   │   ├── ranking_service.py     #   � Rating calculations
│   │   └── input_handlers/        #   🎮 User interface logic
│   │
│   ├── rating_scraper_api/        # 🔌 Platform integrations
│   │   ├── CodeForces_api.py      #   🟦 CodeForces API
│   │   ├── leetcode_api.py        #   🟨 LeetCode GraphQL
│   │   └── CodeChef_api.py        #   � CodeChef scraping
│   │
│   ├── cousera/                   # 🎓 Educational features
│   │   └── coursera_scraper.py    #   🕷️ Profile extraction
│   │
│   ├── bonus_calculatorF/         # 🧮 Bonus calculation
│   │   └── bonus_calculator.py    #   💰 Intelligent scoring
│   │
│   ├── heatmap/                   # 📈 Visualization
│   │   └── heat_map.py            #   🎨 GitHub-style graphs
│   │
│   ├── logic_formulas/            # 🔢 Ranking algorithms
│   │   ├── formula_main.py        #   ⚖️ Core ranking logic
│   │   └── ranking_platform.py    #   🏗️ Platform management
│   │
│   └── [additional modules]       # 🔧 Supporting functionality
│
└── README.md                      # 📄 This overview file
```

## 🎉 Success Stories & Use Cases

### 🎯 Career Development

_"Used the unified ranking to showcase my skills during job interviews. The combination of competitive programming ratings and educational certificates gave recruiters a complete picture of my abilities."_

### 📈 Progress Tracking

_"The heatmap visualization motivated me to code more consistently. Seeing my activity patterns helped me identify and fix gaps in my practice routine."_

### 🎓 Educational Impact

_"Adding my Coursera certifications boosted my ranking significantly. The intelligent bonus system recognized the value of my Stanford ML course and Google certificates."_

### 🏆 Competitive Analysis

_"Compared my performance across platforms and identified where to focus my efforts. The weighted scoring system showed that improving my CodeForces rating had the biggest impact."_

## 🚀 Getting Started

Ready to unify your coding achievements? Here's how:

### 🎯 Immediate Use

1. **Download** or clone this repository
2. **Open** the `backend` folder
3. **Run** `start.bat` (Windows) or execute from terminal
4. **Choose** your preferred version (Simple recommended for first-time users)
5. **Follow** the guided setup process

### 📊 First Steps

1. **Register** your account (Simple/Advanced versions)
2. **Add** your coding platform usernames
3. **Connect** your Coursera profile (optional but recommended)
4. **Generate** your first unified ranking
5. **Explore** heatmaps and analytics

### 🎓 Maximizing Your Score

- **Optimize Platform Performance**: Focus on platforms with higher weights
- **Strategic Course Selection**: Choose high-value courses from prestigious institutions
- **Consistent Activity**: Maintain regular coding practice for better heatmap metrics
- **Profile Optimization**: Keep platform profiles public for automatic data fetching

---

<<<<<<< HEAD
**🏆 Transform how you track and showcase your programming journey. Start building your unified coding profile today!**

**[🚀 Get Started Now - Go to Backend Folder Readme ](backend/README.md)**
=======
