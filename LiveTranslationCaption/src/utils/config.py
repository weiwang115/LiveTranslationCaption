import json
import os


class Config:
    """Configuration manager for the application."""
    
    DEFAULT_CONFIG = {
        "audio_input_device": "default",
        "language": "ja",
        "translation_language": "en",
        "caption_display_duration": 5,
        "enable_auto_start": True,
        "sample_rate": 16000,
        "chunk_size": 1024,
        "energy_threshold": 300,
        "api_keys": {
            "translation_service": ""
        }
    }
    
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file or create default."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    config = self.DEFAULT_CONFIG.copy()
                    config.update(loaded_config)
                    return config
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self.save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config=None):
        """Save configuration to file."""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value."""
        self.config[key] = value
    
    def reload(self):
        """Reload configuration from file."""
        self.config = self._load_config()
    
    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()