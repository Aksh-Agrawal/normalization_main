# Coding Profile Analyzer

A web application that analyzes coding profiles from various platforms (Codeforces, LeetCode, CodeChef) and calculates a unified rating. It also features course bonus calculation from Coursera profiles and displays coding activity through heatmaps.

## Features

- **Multi-Platform Analysis**: Analyze profiles from Codeforces, LeetCode, and CodeChef
- **Unified Rating System**: Calculate a standardized rating across different platforms
- **Course Bonus Calculator**: Add bonus points based on Coursera course completions
- **Activity Visualization**: View your coding activity through interactive heatmaps
- **Responsive UI**: Modern and user-friendly interface built with React and Material UI

## Project Structure

The project consists of two main parts:

1. **Backend (Python/Flask)**: Handles data fetching, processing, and calculations
2. **Frontend (React)**: Provides the user interface

## Setup and Installation

### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Install required Python packages:

```bash
pip install -r requirements.txt
```

3. Start the Flask server:

```bash
python app.py
```

The backend server will start running on `http://localhost:5000`.

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install required Node.js packages:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

The frontend development server will start running on `http://localhost:5173`.

## Usage

1. Open your browser and navigate to `http://localhost:5173`
2. Enter your coding platform handles (Codeforces, LeetCode, CodeChef)
3. View your platform ratings and unified rating
4. Explore your coding activity through the heatmap
5. Add your Coursera profile URL for additional bonus points
6. See your final score and breakdown

## Technologies Used

### Backend

- Python
- Flask
- Web scraping libraries (BeautifulSoup, Selenium)
- Data processing (Pandas, NumPy)

### Frontend

- React
- Material UI
- Axios for API calls
- Nivo for data visualization

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
