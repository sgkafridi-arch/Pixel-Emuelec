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
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

# your project imports (keep as-is if they exist)
from core.database import init_db, get_db_session
from core.tensor_service import TensorOptimizationService
from core.performance_profiles import PerformanceProfileManager
from core.core_manager import CoreManager

from ui.screens.home import HomeScreen
from ui.screens.library import LibraryScreen
from ui.screens.downloader import CoreDownloaderScreen
from ui.screens.settings import SettingsScreen
from ui.theme_engine import MaterialYouTheme


class PixelEditionApp(App):

    def build(self):
        """
        Entry point for Kivy app
        """

        # ---------- INIT BACKEND ----------
        try:
            init_db()
            self.db_session = get_db_session()

            self.tensor_service = TensorOptimizationService()
            self.tensor_service.detect_device()

            self.profile_manager = PerformanceProfileManager(self.db_session)
            self.core_manager = CoreManager(self.db_session)

            self.theme = MaterialYouTheme()

        except Exception as e:
            print(f"[INIT ERROR] {e}")

        # ---------- MAIN LAYOUT ----------
        self.main_layout = BoxLayout(orientation='vertical')

        # IMPORTANT: delay UI build (fixes Codespaces/Kivy lifecycle bugs)
        Clock.schedule_once(self._build_ui, 0)

        return self.main_layout

    # ---------------- UI BUILD ----------------
    def _build_ui(self, dt=None):

        # HEADER
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

        # CONTENT AREA
        self.content_area = BoxLayout(orientation='vertical')
        self.main_layout.add_widget(self.content_area)

        # ---------- CREATE SCREENS ----------
        self.home_screen = HomeScreen(name='home', app=self)
        self.library_screen = LibraryScreen(name='library', app=self)
        self.downloader_screen = CoreDownloaderScreen(name='downloader', app=self)
        self.settings_screen = SettingsScreen(name='settings', app=self)

        # Default screen
        self.show_downloader()

    # ---------------- SAFE SCREEN SWITCHING ----------------
    def show_home(self, instance=None):
        if not hasattr(self, "home_screen"):
            return
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.home_screen)

    def show_library(self, instance=None):
        if not hasattr(self, "library_screen"):
            return
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.library_screen)

    def show_downloader(self, instance=None):
        if not hasattr(self, "downloader_screen"):
            return
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.downloader_screen)

    def show_settings(self, instance=None):
        if not hasattr(self, "settings_screen"):
            return
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.settings_screen)

    # ---------------- NAV MENU ----------------
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
            btn.bind(on_press=lambda x, cb=callback: self._close_popup_and_run(cb))
            content.add_widget(btn)

        self.popup = Popup(title="Navigation", content=content,
                           size_hint=(0.8, 0.6))
        self.popup.open()

    def _close_popup_and_run(self, callback):
        if hasattr(self, "popup"):
            self.popup.dismiss()
        callback()

    # ---------------- UI HELPERS ----------------
    def _update_rect(self, instance, value):
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size


if __name__ == '__main__':
    PixelEditionApp().run()
