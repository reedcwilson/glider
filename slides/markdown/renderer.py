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
        # We'll handle all styling in the CSS now
        styled_html = f"""
        <div class="slide-content">
            {html_content}
        </div>
        """
        return styled_html
    
    def create_slide_html(self, html_content, slide_style):
        """Create complete HTML document for slide"""
        styled_content = self.apply_styling(html_content, slide_style)
        justify = slide_style.get('justify', 'left')
        
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
                    font-family: {slide_style.get('font', 'Helvetica')};
                    font-size: {slide_style.get('fontSize', 24)}px;
                    color: {slide_style.get('textColor', '#000000')};
                }}
                
                .slide-content {{
                    width: 100%;
                    text-align: {justify};
                }}
                
                /* Center justification specific styles */
                {f'''
                /* Center everything except lists */
                .slide-content h1, 
                .slide-content h2, 
                .slide-content h3, 
                .slide-content h4, 
                .slide-content h5, 
                .slide-content h6,
                .slide-content p {{
                    text-align: center;
                }}
                
                /* For lists, we need to center the container but left-align the content */
                .slide-content ul,
                .slide-content ol {{
                    width: fit-content;
                    margin-left: auto;
                    margin-right: auto;
                    text-align: left;
                    padding-left: 40px;
                }}
                ''' if justify == 'center' else ''}
                
                pre {{
                    background-color: #f5f5f5;
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                    text-align: left;
                    {f'margin: 0 auto;' if justify == 'center' else ''}
                }}
                
                code {{
                    font-family: monospace;
                }}
                
                img {{
                    max-width: 100%;
                    height: auto;
                    {f'display: block; margin: 0 auto;' if justify == 'center' else ''}
                }}
                
                /* Tables should always be full width */
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 0 auto;
                }}
                
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                
                th {{
                    background-color: #f2f2f2;
                }}
                
                /* Blockquotes styling */
                blockquote {{
                    border-left: 5px solid #ddd;
                    padding-left: 10px;
                    margin-left: 20px;
                    font-style: italic;
                    {f'margin-left: auto; margin-right: auto; width: 80%;' if justify == 'center' else ''}
                }}
            </style>
        </head>
        <body>
            {styled_content}
        </body>
        </html>
        """
        
        return html_document
