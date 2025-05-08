"""
Error handling utilities
"""

import logging
import sys


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("slides_error.log"),
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger("slides")


class ErrorHandler:
    """Handles various types of errors in the application"""
    
    @staticmethod
    def handle_file_error(error, file_path=None):
        """Handle file-related errors"""
        message = f"File error: {str(error)}"
        if file_path:
            message += f" (File: {file_path})"
        
        logger.error(message)
        return message
    
    @staticmethod
    def handle_config_error(error, config_path=None):
        """Handle configuration errors"""
        message = f"Configuration error: {str(error)}"
        if config_path:
            message += f" (Config: {config_path})"
        
        logger.error(message)
        return message
    
    @staticmethod
    def handle_markdown_error(error, markdown_path=None):
        """Handle markdown parsing errors"""
        message = f"Markdown error: {str(error)}"
        if markdown_path:
            message += f" (File: {markdown_path})"
        
        logger.error(message)
        return message
    
    @staticmethod
    def handle_hotkey_error(error):
        """Handle hotkey-related errors"""
        message = f"Hotkey error: {str(error)}"
        logger.error(message)
        return message
    
    @staticmethod
    def handle_application_error(error):
        """Handle general application errors"""
        message = f"Application error: {str(error)}"
        logger.error(message)
        return message
