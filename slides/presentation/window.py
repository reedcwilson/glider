"""
Main presentation window
"""

import os
from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QMessageBox, QVBoxLayout, 
    QWidget, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt, QSize
from slides.config.slide_config import SlideConfig
from slides.presentation.slide_view import SlideView
from slides.markdown.parser import MarkdownParser
from slides.markdown.renderer import HTMLRenderer


class PresentationWindow(QMainWindow):
    """Main presentation window"""
    
    def __init__(self, app_config):
        """Initialize presentation window"""
        super().__init__()
        
        self.app_config = app_config
        self.slide_config = SlideConfig()
        self.markdown_parser = MarkdownParser()
        self.html_renderer = HTMLRenderer()
        
        self.current_slide_index = 0
        
        # Set up window properties
        window_config = app_config.get_window_config()
        self.setWindowTitle("Markdown Slides")
        self.resize(
            window_config.get('width', 800),
            window_config.get('height', 600)
        )
        
        if window_config.get('fullscreen', False):
            self.showFullScreen()
        
        # Set up central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create slide view
        self.slide_view = SlideView(self)
        self.main_layout.addWidget(self.slide_view)
        
        # Create navigation controls
        self.create_navigation_controls()
        
        # Prompt for slides.yaml on startup
        self.prompt_for_slides_config()
    
    def create_navigation_controls(self):
        """Create navigation buttons"""
        control_layout = QHBoxLayout()
        
        # Previous slide button
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_slide)
        control_layout.addWidget(self.prev_button)
        
        # Next slide button
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_slide)
        control_layout.addWidget(self.next_button)
        
        self.main_layout.addLayout(control_layout)
    
    def prompt_for_slides_config(self):
        """Prompt user to select slides.yaml file"""
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Directory with slides.yaml",
            os.path.expanduser("~"),
            options=options
        )
        
        if directory:
            yaml_path = os.path.join(directory, "slides.yaml")
            if os.path.exists(yaml_path):
                self.load_slides_config(yaml_path)
            else:
                QMessageBox.warning(
                    self,
                    "File Not Found",
                    f"slides.yaml not found in {directory}"
                )
                self.prompt_for_slides_config()
    
    def load_slides_config(self, yaml_path):
        """Load slides configuration from YAML file"""
        try:
            self.slide_config.load_config(yaml_path)
            self.setWindowTitle(self.slide_config.get_title())
            
            # Load first slide
            if self.slide_config.get_slide_count() > 0:
                self.load_slide(0)
            else:
                QMessageBox.warning(
                    self,
                    "No Slides",
                    "No slides found in configuration"
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load slides configuration: {str(e)}"
            )
    
    def load_slide(self, slide_index):
        """Load and display slide"""
        if slide_index < 0 or slide_index >= self.slide_config.get_slide_count():
            return False
        
        slide = self.slide_config.get_slide(slide_index)
        if not slide:
            return False
        
        # Parse markdown to HTML
        html_content = self.markdown_parser.parse_file(slide.path)
        
        # Apply styling and create complete HTML
        styled_html = self.html_renderer.create_slide_html(html_content, slide.style)
        
        # Update slide view
        self.slide_view.set_content(styled_html)
        
        # Update current slide index
        self.current_slide_index = slide_index
        
        # Update navigation buttons
        self.prev_button.setEnabled(slide_index > 0)
        self.next_button.setEnabled(slide_index < self.slide_config.get_slide_count() - 1)
        
        return True
    
    def next_slide(self):
        """Navigate to next slide"""
        if self.current_slide_index < self.slide_config.get_slide_count() - 1:
            self.load_slide(self.current_slide_index + 1)
    
    def previous_slide(self):
        """Navigate to previous slide"""
        if self.current_slide_index > 0:
            self.load_slide(self.current_slide_index - 1)
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key_Right or event.key() == Qt.Key_Space:
            self.next_slide()
        elif event.key() == Qt.Key_Left or event.key() == Qt.Key_Backspace:
            self.previous_slide()
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
