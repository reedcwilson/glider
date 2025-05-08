#!/usr/bin/env python3
"""
Markdown Slides Application for macOS
Entry point for the application
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from slides.config.app_config import AppConfig
from slides.config.slide_config import SlideConfig
from slides.presentation.window import PresentationWindow
from slides.hotkeys.manager import HotkeyManager
from slides.utils.file_utils import ensure_config_directory
from slides.utils.error_handler import ErrorHandler


def main():
    """Application entry point"""
    try:
        # Ensure configuration directory exists
        ensure_config_directory()
        
        # Initialize application
        app = QApplication(sys.argv)
        
        # Load application configuration
        app_config = AppConfig()
        config_path = os.path.expanduser("~/.config/slides/config.json")
        app_config.load_config(config_path)
        
        # Initialize presentation window
        window = PresentationWindow(app_config)
        
        # Initialize hotkey manager with safe defaults
        try:
            # Initialize hotkey manager
            hotkey_manager = HotkeyManager(app_config)
            
            # Set up hotkey handlers
            hotkey_manager.set_next_handler(window.next_slide)
            hotkey_manager.set_previous_handler(window.previous_slide)
            
            # Register hotkeys
            hotkey_manager.register_hotkeys()
            
            # Clean up on exit (in try block)
            exit_code = app.exec()
            try:
                hotkey_manager.unregister_hotkeys()
            except:
                pass  # Ignore errors during cleanup
            sys.exit(exit_code)
        except Exception as e:
            # If hotkey registration fails, continue without hotkeys
            print(f"Warning: Global hotkeys disabled - {str(e)}")
            ErrorHandler.handle_hotkey_error(e)
            
            # Show window and start application without hotkeys
            window.show()
            sys.exit(app.exec())
        
    except Exception as e:
        ErrorHandler.handle_application_error(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
