# Quick Start Guide

## For Windows Users

### First Time Setup

1. **Enable Stereo Mix**:
   - Right-click the speaker icon in your system tray
   - Click "Sound settings"
   - Click "Sound Control Panel" on the right
   - Go to the "Recording" tab
   - Right-click in empty space and check "Show Disabled Devices"
   - Right-click "Stereo Mix" and select "Enable"
   - Click "OK"

2. **Install the Application**:
   - Double-click `install.bat`
   - Wait for installation to complete
   - Press any key to close

### Running the Application

**Option 1: Using the run script**
- Double-click `run.bat`

**Option 2: Manual**
1. Open Command Prompt in the project folder
2. Run: `venv\Scripts\activate`
3. Run: `python src\main.py`

### Using the Application

1. After starting, look for the application icon in your system tray (bottom-right corner)
2. Right-click the icon
3. Select "Start" to begin capturing audio
4. Play any Japanese audio (video, game, etc.)
5. English captions will appear at the bottom of your screen
6. Right-click the icon and select "Stop" when done
7. Select "Quit" to close the application

### Settings

Right-click the system tray icon and select "Settings" to configure:
- Caption display duration
- Auto-start on launch
- Audio input device
- Languages (source and target)

## Building an Executable

To create a standalone `.exe` file:
1. Double-click `build.bat`
2. Wait for the build to complete
3. Find the executable in the `dist` folder

## Troubleshooting

**No captions appearing?**
- Make sure Stereo Mix is enabled and set as default recording device
- Check if audio is actually playing
- Try increasing the volume of the application you're listening to

**"PyAudio not installed" error?**
- Run: `pip install pipwin`
- Then: `pipwin install pyaudio`

**Translation not working?**
- Check your internet connection
- Google Translate API requires internet access

**Captions are behind other windows?**
- This shouldn't happen (window is always on top)
- Try restarting the application

## Tips

- The application works best with clear audio
- Background noise may affect recognition accuracy
- Captions stay on screen for 5 seconds by default (configurable)
- The app uses free Google APIs, so there may be rate limits
- Close other audio applications if you experience issues

## System Requirements

- Windows 10 or Windows 11
- Python 3.8 or higher
- Active internet connection
- Stereo Mix or equivalent audio loopback device
- At least 4GB RAM recommended
