# Coding Profile Analyzer

A comprehensive Python-based web application that analyzes coding profiles from various competitive programming platforms (Codeforces, LeetCode, CodeChef) and calculates a unified normalized rating. The system also features course bonus calculation from Coursera profiles and displays coding activity through interactive heatmaps.

## Features

- **Multi-Platform Analysis**: Analyze profiles from Codeforces, LeetCode, CodeChef, and more
- **Unified Rating System**: Calculate a standardized rating across different platforms using advanced normalization algorithms
- **Smart Rating Imputation**: Automatically estimates missing platform ratings based on user's performance on other platforms
- **Course Bonus Calculator**: Add bonus points based on Coursera course completions considering institution reputation, course difficulty, and more
- **Activity Visualization**: View your coding activity through interactive GitHub-style heatmaps
- **API Integration**: Seamless integration with various platform APIs
- **Web Scraping**: Extract data from platforms without public APIs

## Project Structure

```
normalization_main/
├── README.md               # Project documentation
├── improve.md              # Future improvements list
├── start.bat               # Windows batch file to start the application
├── backend/                # Main Flask backend application
│   ├── app.py              # Flask application entry point
│   ├── dockerfile          # Docker configuration for containerization
│   ├── main.py             # Secondary application entry point
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
```

## Technologies Used

### Backend

- **Python 3.11**: Core programming language
- **Flask 3.0.0**: Web framework for the backend API
- **Flask-CORS 4.0.0**: Cross-origin resource sharing support
- **BeautifulSoup4 4.10.0**: HTML parsing for web scraping
- **Requests 2.31.0**: HTTP library for API calls
- **Pandas 2.2.0**: Data manipulation and analysis
- **NumPy 1.26.3**: Scientific computing and mathematical operations
- **Matplotlib 3.8.2**: Visualization library for heatmaps
- **Selenium 4.16.0**: Automated browser interaction for web scraping
- **WebDriver Manager 4.0.1**: Simplified WebDriver management

### Key Components

#### Unified Ranking System (URS)

- Advanced algorithm for normalizing ratings across different platforms
- Dynamic weight calculation based on platform difficulty, participation, and drift
- Adaptive temporal decay for rating relevance
- Intelligent missing rating imputation

#### Coursera Bonus Calculator

- Institution reputation scoring based on global rankings
- Course duration and intensity evaluation
- Topic relevance and industry demand assessment
- Skills market value analysis
- Difficulty and specialization level consideration

#### Activity Visualization

- GitHub-style heatmaps for coding activity
- Aggregated multi-platform activity visualization
- Temporal analysis of coding frequency

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Web browser with JavaScript enabled

### Backend Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/normalization_main.git
cd normalization_main
```

2. Navigate to the backend directory:

```bash
cd backend
```

3. Install required Python packages:

```bash
pip install -r requirements.txt
```

4. Start the Flask server:

```bash
python app.py
```

The backend server will start running on `http://localhost:8000`.

### Quick Start (Windows)

For Windows users, you can simply run the included batch file:

```bash
start.bat
```

### Docker Setup

A Dockerfile is included for containerized deployment:

```bash
cd backend
docker build -t coding-profile-analyzer .
docker run -p 8000:8000 coding-profile-analyzer
```

## Usage

### API Endpoints

#### `GET /`

- Returns a welcome message
- Response: `{"message": "Welcome to the Starization API!"}`

#### `POST /analyze`

- Analyzes user profiles from multiple platforms
- Request Body:
  ```json
  {
    "codeforces": "your_cf_handle",
    "leetcode": "your_lc_handle",
    "codechef": "your_cc_handle",
    "coursera_url": "https://www.coursera.org/account/accomplishments/professional-cert/XXXXXXXX"
  }
  ```
- Response:
  ```json
  {
    "user_id": "your_handle",
    "unified_rating": 2145.75,
    "course_bonus": 120.5,
    "total_rating": 2266.25,
    "platform_breakdown": {
      "Codeforces": 1800,
      "Leetcode": 2200,
      "CodeChef": 1600
    },
    "ranking_position": 1
  }
  ```

### Example Usage

1. Start the backend server
2. Make an API request to analyze a user's profile:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "codeforces": "tourist",
    "leetcode": "tourist",
    "codechef": "tourist"
  }'
```

3. Review the normalized rating and breakdown
4. For coursera bonus points, include a valid Coursera profile URL in the request

## Rating Normalization Algorithm

The unified rating system employs a sophisticated normalization algorithm that:

1. **Platform Weight Calculation**: Computes dynamic weights for each platform based on:

   - Difficulty (α): Platform's perceived difficulty level
   - Participation (β): Popularity and community engagement
   - Drift (γ): Rating stability over time

2. **Temporal Decay**: Applies exponential decay to platform weights based on data recency:

   ```
   final_weight = softmax_weight * e^(-λ * Δt)
   ```

3. **Missing Rating Imputation**: Intelligently estimates missing platform ratings using:

   - User's ratings on other platforms
   - Historical platform averages

4. **Unified Rating Calculation**: Computes weighted average of normalized ratings:
   ```
   unified_rating = Σ(platform_weights * platform_ratings) / Σ(platform_weights)
   ```

## Coursera Bonus System

The system awards bonus points for completed Coursera courses based on:

- **Institution Reputation**: Prestigious universities (like Stanford, MIT, Harvard) yield higher bonuses
- **Course Difficulty**: Technical and specialized courses provide higher bonuses
- **Course Length**: Longer and more intensive courses are weighted higher
- **Topic Relevance**: Courses relevant to programming and computer science boost ratings more
- **Specialization Completion**: Completing entire specializations provides additional points

## Planned Improvements

- Automatic rating estimation when user enters "N/A" in username field
- Improved integration between Coursera scraper and bonus calculator
- Support for additional platforms (AtCoder, HackerRank, etc.)
- UI improvements and mobile responsiveness

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Keywords

competitive programming, coding profiles, rating normalization, algorithm, Codeforces, LeetCode, CodeChef, Coursera, web scraping, API integration, unified rating, Python, Flask, data analysis, heatmap visualization, bonus calculator

## Contact

For questions or feedback, please open an issue on the GitHub repository.
