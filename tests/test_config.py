"""
Tests for configuration handling
"""

import os
import tempfile
import unittest
import json
import yaml
from slides.config.app_config import AppConfig
from slides.config.slide_config import SlideConfig


class TestAppConfig(unittest.TestCase):
    """Test application configuration handling"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, "config.json")
    
    def tearDown(self):
        """Clean up test environment"""
        self.temp_dir.cleanup()
    
    def test_default_config(self):
        """Test default configuration"""
        app_config = AppConfig()
        self.assertIn("hotkeys", app_config.config)
        self.assertIn("window", app_config.config)
    
    def test_load_config(self):
        """Test loading configuration from file"""
        # Create test config file
        test_config = {
            "hotkeys": {
                "next_slide": ["alt", "right"],
                "previous_slide": ["alt", "left"]
            },
            "window": {
                "width": 1024,
                "height": 768,
                "fullscreen": True
            }
        }
        
        with open(self.config_path, "w") as f:
            json.dump(test_config, f)
        
        # Load config
        app_config = AppConfig()
        app_config.load_config(self.config_path)
        
        # Verify config was loaded correctly
        self.assertEqual(app_config.config["hotkeys"]["next_slide"], ["alt", "right"])
        self.assertEqual(app_config.config["window"]["width"], 1024)
        self.assertTrue(app_config.config["window"]["fullscreen"])
    
    def test_get_hotkey_config(self):
        """Test getting hotkey configuration"""
        app_config = AppConfig()
        hotkeys = app_config.get_hotkey_config()
        self.assertIn("next_slide", hotkeys)
        self.assertIn("previous_slide", hotkeys)
    
    def test_get_window_config(self):
        """Test getting window configuration"""
        app_config = AppConfig()
        window = app_config.get_window_config()
        self.assertIn("width", window)
        self.assertIn("height", window)
        self.assertIn("fullscreen", window)


class TestSlideConfig(unittest.TestCase):
    """Test slide configuration handling"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.yaml_path = os.path.join(self.temp_dir.name, "slides.yaml")
        
        # Create test markdown files
        self.slide1_path = os.path.join(self.temp_dir.name, "slide1.md")
        self.slide2_path = os.path.join(self.temp_dir.name, "slide2.md")
        
        with open(self.slide1_path, "w") as f:
            f.write("# Slide 1\nContent for slide 1")
        
        with open(self.slide2_path, "w") as f:
            f.write("# Slide 2\nContent for slide 2")
    
    def tearDown(self):
        """Clean up test environment"""
        self.temp_dir.cleanup()
    
    def test_load_config(self):
        """Test loading slide configuration from YAML file"""
        # Create test YAML file
        test_config = {
            "title": "Test Presentation",
            "style": {
                "font": "Arial",
                "fontSize": 28,
                "backgroundColor": "#F0F0F0"
            },
            "slides": [
                {"path": "slide1.md"},
                {"path": "slide2.md", "style": {"backgroundColor": "#E0E0E0"}}
            ]
        }
        
        with open(self.yaml_path, "w") as f:
            yaml.dump(test_config, f)
        
        # Load config
        slide_config = SlideConfig()
        slide_config.load_config(self.yaml_path)
        
        # Verify config was loaded correctly
        self.assertEqual(slide_config.get_title(), "Test Presentation")
        self.assertEqual(slide_config.get_slide_count(), 2)
        
        # Check global style
        global_style = slide_config.get_global_style()
        self.assertEqual(global_style["font"], "Arial")
        self.assertEqual(global_style["fontSize"], 28)
        
        # Check slides
        slides = slide_config.get_slides()
        self.assertEqual(len(slides), 2)
        
        # Check slide paths are resolved correctly
        self.assertTrue(slides[0].path.endswith("slide1.md"))
        self.assertTrue(slides[1].path.endswith("slide2.md"))
        
        # Check slide styles
        self.assertEqual(slides[0].style["font"], "Arial")  # Inherited from global
        self.assertEqual(slides[1].style["backgroundColor"], "#E0E0E0")  # Overridden
    
    def test_get_slide(self):
        """Test getting slide by index"""
        # Create test YAML file
        test_config = {
            "title": "Test Presentation",
            "slides": [
                {"path": "slide1.md"},
                {"path": "slide2.md"}
            ]
        }
        
        with open(self.yaml_path, "w") as f:
            yaml.dump(test_config, f)
        
        # Load config
        slide_config = SlideConfig()
        slide_config.load_config(self.yaml_path)
        
        # Get slides by index
        slide0 = slide_config.get_slide(0)
        slide1 = slide_config.get_slide(1)
        slide_invalid = slide_config.get_slide(2)
        
        # Verify slides
        self.assertIsNotNone(slide0)
        self.assertIsNotNone(slide1)
        self.assertIsNone(slide_invalid)
        
        self.assertTrue(slide0.path.endswith("slide1.md"))
        self.assertTrue(slide1.path.endswith("slide2.md"))
