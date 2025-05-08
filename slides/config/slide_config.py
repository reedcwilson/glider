"""
Slide configuration handling
"""

import os
import yaml
import tempfile
from slides.utils.error_handler import ErrorHandler
from slides.utils.file_utils import file_exists, read_file


class Slide:
    """Represents a single slide"""
    
    def __init__(self, index, style=None):
        """Initialize a slide object"""
        self.index = index
        self.style = style or {}
        self.path = None
        self.content = None
        self.html = None
        self.is_temp_file = False
    
    def set_path(self, path):
        """Set the path to the markdown file"""
        self.path = path
        self.is_temp_file = False
    
    def set_content(self, content):
        """Set direct markdown content"""
        self.content = content
        # Create a temporary file for the content
        fd, temp_path = tempfile.mkstemp(suffix='.md', prefix=f'slide_{self.index}_')
        os.close(fd)
        
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.path = temp_path
        self.is_temp_file = True
    
    def cleanup(self):
        """Clean up temporary files if needed"""
        if self.is_temp_file and self.path and os.path.exists(self.path):
            try:
                os.remove(self.path)
            except Exception as e:
                ErrorHandler.handle_file_error(e, self.path)


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
            
            # Clean up any existing slides
            self._cleanup_slides()
            self.slides = []
            
            # Process slides
            self._process_slides()
            
        except Exception as e:
            ErrorHandler.handle_config_error(e, yaml_path)
    
    def _cleanup_slides(self):
        """Clean up temporary files from slides"""
        for slide in self.slides:
            slide.cleanup()
    
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
            style = global_style.copy()
            
            if isinstance(slide_data, dict):
                # Extract style if present
                if 'style' in slide_data:
                    style.update(slide_data['style'])
                
                # Create slide object
                slide = Slide(index, style)
                
                # Handle path or content
                if 'path' in slide_data:
                    # Resolve relative path
                    full_path = os.path.join(self.base_dir, slide_data['path'])
                    slide.set_path(full_path)
                elif 'content' in slide_data:
                    # Use direct markdown content
                    slide.set_content(slide_data['content'])
                else:
                    raise ValueError(f"Slide {index} must have either 'path' or 'content' defined")
            else:
                # Simple string path
                slide = Slide(index, style)
                full_path = os.path.join(self.base_dir, slide_data)
                slide.set_path(full_path)
            
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
    
    def __del__(self):
        """Destructor to clean up temporary files"""
        self._cleanup_slides()
