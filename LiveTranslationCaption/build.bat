@echo off
REM Build script for LiveTranslationCaption Windows executable

echo ============================================
echo Building LiveTranslationCaption...
echo ============================================

REM Ensure pyinstaller is installed
pip install pyinstaller

REM Build the executable
pyinstaller --name LiveTranslationCaption ^
            --windowed ^
            --onefile ^
            --add-data "config.json;." ^
            --icon resources/icon.ico ^
            --hidden-import PyQt5 ^
            --hidden-import speech_recognition ^
            --hidden-import googletrans ^
            --hidden-import pyaudio ^
            src/main.py

echo.
echo ============================================
echo Build complete!
echo Executable location: dist/LiveTranslationCaption.exe
echo ============================================
pause
