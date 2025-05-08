"""
Application configuration handling
"""

import json
import os
from slides.utils.error_handler import ErrorHandler
from slides.utils.file_utils import file_exists, read_file, write_file


class AppConfig:
    """Handles application-wide configuration"""
    
    DEFAULT_CONFIG = {
        "hotkeys": {
            "next_slide": ["cmd", "alt", "shift", "right"],
            "previous_slide": ["cmd", "alt", "shift", "left"]
        },
        "window": {
            "width": 800,
            "height": 600,
            "fullscreen": False
        },
        "slides": {
            "default_directory": "~"
        }
    }
    
    def __init__(self):
        """Initialize application configuration"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.config_path = None
    
    def load_config(self, config_path):
        """Load application configuration from JSON file"""
        self.config_path = config_path
        
        try:
            if file_exists(config_path):
                config_data = read_file(config_path)
                loaded_config = json.loads(config_data)
                
                # Update default config with loaded values
                self._update_config(loaded_config)
            else:
                # Create default config file if it doesn't exist
                self._create_default_config()
                
        except Exception as e:
            ErrorHandler.handle_config_error(e, config_path)
    
    def _update_config(self, loaded_config):
        """Update configuration with loaded values"""
        # Update hotkeys if present
        if 'hotkeys' in loaded_config:
            self.config['hotkeys'].update(loaded_config['hotkeys'])
        
        # Update window settings if present
        if 'window' in loaded_config:
            self.config['window'].update(loaded_config['window'])
            
        # Update slides settings if present
        if 'slides' in loaded_config:
            if 'slides' not in self.config:
                self.config['slides'] = {}
            self.config['slides'].update(loaded_config['slides'])
    
    def _create_default_config(self):
        """Create default configuration file"""
        try:
            config_json = json.dumps(self.config, indent=2)
            write_file(self.config_path, config_json)
        except Exception as e:
            ErrorHandler.handle_config_error(e, self.config_path)
    
    def get_hotkey_config(self):
        """Return hotkey configuration"""
        return self.config.get('hotkeys', {})
    
    def get_window_config(self):
        """Return window configuration"""
        return self.config.get('window', {})
        
    def get_slides_config(self):
        """Return slides configuration"""
        return self.config.get('slides', {})
