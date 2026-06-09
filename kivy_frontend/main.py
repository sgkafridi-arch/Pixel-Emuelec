#!/usr/bin/env python3
"""
Pixel Edition - Premium Emulator Frontend for Tensor-Powered Pixel Devices
Version: 0.1.0

Main application entry point (Pure XML-Driven Architecture Layout)
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

# Core XML Engines (Pure In-Memory Subsystem)
from core.xml_engine import XMLEngine
from core.engine import FrontEndEngine

# Services & Hardware Optimization Layers
from services.tensor_service import TensorOptimizationService
from services.core_manager import CoreManager

# UI Screens & Layout Layers
from ui.screens.home import HomeScreen
from ui.screens.library import LibraryScreen
from ui.screens.downloader import CoreDownloaderScreen
from ui.screens.settings import SettingsScreen
from ui.theme.monet import MaterialYouTheme


class PixelEditionApp(App):

    def build(self):
        """
        Initializes the application state, native systems, and parent layout.
        """
        # ---------- INIT XML BACKEND & SERVICES ----------
        try:
            # Initialize our high-performance database-free XML subsystems
            self.xml_engine = XMLEngine()
            self.frontend_engine = FrontEndEngine(self.xml_engine)

            # Hardware specific service deployments
            self.tensor_service = TensorOptimizationService()
            self.tensor_service.detect_device()

            # Pass the frontend engine context to route execution via raw XML paths
            self.core_manager = CoreManager(self.frontend_engine)

            # Dynamic Material You Theme Palette Subsystem
            self.theme = MaterialYouTheme()

        except Exception as e:
            print(f"[INIT ERROR] Failed parsing native service initialization stacks: {e}")

        # ---------- MAIN BASE LAYOUT ----------
        self.main_layout = BoxLayout(orientation='vertical')

        # Prevent Codespaces/X11 rendering lifecycle racing loops via scheduled frame delay
        Clock.schedule_once(self._build_ui, 0)

        return self.main_layout

    # ---------------- UI BUILD LIFECYCLE ----------------
    def _build_ui(self, dt=None):
        """
        Builds the complete UI structure using a strictly protected execution order.
        """
        # STEP 1: INSTANTIATE ALL SCREENS FIRST
        # This registers attributes to memory before navigation flows can access them.
        self.home_screen = HomeScreen(name='home', app=self)
        self.library_screen = LibraryScreen(name='library', app=self)
        self.downloader_screen = CoreDownloaderScreen(name='downloader', app=self)
        self.settings_screen = SettingsScreen(name='settings', app=self)

        # STEP 2: BUILD MAIN HEADER COMPONENT
        header = BoxLayout(size_hint_y=0.08, orientation='horizontal')

        with header.canvas.before:
            Color(0.15, 0.15, 0.18, 1)
            self.header_rect = Rectangle(size=header.size, pos=header.pos)

        header.bind(size=self._update_rect, pos=self._update_rect)

        title = Label(text='Pixel Edition', size_hint_x=0.7, font_size='22sp')
        nav_btn = Button(text='☰', size_hint_x=0.3, font_size='20sp')
        nav_btn.bind(on_press=self.show_nav_menu)

        header.add_widget(title)
        header.add_widget(nav_btn)
        self.main_layout.add_widget(header)

        # STEP 3: BUILD CENTRAL RENDERING CANVAS
        self.content_area = BoxLayout(orientation='vertical')
        self.main_layout.add_widget(self.content_area)

        # STEP 4: MOUNT THE DEFAULT SCREEN SECURELY
        # Now that self.home_screen exists in the class namespace, this call is safe.
        self.show_home()

    # ---------------- SAFE SCREEN MOUNT ROUTINES ----------------
    def show_home(self, instance=None):
        """Clears content canvas and mounts the Home Screen configuration."""
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.home_screen)

    def show_library(self, instance=None):
        """Clears content canvas and mounts the Rom Library Core."""
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.library_screen)

    def show_downloader(self, instance=None):
        """Clears content canvas and mounts the Emulator Core Downloader Panel."""
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.downloader_screen)

    def show_settings(self, instance=None):
        """Clears content canvas and mounts Frontend Preferences Config."""
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.settings_screen) 

    # ---------------- SYSTEM NAVIGATION PANEL ----------------
    def show_nav_menu(self, instance):
        """Generates dynamic flyout navigation panel overlay."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        buttons = [
            ("Home", self.show_home),
            ("Library", self.show_library),
            ("Download Cores", self.show_downloader),
            ("Settings", self.show_settings),
        ]

        for text, callback in buttons:
            btn = Button(text=text, size_hint_y=None, height=50)
            # Safe unique lambda binding ensures proper navigation flow closure
            btn.bind(on_press=lambda x, cb=callback: self._close_popup_and_run(cb))
            content.add_widget(btn)

        self.popup = Popup(title="Navigation", content=content, size_hint=(0.8, 0.6))
        self.popup.open()

    def _close_popup_and_run(self, callback):
        """Dismisses the modal overlay safely before updating active view states."""
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()
        callback()

    # ---------------- UI LAYOUT HELPERS ----------------
    def _update_rect(self, instance, value):
        """Synchronizes background layout bounds with active system resolution transformations."""
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size


if __name__ == '__main__':
    PixelEditionApp().run()
