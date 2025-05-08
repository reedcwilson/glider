"""
Tests for markdown processing
"""

import os
import tempfile
import unittest
from slides.markdown.parser import MarkdownParser
from slides.markdown.renderer import HTMLRenderer


class TestMarkdownParser(unittest.TestCase):
    """Test markdown parsing functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.parser = MarkdownParser()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.markdown_path = os.path.join(self.temp_dir.name, "test.md")
    
    def tearDown(self):
        """Clean up test environment"""
        self.temp_dir.cleanup()
    
    def test_parse_text(self):
        """Test parsing markdown text"""
        markdown_text = "# Test Heading\n\nThis is a test paragraph."
        html = self.parser.parse_text(markdown_text)
        
        self.assertIn("<h1>Test Heading</h1>", html)
        self.assertIn("<p>This is a test paragraph.</p>", html)
    
    def test_parse_file(self):
        """Test parsing markdown file"""
        # Create test markdown file
        markdown_content = "# File Test\n\nThis is a test file."
        with open(self.markdown_path, "w") as f:
            f.write(markdown_content)
        
        # Parse file
        html = self.parser.parse_file(self.markdown_path)
        
        self.assertIn("<h1>File Test</h1>", html)
        self.assertIn("<p>This is a test file.</p>", html)
    
    def test_parse_code_blocks(self):
        """Test parsing code blocks"""
        markdown_text = "```python\ndef test():\n    return 'Hello'\n```"
        html = self.parser.parse_text(markdown_text)
        
        self.assertIn("<code>", html)
        # The code is present but with syntax highlighting spans
        self.assertIn("<span class=\"k\">def</span>", html)
    
    def test_parse_tables(self):
        """Test parsing tables"""
        markdown_text = "| Header 1 | Header 2 |\n| -------- | -------- |\n| Cell 1   | Cell 2   |"
        html = self.parser.parse_text(markdown_text)
        
        self.assertIn("<table>", html)
        self.assertIn("<th>Header 1</th>", html)
        self.assertIn("<td>Cell 1</td>", html)


class TestHTMLRenderer(unittest.TestCase):
    """Test HTML rendering functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.renderer = HTMLRenderer()
    
    def test_apply_styling(self):
        """Test applying styling to HTML content"""
        html_content = "<h1>Test</h1><p>Content</p>"
        style = {
            "font": "Arial",
            "fontSize": 28,
            "textColor": "#333333",
            "justify": "center"
        }
        
        styled_html = self.renderer.apply_styling(html_content, style)
        
        self.assertIn("font-family: Arial", styled_html)
        self.assertIn("font-size: 28px", styled_html)
        self.assertIn("color: #333333", styled_html)
        self.assertIn("text-align: center", styled_html)
    
    def test_create_slide_html(self):
        """Test creating complete HTML document for slide"""
        html_content = "<h1>Test Slide</h1>"
        style = {
            "backgroundColor": "#F0F0F0",
            "font": "Helvetica",
            "fontSize": 24
        }
        
        slide_html = self.renderer.create_slide_html(html_content, style)
        
        self.assertIn("<!DOCTYPE html>", slide_html)
        self.assertIn("<html>", slide_html)
        self.assertIn("<head>", slide_html)
        self.assertIn("<body>", slide_html)
        self.assertIn("background-color: #F0F0F0", slide_html)
        self.assertIn("<h1>Test Slide</h1>", slide_html)
