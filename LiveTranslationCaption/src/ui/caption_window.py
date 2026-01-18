from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QColor, QPalette
import sys


class CaptionSignals(QObject):
    """Signals for thread-safe caption updates."""
    update_text = pyqtSignal(str)


class CaptionWindow(QWidget):
    """
    A transparent overlay window that displays translated captions.
    Always on top, click-through enabled.
    """
    
    def __init__(self, width=800, height=150):
        super().__init__()
        self.signals = CaptionSignals()
        self.signals.update_text.connect(self._update_caption_internal)
        
        self.caption_text = ""
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(self._fade_caption)
        self.fade_duration = 5000  # 5 seconds
        
        self._init_ui(width, height)
        
    def _init_ui(self, width, height):
        """Initialize the UI."""
        # Window flags for transparent, always on top, frameless window
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowTransparentForInput  # Click-through
        )
        
        # Set transparent background
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Set window size and position (bottom center of screen)
        self.resize(width, height)
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - width) // 2
        y = screen_geometry.height() - height - 100
        self.move(x, y)
        
        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Create caption label
        self.caption_label = QLabel("")
        self.caption_label.setAlignment(Qt.AlignCenter)
        self.caption_label.setWordWrap(True)
        
        # Style the label with bold font and background
        font = QFont("Arial", 18, QFont.Bold)
        self.caption_label.setFont(font)
        self.caption_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 180);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        layout.addWidget(self.caption_label)
        self.setLayout(layout)
        
        # Show the window
        self.show()
        
    def update_caption(self, text):
        """
        Update the caption text (thread-safe).
        
        Args:
            text: Caption text to display
        """
        if text and text.strip():
            self.signals.update_text.emit(text)
    
    def _update_caption_internal(self, text):
        """Internal method to update caption (runs in main thread)."""
        self.caption_text = text
        self.caption_label.setText(text)
        self.caption_label.show()
        
        # Restart fade timer
        self.fade_timer.stop()
        self.fade_timer.start(self.fade_duration)
    
    def _fade_caption(self):
        """Fade out the caption after duration."""
        self.caption_label.setText("")
        self.fade_timer.stop()
    
    def set_fade_duration(self, milliseconds):
        """Set how long captions are displayed before fading."""
        self.fade_duration = milliseconds
    
    def close(self):
        """Close the caption window."""
        self.fade_timer.stop()
        super().close()