@echo off
cls
echo.
echo ===============================================
echo           UNIFIED RANKING SYSTEM
echo ===============================================
echo.
echo    🚀 Welcome to your personal coding tracker!
echo    Track ratings across coding platforms and
echo    calculate unified rankings with course bonuses
echo.
echo ===============================================

cd /d "%~dp0"

echo 🔍 Checking system requirements...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Python !PYTHON_VERSION! is available
)

REM Check if required packages are installed
echo 🔍 Checking required packages...
python -c "import requests, bs4, pandas, matplotlib, bcrypt, numpy" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Some required packages are missing
    echo 📦 Installing required packages...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install packages
        echo Please run: pip install -r requirements.txt
        pause
        exit /b 1
    )
) else (
    echo ✅ All packages are available
)

echo.
echo ===============================================
echo              CHOOSE YOUR VERSION
echo ===============================================
echo.
echo 1. 🔧 SIMPLE VERSION (Recommended)
echo    ✅ Visible password input (works everywhere)
echo    ✅ Auto-fetch ratings from CodeForces, LeetCode, CodeChef
echo    ✅ Coursera profile scraping with bonus calculation
echo    ✅ Unified ranking calculation and heatmap generation
echo    ✅ Course tracking and user profiles
echo.
echo 2. 🛡️ ADVANCED VERSION (Secure)
echo    ✅ Hidden password input with fallback
echo    ✅ All features from Simple Version
echo    ✅ Enhanced security features
echo.
echo 3. 📊 ORIGINAL SINGLE-USER VERSION
echo    ✅ Direct platform rating input without registration
echo    ✅ Immediate ranking calculation and heatmap
echo    ✅ Coursera bonus calculation
echo    ⚠️ No data persistence or user accounts
echo.
echo 4. ❌ EXIT
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Starting Simple Version...
    echo ℹ️ Your password will be visible when typing
    echo.
    python main_simple.py
) else if "%choice%"=="2" (
    echo.
    echo 🛡️ Starting Advanced Version...
    echo ℹ️ Password input will be hidden when possible
    echo.
    python main_oop_fixed.py
) else if "%choice%"=="3" (
    echo.
    echo 📊 Starting Original Single-User Version...
    echo ℹ️ No registration required - direct platform input
    echo.
    python main.py
) else if "%choice%"=="4" (
    echo.
    echo 👋 Thank you for using Unified Ranking System!
    exit /b 0
) else (
    echo.
    echo ❌ Invalid choice. Please enter 1, 2, 3, or 4.
    echo.
    pause
    goto :eof
)

echo.
echo ===============================================
echo           APPLICATION FINISHED
echo ===============================================
echo.
echo Thank you for using Unified Ranking System! 🎉
echo.
echo 💡 TIPS FOR NEXT TIME:
echo   • Keep your coding platform profiles public for auto-fetch
echo   • Make your Coursera profile public for course scraping  
echo   • Regular updates help maintain accurate rankings
echo.
echo 📊 FEATURES SUMMARY:
echo   ✅ Multi-platform rating tracking (CodeForces, LeetCode, CodeChef)
echo   ✅ Automatic rating fetching via web APIs
echo   ✅ GitHub-style activity heatmap generation
echo   ✅ Coursera course scraping with intelligent bonus calculation
echo   ✅ Unified ranking system with weighted platform scores
echo   ✅ User authentication and data persistence
echo.
pause
