@echo off
echo Starting Coding Profile Analyzer...

echo Starting backend server...
start cmd /k "cd backend && python app.py"

echo Starting frontend development server...
start cmd /k "cd frontend && npm run dev"

echo Services are starting. Please wait a moment...
echo Then access the application at: http://localhost:5173
pause
