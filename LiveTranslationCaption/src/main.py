#!/usr/bin/env python3
"""
Live Translation Caption Application
Captures system audio, recognizes Japanese speech, and displays English captions.
"""

import sys
import os
import threading
import time
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audio.capture import AudioCapture
from audio.processor import AudioProcessor
from translation.translator import Translator
from ui.caption_window import CaptionWindow
from ui.settings_dialog import SettingsDialog
from utils.config import Config


class LiveTranslationApp:
    """Main application class."""
    
    def __init__(self):
        self.config = Config("config.json")
        
        # Initialize Qt Application
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # Initialize components
        self.audio_capture = None
        self.audio_processor = None
        self.translator = None
        self.caption_window = None
        
        # Processing thread
        self.is_running = False
        self.processing_thread = None
        
        # Create system tray icon
        self._create_tray_icon()
        
        # Initialize components
        self._init_components()
        
    def _create_tray_icon(self):
        """Create system tray icon with menu."""
        self.tray_icon = QSystemTrayIcon(self.app)
        
        # Create menu
        menu = QMenu()
        
        start_action = QAction("Start", self.app)
        start_action.triggered.connect(self.start_capture)
        menu.addAction(start_action)
        
        stop_action = QAction("Stop", self.app)
        stop_action.triggered.connect(self.stop_capture)
        menu.addAction(stop_action)
        
        menu.addSeparator()
        
        settings_action = QAction("Settings", self.app)
        settings_action.triggered.connect(self.show_settings)
        menu.addAction(settings_action)
        
        menu.addSeparator()
        
        quit_action = QAction("Quit", self.app)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.setToolTip("Live Translation Caption")
        self.tray_icon.show()
        
        # Show notification
        self.tray_icon.showMessage(
            "Live Translation Caption",
            "Application started. Right-click the icon to start/stop.",
            QSystemTrayIcon.Information,
            2000
        )
    
    def _init_components(self):
        """Initialize all components."""
        # Audio capture
        sample_rate = self.config.get("sample_rate", 16000)
        chunk_size = self.config.get("chunk_size", 1024)
        self.audio_capture = AudioCapture(sample_rate=sample_rate, chunk_size=chunk_size)
        
        # Audio processor
        language = self.config.get("language", "ja")
        energy_threshold = self.config.get("energy_threshold", 300)
        self.audio_processor = AudioProcessor(language=f"{language}-JP", energy_threshold=energy_threshold)
        
        # Translator
        source_lang = self.config.get("language", "ja")
        target_lang = self.config.get("translation_language", "en")
        self.translator = Translator(source_lang=source_lang, target_lang=target_lang)
        
        # Caption window
        self.caption_window = CaptionWindow()
        duration_ms = self.config.get("caption_display_duration", 5) * 1000
        self.caption_window.set_fade_duration(duration_ms)
    
    def start_capture(self):
        """Start audio capture and processing."""
        if not self.is_running:
            self.is_running = True
            self.audio_capture.start()
            
            # Start processing thread
            self.processing_thread = threading.Thread(target=self._process_audio_loop, daemon=True)
            self.processing_thread.start()
            
            self.tray_icon.showMessage(
                "Live Translation Caption",
                "Capture started",
                QSystemTrayIcon.Information,
                1000
            )
            print("Application started - Listening for audio...")
    
    def stop_capture(self):
        """Stop audio capture and processing."""
        if self.is_running:
            self.is_running = False
            self.audio_capture.stop()
            
            if self.processing_thread:
                self.processing_thread.join(timeout=2)
            
            self.tray_icon.showMessage(
                "Live Translation Caption",
                "Capture stopped",
                QSystemTrayIcon.Information,
                1000
            )
            print("Application stopped")
    
    def _process_audio_loop(self):
        """Main processing loop running in separate thread."""
        while self.is_running:
            try:
                # Get 3 seconds of audio
                audio_data = self.audio_capture.get_audio_chunk(duration_seconds=3)
                
                if audio_data:
                    # Process audio to text
                    japanese_text = self.audio_processor.process_audio(audio_data)
                    
                    if japanese_text:
                        # Translate to English
                        english_caption = self.translator.translate(japanese_text)
                        
                        if english_caption:
                            # Update caption window
                            self.caption_window.update_caption(english_caption)
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error in processing loop: {e}")
                time.sleep(1)
    
    def show_settings(self):
        """Show settings dialog."""
        dialog = SettingsDialog("config.json")
        if dialog.exec_():
            # Reload configuration
            self.config.reload()
            
            # Restart if running
            was_running = self.is_running
            if was_running:
                self.stop_capture()
            
            # Reinitialize components
            self._init_components()
            
            if was_running:
                self.start_capture()
    
    def quit_app(self):
        """Quit the application."""
        self.stop_capture()
        if self.caption_window:
            self.caption_window.close()
        self.app.quit()
    
    def run(self):
        """Run the application."""
        # Auto-start if enabled
        if self.config.get("enable_auto_start", True):
            QTimer.singleShot(1000, self.start_capture)
        
        return self.app.exec_()


def main():
    """Main entry point."""
    print("="*60)
    print("Live Translation Caption - Japanese to English")
    print("="*60)
    print("Starting application...")
    
    try:
        app = LiveTranslationApp()
        sys.exit(app.run())
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()