"""
Tests for hotkey management
"""

import unittest
from unittest.mock import MagicMock, patch
from slides.config.app_config import AppConfig
from slides.hotkeys.manager import HotkeyManager


class TestHotkeyManager(unittest.TestCase):
    """Test hotkey management functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Create mock app config
        self.app_config = MagicMock(spec=AppConfig)
        self.app_config.get_hotkey_config.return_value = {
            "next_slide": ["cmd", "right"],
            "previous_slide": ["cmd", "left"]
        }
        
        # Create hotkey manager
        self.hotkey_manager = HotkeyManager(self.app_config)
        
        # Create mock handlers
        self.next_handler = MagicMock()
        self.previous_handler = MagicMock()
        
        # Set handlers
        self.hotkey_manager.set_next_handler(self.next_handler)
        self.hotkey_manager.set_previous_handler(self.previous_handler)
    
    def test_set_handlers(self):
        """Test setting hotkey handlers"""
        self.assertEqual(self.hotkey_manager.next_handler, self.next_handler)
        self.assertEqual(self.hotkey_manager.previous_handler, self.previous_handler)
    
    @patch('pynput.keyboard.Listener')
    def test_register_hotkeys(self, mock_listener):
        """Test registering hotkeys"""
        # Mock listener instance
        mock_listener_instance = MagicMock()
        mock_listener.return_value = mock_listener_instance
        
        # Register hotkeys
        self.hotkey_manager.register_hotkeys()
        
        # Verify listener was created and started
        mock_listener.assert_called_once()
        mock_listener_instance.start.assert_called_once()
    
    @patch('pynput.keyboard.Listener')
    def test_unregister_hotkeys(self, mock_listener):
        """Test unregistering hotkeys"""
        # Mock listener instance
        mock_listener_instance = MagicMock()
        mock_listener.return_value = mock_listener_instance
        
        # Register hotkeys
        self.hotkey_manager.register_hotkeys()
        
        # Unregister hotkeys
        self.hotkey_manager.unregister_hotkeys()
        
        # Verify listener was stopped
        mock_listener_instance.stop.assert_called_once()
    
    def test_check_hotkey_combination(self):
        """Test checking hotkey combinations"""
        from pynput.keyboard import Key, KeyCode
        
        # Set up active keys
        self.hotkey_manager.active_keys = {Key.cmd, Key.right}
        
        # Check next slide hotkey
        result = self.hotkey_manager._check_hotkey_combination('next_slide')
        self.assertTrue(result)
        
        # Check previous slide hotkey (should be false)
        result = self.hotkey_manager._check_hotkey_combination('previous_slide')
        self.assertFalse(result)
        
        # Change active keys
        self.hotkey_manager.active_keys = {Key.cmd, Key.left}
        
        # Check previous slide hotkey
        result = self.hotkey_manager._check_hotkey_combination('previous_slide')
        self.assertTrue(result)
