"""
Global hotkey registration and management
"""

from pynput import keyboard
from slides.utils.error_handler import ErrorHandler


class HotkeyManager:
    """Manages global hotkeys for the application"""
    
    # Key mapping for pynput
    KEY_MAPPING = {
        'cmd': keyboard.Key.cmd,
        'alt': keyboard.Key.alt,
        'shift': keyboard.Key.shift,
        'ctrl': keyboard.Key.ctrl,
        'left': keyboard.Key.left,
        'right': keyboard.Key.right,
        'up': keyboard.Key.up,
        'down': keyboard.Key.down,
        'space': keyboard.Key.space,
        'esc': keyboard.Key.esc
    }
    
    def __init__(self, config):
        """Initialize hotkey manager with configuration"""
        self.config = config
        self.hotkey_config = config.get_hotkey_config()
        self.next_handler = None
        self.previous_handler = None
        self.listener = None
        self.active_keys = set()
    
    def register_hotkeys(self):
        """Register global hotkeys"""
        try:
            # Check if we're on macOS and handle accordingly
            import platform
            if platform.system() == 'Darwin':
                # On macOS, we'll log a warning but not fail if hotkeys can't be registered
                try:
                    self.listener = keyboard.Listener(
                        on_press=self._on_key_press,
                        on_release=self._on_key_release,
                        suppress=False  # Don't suppress events to avoid conflicts
                    )
                    self.listener.start()
                except Exception as e:
                    ErrorHandler.handle_hotkey_error(e)
                    print("Warning: Global hotkeys could not be registered. Use in-app navigation instead.")
            else:
                # On other platforms, proceed normally
                self.listener = keyboard.Listener(
                    on_press=self._on_key_press,
                    on_release=self._on_key_release
                )
                self.listener.start()
        except Exception as e:
            ErrorHandler.handle_hotkey_error(e)
            print("Warning: Global hotkeys could not be registered. Use in-app navigation instead.")
    
    def unregister_hotkeys(self):
        """Unregister global hotkeys"""
        if self.listener:
            self.listener.stop()
            self.listener = None
    
    def set_next_handler(self, handler):
        """Set handler for next slide hotkey"""
        self.next_handler = handler
    
    def set_previous_handler(self, handler):
        """Set handler for previous slide hotkey"""
        self.previous_handler = handler
    
    def _on_key_press(self, key):
        """Handle key press events"""
        # Add key to active keys set
        self.active_keys.add(key)
        
        # Check if next slide hotkey combination is pressed
        if self._check_hotkey_combination('next_slide') and self.next_handler:
            self.next_handler()
            return True
        
        # Check if previous slide hotkey combination is pressed
        if self._check_hotkey_combination('previous_slide') and self.previous_handler:
            self.previous_handler()
            return True
        
        return True
    
    def _on_key_release(self, key):
        """Handle key release events"""
        # Remove key from active keys set
        if key in self.active_keys:
            self.active_keys.remove(key)
        
        return True
    
    def _check_hotkey_combination(self, hotkey_name):
        """Check if a specific hotkey combination is currently pressed"""
        if hotkey_name not in self.hotkey_config:
            return False
        
        required_keys = self.hotkey_config[hotkey_name]
        
        # Convert string keys to pynput keys
        required_pynput_keys = set()
        for key_name in required_keys:
            if key_name in self.KEY_MAPPING:
                required_pynput_keys.add(self.KEY_MAPPING[key_name])
            else:
                # For single character keys
                required_pynput_keys.add(keyboard.KeyCode.from_char(key_name))
        
        # Check if all required keys are in the active keys set
        return required_pynput_keys.issubset(self.active_keys)
