#!/usr/bin/env python3
"""
Pixel Edition - Premium Emulator Frontend for Tensor-Powered Pixel Devices
Version: 0.1.0

Main application entry point (Pure XML-Driven Architecture)
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

# Core XML Engines
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
from ui.theme.monet import MaterialYouTheme  # Updated path to match UI guidelines


class PixelEditionApp(App):

    def build(self):
        """
        Entry point for Kivy app lifecycle
        """
        # ---------- INIT XML BACKEND ----------
        try:
            # Initialize our high-performance in-memory engines instead of databases
            self.xml_engine = XMLEngine()
            self.frontend_engine = FrontEndEngine(self.xml_engine)

            # Hardware specific service deployments
            self.tensor_service = TensorOptimizationService()
            self.tensor_service.detect_device()

            # Pass the frontend engine context to route actions purely via XML tags
            self.core_manager = CoreManager(self.frontend_engine)

            # Extract Dynamic System Wallpaper Palette
            self.theme = MaterialYouTheme()

        except Exception as e:
            print(f"[INIT ERROR] Failed parsing native service initialization stacks: {e}")

        # ---------- MAIN BASE LAYOUT ----------
        self.main_layout = BoxLayout(orientation='vertical')

        # Prevent Codespaces/X11 rendering lifecycle racing loops
        Clock.schedule_once(self._build_ui, 0)

        return self.main_layout

    # ---------------- UI BUILD PIPELINE ----------------
    def _build_ui(self, dt=None):
        # HEADER BAR
        header = BoxLayout(size_hint_y=0.08, orientation='horizontal')

        with header.canvas.before:
            Color(0.15, 0.15, 0.18, 1)
            self.header_rect = Rectangle(size=header.size, pos=header.pos)

        header.bind(size=self._update_rect, pos=self._update_rect)

        title = Label(text='Pixel Edition', size_hint_x=0.7, font_size='22sp', halign='left')
        nav_btn = Button(text='☰', size_hint_x=0.3, font_size='20sp')
        nav_btn.bind(on_press=self.show_nav_menu)

        header.add_widget(title)
        header.add_widget(nav_btn)

        self.main_layout.add_widget(header)

        # CENTRAL DISPLAY CANVAS AREA
        self.content_area = BoxLayout(orientation='vertical')
        self.main_layout.add_widget(self.content_area)

        # ---------- INITIALIZE APP VIEWS ----------
        self.home_screen = HomeScreen(name='home', app=self)
        self.library_screen = LibraryScreen(name='library', app=self)
        self.downloader_screen = CoreDownloaderScreen(name='downloader', app=self)
        self.settings_screen = SettingsScreen(name='settings', app=self)

        # Default initialization launch target
        self.show_downloader()

    # ---------------- INDENTED SCREEN NAVIGATION CONTROLS ----------------
    def show_home(self, instance=None):
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.home_screen)

    def show_library(self, instance=None):
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.library_screen)

    def show_downloader(self, instance=None):
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.downloader_screen)

    def show_settings(self, instance=None):
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.settings_screen) 

    # ---------------- DYNAMIC SYSTEM NAVIGATION OVERLAYS ----------------
    def show_nav_menu(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        buttons = [
            ("Home", self.show_home),
            ("Library", self.show_library),
            ("Download Cores", self.show_downloader),
            ("Settings", self.show_settings),
        ]

        for text, callback in buttons:
            btn = Button(text=text, size_hint_y=None, height=50)
            # Safe binding context prevents callback execution dropping before closing
            btn.bind(on_press=lambda x, cb=callback: self._close_popup_and_run(cb))
            content.add_widget(btn)

        self.popup = Popup(title="Navigation", content=content, size_hint=(0.8, 0.6))
        self.popup.open()

    def _close_popup_and_run(self, callback):
        """Dismisses navigation panels securely before invoking view state updates."""
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()
        callback()

    # ---------------- UI CANVAS TRANSFORM HELPERS ----------------
    def _update_rect(self, instance, value):
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size


if __name__ == '__main__':
    PixelEditionApp().run()
