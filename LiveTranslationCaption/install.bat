@echo off
REM Installation script for LiveTranslationCaption

echo ============================================
echo Installing LiveTranslationCaption Dependencies...
echo ============================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Create virtual environment (optional)
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing required packages...
pip install -r requirements.txt

echo.
echo ============================================
echo Installation complete!
echo ============================================
echo.
echo To run the application:
echo   1. Activate the virtual environment: venv\Scripts\activate.bat
echo   2. Run: python src\main.py
echo   OR simply run: run.bat
echo.
echo Don't forget to enable Stereo Mix in Windows audio settings!
echo.
pause
