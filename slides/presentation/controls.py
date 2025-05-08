"""
Navigation controls for the presentation
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal


class NavigationControls(QWidget):
    """Navigation controls for slide presentation"""
    
    # Define signals
    next_clicked = pyqtSignal()
    previous_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize navigation controls"""
        super().__init__(parent)
        
        # Set up layout
        self.layout = QHBoxLayout(self)
        
        # Create previous button
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_clicked.emit)
        self.layout.addWidget(self.prev_button)
        
        # Create next button
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_clicked.emit)
        self.layout.addWidget(self.next_button)
        
        # Set initial state
        self.set_navigation_state(0, 0)
    
    def set_navigation_state(self, current_index, total_slides):
        """Update navigation button states based on current position"""
        self.prev_button.setEnabled(current_index > 0)
        self.next_button.setEnabled(current_index < total_slides - 1)
