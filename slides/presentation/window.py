"""
Main presentation window
"""

import os

from PyQt6.QtCore import QPoint, QSize, Qt
from PyQt6.QtGui import QColor, QMouseEvent, QPainter, QPainterPath, QRegion
from PyQt6.QtWidgets import (QFileDialog, QHBoxLayout, QMainWindow,
                             QMessageBox, QPushButton, QSizePolicy,
                             QStackedLayout, QVBoxLayout, QWidget)

from slides.config.slide_config import SlideConfig
from slides.markdown.parser import MarkdownParser
from slides.markdown.renderer import HTMLRenderer
from slides.presentation.slide_view import SlideView


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

        # Variables for window dragging
        self.dragging = False
        self.drag_position = None

        # Set up window properties
        window_config = app_config.get_window_config()
        self.setWindowTitle("Markdown Slides")
        self.resize(window_config.get("width", 800), window_config.get("height", 600))

        # Remove title bar but keep window frame
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # Set window to be transparent for rounded corners
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        if window_config.get("fullscreen", False):
            self.showFullScreen()

        # Set up central widget with stacked layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout for the central widget
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(
            10, 10, 10, 10
        )  # Add margins for the rounded corners
        self.main_layout.setSpacing(0)

        # Create slide view (main content)
        self.slide_view = SlideView(self)
        self.main_layout.addWidget(self.slide_view)

        # Create overlay for navigation buttons
        self.create_navigation_overlay()

        # Apply rounded corners style
        self.setStyleSheet(
            """
            QMainWindow {
                background: transparent;
            }
            QWidget#centralWidget {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 15px;
            }
        """
        )
        self.central_widget.setObjectName("centralWidget")

        # Show the window before prompting for slides.yaml
        self.show()

        # Prompt for slides.yaml on startup
        self.prompt_for_slides_config()

    def create_navigation_overlay(self):
        """Create navigation buttons as an overlay on the content"""
        # Create container widget that will be positioned over the slide content
        self.overlay_widget = QWidget(self.central_widget)
        self.overlay_widget.setObjectName("navigationOverlay")

        # Make the overlay fill the entire central widget
        self.overlay_widget.setGeometry(self.central_widget.geometry())

        # Use horizontal layout for the overlay
        overlay_layout = QHBoxLayout(self.overlay_widget)
        overlay_layout.setContentsMargins(0, 0, 0, 0)
        overlay_layout.setSpacing(0)

        # Previous slide button (left side)
        self.prev_button = QPushButton("<")
        self.prev_button.clicked.connect(self.previous_slide)
        self.prev_button.setFixedWidth(40)
        self.prev_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )
        self.prev_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(0, 0, 0, 15);
                color: rgba(220, 220, 220, 255);
                border: none;
                font-size: 24px;
                font-weight: bold;
                border-top-left-radius: 10px;
                border-bottom-left-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 50);
            }
            QPushButton:disabled {
                background-color: rgba(0, 0, 0, 5);
                color: rgba(180, 180, 180, 50);
            }
        """
        )

        # Spacer to push buttons to the sides
        overlay_layout.addWidget(self.prev_button)
        overlay_layout.addStretch(1)

        # Next slide button (right side)
        self.next_button = QPushButton(">")
        self.next_button.clicked.connect(self.next_slide)
        self.next_button.setFixedWidth(40)
        self.next_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )
        self.next_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(0, 0, 0, 15);
                color: rgba(220, 220, 220, 255);
                border: none;
                font-size: 24px;
                font-weight: bold;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 50);
            }
            QPushButton:disabled {
                background-color: rgba(0, 0, 0, 5);
                color: rgba(180, 180, 180, 50);
            }
        """
        )
        overlay_layout.addWidget(self.next_button)

        # Make sure the overlay stays on top and resizes with the window
        self.central_widget.resizeEvent = self.resize_overlay

    def resize_overlay(self, event):
        """Ensure the overlay resizes with the window"""
        self.overlay_widget.setGeometry(self.central_widget.rect())
        # Call the original resize event
        QWidget.resizeEvent(self.central_widget, event)

    def prompt_for_slides_config(self):
        """Prompt user to select slides.yaml file"""
        try:
            # Get default directory from config, or use home directory as fallback
            slides_config = self.app_config.get_slides_config()
            default_dir = os.path.expanduser(slides_config.get("default_directory", "~"))
            
            directory = QFileDialog.getExistingDirectory(
                self, "Select Directory with slides.yaml", default_dir
            )

            if directory:
                yaml_path = os.path.join(directory, "slides.yaml")
                if os.path.exists(yaml_path):
                    self.load_slides_config(yaml_path)
                else:
                    QMessageBox.warning(
                        self, "File Not Found", f"slides.yaml not found in {directory}"
                    )
                    self.prompt_for_slides_config()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error selecting directory: {str(e)}")

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
                    self, "No Slides", "No slides found in configuration"
                )
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to load slides configuration: {str(e)}"
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
        self.next_button.setEnabled(
            slide_index < self.slide_config.get_slide_count() - 1
        )

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
        if event.key() == Qt.Key.Key_Right or event.key() == Qt.Key.Key_Space:
            self.next_slide()
        elif event.key() == Qt.Key.Key_Left or event.key() == Qt.Key.Key_Backspace:
            self.previous_slide()
        elif event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press events for window dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move events for window dragging"""
        if self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release events for window dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            event.accept()
