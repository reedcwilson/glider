"""
Slide configuration handling
"""

import os
import yaml
from slides.utils.error_handler import ErrorHandler
from slides.utils.file_utils import file_exists, read_file


class Slide:
    """Represents a single slide"""
    
    def __init__(self, path, index, style=None):
        """Initialize a slide object"""
        self.path = path
        self.index = index
        self.style = style or {}
        self.content = None
        self.html = None


class SlideConfig:
    """Handles slide-specific configuration"""
    
    DEFAULT_STYLE = {
        "font": "Helvetica",
        "fontSize": 24,
        "backgroundColor": "#FFFFFF",
        "textColor": "#000000",
        "justify": "left"
    }
    
    def __init__(self):
        """Initialize slide configuration"""
        self.config = {}
        self.slides = []
        self.base_dir = ""
    
    def load_config(self, yaml_path):
        """Load slide configuration from YAML file"""
        try:
            if not file_exists(yaml_path):
                raise FileNotFoundError(f"Slide configuration file not found: {yaml_path}")
            
            # Store the base directory for resolving relative paths
            self.base_dir = os.path.dirname(os.path.abspath(yaml_path))
            
            # Read and parse YAML file
            yaml_content = read_file(yaml_path)
            self.config = yaml.safe_load(yaml_content)
            
            # Process slides
            self._process_slides()
            
        except Exception as e:
            ErrorHandler.handle_config_error(e, yaml_path)
    
    def _process_slides(self):
        """Process slides from configuration"""
        if not self.config or 'slides' not in self.config:
            raise ValueError("Invalid slide configuration: 'slides' section missing")
        
        # Get global style
        global_style = self.DEFAULT_STYLE.copy()
        if 'style' in self.config:
            global_style.update(self.config['style'])
        
        # Process each slide
        for index, slide_data in enumerate(self.config['slides']):
            if isinstance(slide_data, dict):
                path = slide_data.get('path')
                style = global_style.copy()
                if 'style' in slide_data:
                    style.update(slide_data['style'])
            else:
                path = slide_data
                style = global_style.copy()
            
            # Resolve relative path
            full_path = os.path.join(self.base_dir, path)
            
            # Create slide object
            slide = Slide(full_path, index, style)
            self.slides.append(slide)
    
    def get_slides(self):
        """Return list of slide objects"""
        return self.slides
    
    def get_slide_count(self):
        """Return number of slides"""
        return len(self.slides)
    
    def get_slide(self, index):
        """Return slide at specified index"""
        if 0 <= index < len(self.slides):
            return self.slides[index]
        return None
    
    def get_title(self):
        """Return presentation title"""
        return self.config.get('title', 'Markdown Presentation')
    
    def get_global_style(self):
        """Return global styling configuration"""
        style = self.DEFAULT_STYLE.copy()
        if 'style' in self.config:
            style.update(self.config['style'])
        return style
