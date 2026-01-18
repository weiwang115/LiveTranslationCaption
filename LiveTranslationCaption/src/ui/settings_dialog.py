from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QSpinBox, QCheckBox,
                             QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt
import json


class SettingsDialog(QDialog):
    """Settings dialog for configuring the application."""
    
    def __init__(self, config_path, parent=None):
        super().__init__(parent)
        self.config_path = config_path
        self.config = self._load_config()
        self._init_ui()
        
    def _load_config(self):
        """Load configuration from file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except:
            return {
                "audio_input_device": "default",
                "language": "ja",
                "translation_language": "en",
                "caption_display_duration": 5,
                "enable_auto_start": True
            }
    
    def _save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def _init_ui(self):
        """Initialize the UI."""
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout()
        
        # Audio settings group
        audio_group = QGroupBox("Audio Settings")
        audio_layout = QFormLayout()
        
        self.device_combo = QComboBox()
        self.device_combo.addItems(["Default", "Stereo Mix", "Loopback"])
        audio_layout.addRow("Input Device:", self.device_combo)
        
        audio_group.setLayout(audio_layout)
        layout.addWidget(audio_group)
        
        # Language settings group
        lang_group = QGroupBox("Language Settings")
        lang_layout = QFormLayout()
        
        self.source_lang_combo = QComboBox()
        self.source_lang_combo.addItems(["Japanese (ja)", "English (en)", "Chinese (zh)", "Korean (ko)"])
        self.source_lang_combo.setCurrentText(f"Japanese (ja)")
        lang_layout.addRow("Source Language:", self.source_lang_combo)
        
        self.target_lang_combo = QComboBox()
        self.target_lang_combo.addItems(["English (en)", "Japanese (ja)", "Chinese (zh)", "Korean (ko)"])
        self.target_lang_combo.setCurrentText(f"English (en)")
        lang_layout.addRow("Target Language:", self.target_lang_combo)
        
        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)
        
        # Display settings group
        display_group = QGroupBox("Display Settings")
        display_layout = QFormLayout()
        
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1, 30)
        self.duration_spin.setValue(self.config.get("caption_display_duration", 5))
        self.duration_spin.setSuffix(" seconds")
        display_layout.addRow("Caption Duration:", self.duration_spin)
        
        self.autostart_check = QCheckBox("Start automatically")
        self.autostart_check.setChecked(self.config.get("enable_auto_start", True))
        display_layout.addRow("", self.autostart_check)
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self._on_save)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _on_save(self):
        """Save settings and close dialog."""
        self.config["caption_display_duration"] = self.duration_spin.value()
        self.config["enable_auto_start"] = self.autostart_check.isChecked()
        
        if self._save_config():
            self.accept()
    
    def get_config(self):
        """Get the current configuration."""
        return self.config
        self.layout.addWidget(self.translation_language_input)

        self.save_button = QtWidgets.QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

        self.load_settings()

    def load_settings(self):
        config_path = os.path.join(os.path.dirname(__file__), '../../config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
                self.audio_device_input.setText(config.get('audio_device', ''))
                self.translation_language_input.setText(config.get('translation_language', ''))

    def save_settings(self):
        config = {
            'audio_device': self.audio_device_input.text(),
            'translation_language': self.translation_language_input.text()
        }
        config_path = os.path.join(os.path.dirname(__file__), '../../config.json')
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
        self.accept()