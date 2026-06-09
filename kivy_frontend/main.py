#!/usr/bin/env python3
"""
Pixel Edition - Premium Emulator Frontend for Tensor-Powered Pixel Devices
Version: 0.1.0

Main application entry point
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from core.database import init_db, get_db_session
    from core.tensor_service import TensorOptimizationService
    from core.performance_profiles import PerformanceProfileManager
    from ui.theme_engine import MaterialYouTheme
    from ui.screens.home import HomeScreen
    from ui.screens.library import LibraryScreen
    from ui.screens.settings import SettingsScreen
    from ui.screens.downloader import CoreDownloaderScreen
except ImportError as e:
    print(f"Import error: {e}")

# Set window properties
Window.size = (1440, 2960)  # Pixel 7 Pro resolution
Window.clearcolor = (0.05, 0.05, 0.05, 1)


class PixelEditionApp(App):
    """
    Main Pixel Edition Application
    Tensor-optimized emulator frontend for Pixel devices
    """
    
    def build(self):
        """
        Build the application UI
        """
        try:
            # Initialize database
            init_db()
            self.db_session = get_db_session()
            
            # Initialize Tensor optimization
            self.tensor_service = TensorOptimizationService()
            self.tensor_service.detect_device()
            
            # Initialize performance profiles
            self.profile_manager = PerformanceProfileManager(self.db_session)
            
            # Apply Material You theme
            self.theme = MaterialYouTheme()
            
            # Create screens
            self.home_screen = HomeScreen(name='home', app=self)
            self.library_screen = LibraryScreen(name='library', app=self)
            self.downloader_screen = CoreDownloaderScreen(name='downloader', app=self)
            self.settings_screen = SettingsScreen(name='settings', app=self)
            
        except Exception as e:
            print(f"Initialization error: {e}")
        
        # Main layout
        self.main_layout = BoxLayout(orientation='vertical')
        self._build_ui()
        
        return self.main_layout
    
    def _build_ui(self):
        """
        Build the UI structure
        """
        # Header
        header = BoxLayout(size_hint_y=0.08, orientation='horizontal')
        header.canvas.before.clear()
        
        from kivy.graphics import Color, Rectangle
        with header.canvas.before:
            Color(0.2, 0.2, 0.22, 1)  # Material You color
            Rectangle(size=header.size, pos=header.pos)
        
        title = Label(text='Pixel Edition', size_hint_x=0.7, font_size='24sp', bold=True)
        header.add_widget(title)
        
        # Navigation button
        nav_btn = Button(text='☰', size_hint_x=0.3, font_size='20sp')
        nav_btn.bind(on_press=self.show_nav_menu)
        header.add_widget(nav_btn)
        
        self.main_layout.add_widget(header)
        
        # Content area
        self.content_area = BoxLayout(orientation='vertical')
        self.main_layout.add_widget(self.content_area)
        
        # Show home screen by default
        self.show_home()
    
    def show_home(self, instance=None):
        """Show home screen"""
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.home_screen)
    
    def show_library(self, instance=None):
        """Show library screen"""
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.library_screen)
    
    def show_downloader(self, instance=None):
        """Show core downloader screen"""
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.downloader_screen)
    
    def show_settings(self, instance=None):
        """Show settings screen"""
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.settings_screen)
    
    def show_nav_menu(self, instance):
        """Show navigation menu"""
        content = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')
        
        buttons = [
            ('Home', self.show_home),
            ('Library', self.show_library),
            ('Download Cores', self.show_downloader),
            ('Settings', self.show_settings),
        ]
        
        for label, callback in buttons:
            btn = Button(text=label, size_hint_y=None, height='50dp')
            btn.bind(on_press=callback)
            content.add_widget(btn)
        
        popup = Popup(title='Navigation', content=content, size_hint=(0.8, 0.6))
        popup.open()


if __name__ == '__main__':
    app = PixelEditionApp()
    app.run()
