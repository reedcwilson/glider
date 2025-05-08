"""
Slide display component
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt


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
        self.web_view.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        self.web_view.setStyleSheet("""
            QWebEngineView {
                background: transparent;
            }
        """)
        self.layout.addWidget(self.web_view)
        
        # Set initial content
        self.clear()
    
    def set_content(self, html_content):
        """Set HTML content to display"""
        # Add border-radius to the HTML content
        styled_html = f"""
        <html>
        <head>
            <style>
                body {{
                    margin: 0;
                    padding: 10px;
                    border-radius: 10px;
                    overflow: hidden;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        self.web_view.setHtml(styled_html)
    
    def clear(self):
        """Clear current content"""
        self.web_view.setHtml("<html><body style='border-radius: 10px; padding: 10px;'><p>No slide loaded</p></body></html>")
