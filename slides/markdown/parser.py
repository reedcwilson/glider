"""
Markdown parsing functionality
"""

import markdown
from slides.utils.error_handler import ErrorHandler
from slides.utils.file_utils import read_file


class MarkdownParser:
    """Handles markdown parsing and conversion to HTML"""
    
    def __init__(self, config=None):
        """Initialize markdown parser with configuration"""
        self.config = config or {}
        self.extensions = ['tables', 'fenced_code', 'codehilite']
    
    def parse_file(self, file_path):
        """Parse markdown file and return HTML"""
        try:
            markdown_text = read_file(file_path)
            return self.parse_text(markdown_text)
        except Exception as e:
            ErrorHandler.handle_markdown_error(e, file_path)
            return f"<p>Error loading slide: {str(e)}</p>"
    
    def parse_text(self, markdown_text):
        """Parse markdown text and return HTML"""
        try:
            html = markdown.markdown(
                markdown_text,
                extensions=self.extensions
            )
            return html
        except Exception as e:
            ErrorHandler.handle_markdown_error(e)
            return f"<p>Error parsing markdown: {str(e)}</p>"
