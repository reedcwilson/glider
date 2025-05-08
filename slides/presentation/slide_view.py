"""
Slide display component
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl


class SlideView(QWidget):
    """Widget for displaying slides as HTML"""
    
    def __init__(self, parent=None):
        """Initialize slide view component"""
        super().__init__(parent)
        
        # Set up layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Create web view for rendering HTML
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)
        
        # Set initial content
        self.clear()
    
    def set_content(self, html_content):
        """Set HTML content to display"""
        self.web_view.setHtml(html_content)
    
    def clear(self):
        """Clear current content"""
        self.web_view.setHtml("<html><body><p>No slide loaded</p></body></html>")
