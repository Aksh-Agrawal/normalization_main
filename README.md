# Coding Profile Analyzer

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![React](https://img.shields.io/badge/React-18.2.0-61dafb)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.3.2-38bdf8)
![Last Updated](https://img.shields.io/badge/last%20updated-June%2017%2C%202023-brightgreen)

A comprehensive full-stack web application that analyzes coding profiles from various competitive programming platforms and provides a unified rating system with intelligent metrics.

> 🚀 **Latest Update**: Added smarter rating imputation system for handling missing platform data and Tailwind CSS for modern UI.

## ✨ Features

- ⚙️ **Multi-Platform Analysis**: Analyze profiles from Codeforces, LeetCode, CodeChef, and more
- 📊 **Unified Rating System**: Calculate a standardized rating across different platforms using advanced normalization algorithms
- 🧠 **Smart Rating Imputation**: Automatically estimates missing platform ratings based on user's performance on other platforms
- 🎓 **Course Bonus Calculator**: Add bonus points based on Coursera course completions considering institution reputation, course difficulty, and more
- 📈 **Activity Visualization**: View your coding activity through interactive GitHub-style heatmaps
- 🔌 **API Integration**: Seamless integration with various platform APIs
- 🕸️ **Web Scraping**: Extract data from platforms without public APIs
- 🔄 **Automatic Updates**: System adapts to platform rating changes and algorithm updates
- 🎨 **Modern UI**: Responsive and clean interface built with React and Tailwind CSS

## Project Structure

```
normalization_main/
├── README.md               # Project documentation
├── improve.md              # Future improvements list
├── start.bat               # Windows batch file to start the application
├── backend/                # Flask backend application
│   ├── main.py             # Main application entry point
│   ├── dockerfile          # Docker configuration for containerization
│   ├── requirements.txt    # Python dependencies
│   ├── bonus_calculatorF/  # Coursera certificate bonus calculation system
│   │   └── bonus_calculator.py  # Advanced bonus point calculation algorithms
│   ├── cousera/            # Coursera profile data scraping modules
│   │   ├── coursera_mock_data.py         # Mock data for testing
│   │   ├── coursera_scraper_utils.py     # Utility functions for scraping
│   │   ├── coursera_scraper_wrapper.py   # Wrapper for easy integration
│   │   ├── coursera_scraper.py           # Main scraper implementation
│   │   ├── friendly_scraper.py           # User-friendly interface for scraping
│   │   ├── handle_url_scraper.py         # URL handling and validation
│   │   ├── interactive_coursera_scraper.py  # Interactive command-line scraper
│   │   ├── interactive_scraper.py        # General interactive scraper
│   │   ├── run_coursera_scraper.py       # Runner script for coursera scraper
│   │   ├── run.py                        # Main execution script
│   │   └── simple_scraper.py             # Simplified scraper implementation
│   ├── heatmap/            # Activity visualization system
│   │   └── heat_map.py     # GitHub-style heatmap generation for coding activity
│   ├── logic_formulas/     # Core rating normalization logic
│   │   ├── formula_main.py         # Unified rating system implementation
│   │   └── ranking_platform.py     # Platform-specific normalization formulas
│   └── rating_scraper_api/ # Platform APIs for fetching user ratings
│       ├── CodeChef_api.py   # CodeChef API integration
│       ├── CodeForces_api.py # Codeforces API integration
│       └── leetcode_api.py   # LeetCode API integration
├── frontend/              # React frontend application
│   ├── src/               # Source code
│   │   ├── App.js(x)      # Main application component
│   │   ├── index.js(x)    # Entry point
│   │   ├── index.css      # Global styles with Tailwind directives
│   │   └── components/    # React components
│   │       ├── ProfileAnalyzer.jsx    # Profile analysis form
│   │       ├── ProfileViewer.jsx      # Profile data display
│   │       ├── HeatmapViewer.jsx      # Activity heatmap visualization
│   │       └── Results.jsx            # Analysis results display
│   ├── public/            # Static files
│   ├── tailwind.config.js # Tailwind CSS configuration
│   ├── postcss.config.js  # PostCSS configuration
│   └── package.json       # Frontend dependencies and scripts
```

## 🔍 Demo

![Demo Screenshot](https://via.placeholder.com/800x450.png?text=Coding+Profile+Analyzer+Demo)

### Sample Output

```json
{
  "user_id": "codingmaster",
  "unified_rating": 2485.75,
  "course_bonus": 150.5,
  "total_rating": 2636.25,
  "platform_breakdown": {
    "Codeforces": 2100,
    "Leetcode": 2700,
    "CodeChef": 1950
  },
  "ranking_position": 1,
  "percentile": 99.8,
  "activity_score": 87.5
}
```

## Technologies Used

### 🔧 Backend

| Technology        | Version | Purpose                                          |
| ----------------- | ------- | ------------------------------------------------ |
| Python            | 3.11    | Core programming language                        |
| Flask             | 3.0.0   | Web framework for the backend API                |
| Flask-CORS        | 4.0.0   | Cross-origin resource sharing support            |
| BeautifulSoup4    | 4.10.0  | HTML parsing for web scraping                    |
| Requests          | 2.31.0  | HTTP library for API calls                       |
| Pandas            | 2.2.0   | Data manipulation and analysis                   |
| NumPy             | 1.26.3  | Scientific computing and mathematical operations |
| Matplotlib        | 3.8.2   | Visualization library for heatmaps               |
| Selenium          | 4.16.0  | Automated browser interaction for web scraping   |
| WebDriver Manager | 4.0.1   | Simplified WebDriver management                  |

### 🎨 Frontend

| Technology             | Version | Purpose                                         |
| ---------------------- | ------- | ----------------------------------------------- |
| React                  | 18.2.0  | JavaScript library for building user interfaces |
| Axios                  | 1.6.0   | Promise-based HTTP client for API requests      |
| Recharts               | 2.8.0   | Composable charting library for visualizations  |
| React Calendar Heatmap | 1.9.0   | GitHub-style heatmap component                  |
| Tailwind CSS           | 3.3.2   | Utility-first CSS framework for styling         |
| PostCSS                | 8.4.24  | Tool for transforming CSS with JavaScript       |
| Autoprefixer           | 10.4.14 | Plugin to parse CSS and add vendor prefixes     |
| Vite                   | 6.3.5   | Next-generation frontend build tool             |

### Key Components

#### Unified Ranking System (URS)

- Advanced algorithm for normalizing ratings across different platforms
- Dynamic weight calculation based on platform difficulty, participation, and drift
- Adaptive temporal decay for rating relevance
- Intelligent missing rating imputation when user enters "N/A" for a platform

#### Coursera Bonus Calculator

- Institution reputation scoring based on global rankings
- Course duration and intensity evaluation
- Topic relevance and industry demand assessment
- Skills market value analysis
- Difficulty and specialization level consideration
- Integrated with the coursera scraper for automatic bonus calculation

#### Activity Visualization

- GitHub-style heatmaps for coding activity
- Aggregated multi-platform activity visualization
- Temporal analysis of coding frequency
- Interactive UI with custom data filtering options

## 🚀 Setup and Installation

### Prerequisites

| Requirement | Version            |
| ----------- | ------------------ |
| Python      | 3.8 or higher      |
| Node.js     | 14.0 or higher     |
| npm/yarn    | Latest             |
| Web browser | Any modern browser |

### Quick Start Guide

#### Method 1: Using start.bat (Windows)

```bash
# Simply double-click on start.bat or run:
start.bat
```

#### Method 2: Manual Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/normalization_main.git
   cd normalization_main
   ```

2. **Set up backend**:

   ```bash
   # Set up virtual environment (recommended)
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate

   # Install dependencies
   cd backend
   pip install -r requirements.txt

   # Start the backend server
   python main.py
   ```

3. **Set up frontend**:

   ```bash
   cd ../frontend

   # Install dependencies
   npm install

   # Start the frontend development server
   npm run dev
   ```

   The frontend server will start running on `http://localhost:5000`.

#### Method 3: Docker Deployment

```bash
# Build the Docker image
cd backend
docker build -t coding-profile-analyzer .

# Run the container
docker run -p 8000:8000 coding-profile-analyzer

# Access the API at http://localhost:8000
```

## 📘 Usage Guide

### API Reference

| Endpoint   | Method | Description             |
| ---------- | ------ | ----------------------- |
| `/`        | GET    | Welcome message         |
| `/analyze` | POST   | Analyze coding profiles |

### Detailed API Documentation

#### 1. Welcome Endpoint

```
GET /
```

**Response:**

```json
{
  "message": "Welcome to the Starization API!"
}
```

#### 2. Profile Analysis Endpoint

```
POST /analyze
```

**Request Body:**

```json
{
  "codeforces": "tourist",
  "leetcode": "tourist",
  "codechef": "tourist",
  "coursera_url": "https://www.coursera.org/account/accomplishments/professional-cert/XXXXXXXX"
}
```

**Response:**

```json
{
  "user_id": "tourist",
  "unified_rating": 3145.75,
  "course_bonus": 220.5,
  "total_rating": 3366.25,
  "platform_breakdown": {
    "Codeforces": 3800,
    "Leetcode": 3200,
    "CodeChef": 2600
  },
  "ranking_position": 1
}
```

### Example Usage

#### Using cURL

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "codeforces": "tourist",
    "leetcode": "tourist",
    "codechef": "tourist"
  }'
```

#### Using Python Requests

```python
import requests
import json

url = "http://localhost:8000/analyze"
data = {
    "codeforces": "tourist",
    "leetcode": "tourist",
    "codechef": "tourist"
}

response = requests.post(url, json=data)
print(json.dumps(response.json(), indent=2))
```

#### Using the Web Interface

1. Open the web interface at `http://localhost:5000`
2. Enter your platform usernames in the designated fields
3. Optionally add a Coursera certificate URL for bonus points
4. Click "Analyze Profile" to see your unified rating and visualization

## 🧮 Rating Normalization Algorithm

The unified rating system employs a sophisticated normalization algorithm developed through extensive research and testing:

### Core Algorithm Components

| Component       | Description                                                  | Formula                                                       |
| --------------- | ------------------------------------------------------------ | ------------------------------------------------------------- |
| Platform Weight | Dynamic weight based on difficulty, participation, and drift | `w_raw = α * difficulty + β * participation + γ * drift`      |
| Softmax Weights | Converted to probability distribution                        | `w_soft = exp(w_raw) / Σ(exp(w_raw))`                         |
| Temporal Decay  | Weight adjustment based on data freshness                    | `w_final = w_soft * e^(-λ * Δt)`                              |
| Missing Rating  | Intelligent estimation for missing data                      | Average of user's other platform ratings                      |
| Unified Rating  | Final weighted calculation                                   | `unified_rating = Σ(w_final * platform_ratings) / Σ(w_final)` |

### Algorithmic Flow

1. **Platform Weight Calculation**:

   ```python
   raw_weight = (alpha * platform.difficulty +
                beta * platform.participation +
                gamma * platform.drift)
   ```

2. **Temporal Decay Application**:

   ```python
   final_weight = softmax_weight * math.exp(-decay_lambda * days_since_update)
   ```

3. **Missing Rating Imputation**:

   ```python
   if not user_rating or user_rating == 'N/A':
       return mean([user_other_platform_ratings]) or mean([platform_historical_ratings])
   ```

4. **Unified Rating Calculation**:
   ```python
   unified_rating = sum([weight * rating for weight, rating in zip(weights, ratings)]) / sum(weights)
   ```

## 🎓 Coursera Bonus System

The system employs a comprehensive course evaluation algorithm to award bonus points based on multiple weighted factors:

| Factor                        | Weight | Examples                                                   |
| ----------------------------- | ------ | ---------------------------------------------------------- |
| **Institution Reputation**    | High   | Stanford: 10.0, Harvard: 10.0, MIT: 10.0                   |
|                               | Medium | UC Berkeley: 8.8, Georgia Tech: 8.5                        |
|                               | Lower  | Regional Universities: 5.0-7.0                             |
| **Course Difficulty**         | High   | Advanced ML: 2.5x, Quantum Computing: 2.5x                 |
|                               | Medium | Web Development: 1.5x, Data Structures: 1.8x               |
|                               | Lower  | Introductory Courses: 1.0x                                 |
| **Course Length**             |        | 4-8 week courses: 1.0x                                     |
|                               |        | 8-12 week courses: 1.5x                                    |
|                               |        | 12+ week courses: 2.0x                                     |
| **Topic Relevance**           | High   | Programming, Algorithms, AI: 2.0x                          |
|                               | Medium | Mathematics, Data Science: 1.5x                            |
|                               | Lower  | General Topics: 1.0x                                       |
| **Specialization Completion** |        | Additional 50% bonus for completing entire specializations |

### Bonus Calculation Formula

```
total_bonus = Σ(institution_score * course_difficulty * topic_relevance * length_modifier) * specialization_multiplier
```

## 🔮 Planned Improvements

| Feature                     | Description                                               | Status          |
| --------------------------- | --------------------------------------------------------- | --------------- |
| **"N/A" Username Handling** | Automatic rating estimation when user enters "N/A"        | In Progress     |
| **Coursera Integration**    | Improved integration between scraper and bonus calculator | In Progress     |
| **UI Enhancement**          | Complete Tailwind CSS migration for all components        | In Progress     |
| **Platform Expansion**      | Support for AtCoder, HackerRank, and TopCoder             | Planned Q3 2023 |
| **Machine Learning Model**  | Enhanced rating prediction using ML algorithms            | Planned Q4 2023 |
| **Real-time Updates**       | Live tracking of rating changes                           | Planned Q4 2023 |
| **Advanced Visualization**  | Interactive comparison charts and progress tracking       | Planned Q3 2023 |
| **Contest Recommender**     | Suggest suitable contests based on user's profile         | Future Plan     |

## 👨‍💻 Contributing

We welcome contributions from developers of all skill levels! Here's how to get started:

1. 🍴 **Fork the repository**
2. 🌿 **Create your feature branch**:
   ```
   git checkout -b feature/amazing-feature
   ```
3. 💾 **Commit your changes**:
   ```
   git commit -m 'Add some amazing feature'
   ```
4. 📤 **Push to the branch**:
   ```
   git push origin feature/amazing-feature
   ```
5. 🔄 **Open a Pull Request**

### Code Style Guidelines

- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript/React code
- Include docstrings and comments for all functions and classes
- Add unit tests for new features
- Keep functions small and focused
- Use Tailwind CSS for styling frontend components

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔑 Keywords

`competitive programming`, `coding profiles`, `rating normalization`, `algorithm`, `Codeforces`, `LeetCode`, `CodeChef`, `Coursera`, `web scraping`, `API integration`, `unified rating`, `Python`, `Flask`, `React`, `Tailwind CSS`, `data analysis`, `heatmap visualization`, `bonus calculator`, `profile analyzer`, `programming achievements`, `developer metrics`

## 📞 Contact & Support

- 💬 **GitHub Issues**: [Open an issue](https://github.com/yourusername/normalization_main/issues) for bug reports and feature requests

---

<div align="center">
Created with ❤️ for competitive programmers worldwide.
<br>
© 2023 Coding Profile Analyzer | Last Updated: June 17, 2023
</div>
