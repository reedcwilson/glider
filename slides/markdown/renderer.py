"""
HTML rendering utilities for markdown slides
"""


class HTMLRenderer:
    """Handles HTML rendering and styling for slides"""
    
    def __init__(self, config=None):
        """Initialize HTML renderer with configuration"""
        self.config = config or {}
    
    def apply_styling(self, html_content, slide_style):
        """Apply styling to HTML content"""
        # This is a simple implementation - in a real app, you might want to use CSS
        styled_html = f"""
        <div style="
            font-family: {slide_style.get('font', 'Helvetica')};
            font-size: {slide_style.get('fontSize', 24)}px;
            color: {slide_style.get('textColor', '#000000')};
            text-align: {slide_style.get('justify', 'left')};
        ">
            {html_content}
        </div>
        """
        return styled_html
    
    def create_slide_html(self, html_content, slide_style):
        """Create complete HTML document for slide"""
        styled_content = self.apply_styling(html_content, slide_style)
        
        # Create a complete HTML document with styling
        html_document = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    background-color: {slide_style.get('backgroundColor', '#FFFFFF')};
                    overflow: hidden;
                }}
                
                pre {{
                    background-color: #f5f5f5;
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                
                code {{
                    font-family: monospace;
                }}
                
                img {{
                    max-width: 100%;
                    height: auto;
                }}
                
                table {{
                    border-collapse: collapse;
                    width: 100%;
                }}
                
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                }}
                
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            {styled_content}
        </body>
        </html>
        """
        
        return html_document
