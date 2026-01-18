# Live Translation Caption

A Windows application that captures system audio, recognizes Japanese speech in real-time, and displays English translated captions on screen.

## Features

- ✨ **Real-time Audio Capture**: Captures system audio using PyAudio with loopback support
- 🎤 **Speech Recognition**: Converts Japanese speech to text using Google Speech Recognition
- 🌐 **Instant Translation**: Translates Japanese text to English using Google Translate API
- 📺 **Overlay Captions**: Displays transparent, always-on-top captions that don't interfere with your applications
- ⚙️ **Configurable**: Customizable settings for audio devices, languages, and display duration
- 🎯 **System Tray**: Runs quietly in the system tray with easy start/stop controls

## Requirements

- **Windows 10/11** (for system audio loopback support)
- **Python 3.8+**
- **Stereo Mix or similar loopback device** enabled in Windows audio settings

## Installation

### Option 1: Run from Source

1. **Clone the repository**:
   ```bash
   git clone https://github.com/weiwang115/LiveTranslationCaption.git
   cd LiveTranslationCaption/LiveTranslationCaption
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Enable Stereo Mix** (if not already enabled):
   - Right-click the speaker icon in the system tray
   - Select "Sound settings" → "Sound Control Panel"
   - Go to the "Recording" tab
   - Right-click empty space and check "Show Disabled Devices"
   - Enable "Stereo Mix" or similar loopback device

5. **Run the application**:
   ```bash
   cd src
   python main.py
   ```

### Option 2: Build Windows Executable

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Build executable**:
   ```bash
   pyinstaller --name LiveTranslationCaption ^
               --windowed ^
               --onefile ^
               --add-data "config.json;." ^
               src/main.py
   ```

3. **Run the executable**:
   - Find the `.exe` in the `dist` folder
   - Double-click to run

## Usage

1. **Start the application**: Run `main.py` or launch the executable
2. **System tray**: The application will appear in the system tray
3. **Start capture**: Right-click the tray icon and select "Start"
4. **View captions**: Translated captions will appear at the bottom center of your screen
5. **Configure**: Right-click → "Settings" to adjust preferences
6. **Stop/Exit**: Right-click → "Stop" or "Quit"

## Configuration

Edit `config.json` to customize settings:

```json
{
  "audio_input_device": "default",
  "language": "ja",
  "translation_language": "en",
  "caption_display_duration": 5,
  "enable_auto_start": true,
  "sample_rate": 16000,
  "chunk_size": 1024,
  "energy_threshold": 300
}
```

- **audio_input_device**: Audio input device (usually "default")
- **language**: Source language code ("ja" for Japanese)
- **translation_language**: Target language code ("en" for English)
- **caption_display_duration**: How long captions stay on screen (seconds)
- **enable_auto_start**: Auto-start capture on launch
- **sample_rate**: Audio sample rate (16000 Hz recommended)
- **chunk_size**: Audio buffer size
- **energy_threshold**: Voice activity detection threshold

## Project Structure

```
LiveTranslationCaption/
├── src/
│   ├── main.py                  # Application entry point
│   ├── audio/
│   │   ├── capture.py           # System audio capture
│   │   └── processor.py         # Speech recognition
│   ├── translation/
│   │   └── translator.py        # Translation service
│   ├── ui/
│   │   ├── caption_window.py    # Caption overlay window
│   │   └── settings_dialog.py   # Settings UI
│   └── utils/
│       └── config.py            # Configuration manager
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
├── config.json                  # Configuration file
└── README.md                    # This file
```

## Troubleshooting

### No audio captured
- Ensure "Stereo Mix" or equivalent loopback device is enabled in Windows
- Check that the correct audio device is selected in settings
- Try adjusting the energy threshold in `config.json`

### Recognition errors
- Ensure you have an active internet connection (Google APIs are used)
- Check that audio quality is sufficient
- Adjust the sample rate if needed

### Captions not appearing
- Verify the caption window is not minimized
- Check if captions are appearing behind other windows
- Restart the application

### Translation errors
- Ensure internet connectivity (Google Translate API requires online access)
- Check for API rate limiting (free tier has usage limits)

## Dependencies

- **PyQt5**: GUI framework for the overlay and system tray
- **PyAudio**: Audio capture library
- **SpeechRecognition**: Speech-to-text conversion
- **googletrans**: Translation API wrapper
- **NumPy**: Audio data processing

## Known Limitations

- Requires active internet connection for speech recognition and translation
- Google's free tier APIs have usage limits
- Loopback audio capture requires Windows-specific audio drivers
- Recognition accuracy depends on audio quality and background noise

## Future Enhancements

- [ ] Offline speech recognition support
- [ ] Multiple translation service backends
- [ ] Customizable caption styles and positions
- [ ] Support for more languages
- [ ] Audio file translation mode
- [ ] Translation history and export

## License

This project is provided as-is for educational and personal use.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Author

**weiwang115**

## Acknowledgments

- Google Speech Recognition API
- Google Translate API
- PyQt5 community
- SpeechRecognition library contributors
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python src/main.py
   ```
2. Configure your audio input device and translation options in the settings dialog.
3. Start listening to system audio, and the application will display translated captions in real-time.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.