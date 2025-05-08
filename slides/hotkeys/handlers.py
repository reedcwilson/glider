"""
Hotkey event handlers
"""


class HotkeyHandlers:
    """Handlers for hotkey events"""
    
    def __init__(self, presentation_window):
        """Initialize hotkey handlers with presentation window"""
        self.presentation_window = presentation_window
    
    def next_slide(self):
        """Handle next slide hotkey"""
        self.presentation_window.next_slide()
    
    def previous_slide(self):
        """Handle previous slide hotkey"""
        self.presentation_window.previous_slide()
