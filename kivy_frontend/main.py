#!/usr/bin/env python3
"""
Pixel Edition - Premium Emulator Frontend for Tensor-Powered Pixel Devices
Version: 0.1.0
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

# UI Screens
from ui.screens.home import HomeScreen
from ui.screens.library import LibraryScreen
from ui.screens.downloader import CoreDownloaderScreen
from ui.screens.settings import SettingsScreen


class PixelEditionApp(App):

    def build(self):
        # ── Optional services (fail gracefully if missing) ──────────────────
        self.tensor_service = None
        self.core_manager = None
        self.theme = None

        try:
            from core.tensor_service import TensorOptimizationService
            self.tensor_service = TensorOptimizationService()
            self.tensor_service.detect_device()
            print("[INIT] TensorOptimizationService loaded.")
        except Exception as e:
            print(f"[INIT] tensor_service unavailable: {e}")

        try:
            from core.core_manager import CoreManager
            self.core_manager = CoreManager()
            print("[INIT] CoreManager loaded.")
        except Exception as e:
            print(f"[INIT] core_manager unavailable: {e}")

        # ── Root layout ──────────────────────────────────────────────────────
        self.main_layout = BoxLayout(orientation='vertical')
        Clock.schedule_once(self._build_ui, 0)
        return self.main_layout

    def _build_ui(self, dt=None):
        # STEP 1 — Instantiate all screens before any navigation runs
        print("[BUILD] Instantiating screens...")
        self.home_screen      = HomeScreen(name='home', app=self)
        self.library_screen   = LibraryScreen(name='library', app=self)
        self.downloader_screen = CoreDownloaderScreen(name='downloader', app=self)
        self.settings_screen  = SettingsScreen(name='settings', app=self)
        print("[BUILD] All screens ready.")

        # STEP 2 — Header
        header = BoxLayout(size_hint_y=0.08, orientation='horizontal')
        with header.canvas.before:
            Color(0.15, 0.15, 0.18, 1)
            self.header_rect = Rectangle(size=header.size, pos=header.pos)
        header.bind(size=self._update_rect, pos=self._update_rect)

        title   = Label(text='Pixel Edition', size_hint_x=0.7, font_size='22sp')
        nav_btn = Button(text='☰', size_hint_x=0.3, font_size='20sp')
        nav_btn.bind(on_press=self.show_nav_menu)
        header.add_widget(title)
        header.add_widget(nav_btn)
        self.main_layout.add_widget(header)

        # STEP 3 — Content canvas
        self.content_area = BoxLayout(orientation='vertical')
        self.main_layout.add_widget(self.content_area)

        # STEP 4 — Default screen
        self.show_home()

    # ── Screen switchers ────────────────────────────────────────────────────
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

    # ── Navigation menu ─────────────────────────────────────────────────────
    def show_nav_menu(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        for text, callback in [
            ("Home",           self.show_home),
            ("Library",        self.show_library),
            ("Download Cores", self.show_downloader),
            ("Settings",       self.show_settings),
        ]:
            btn = Button(text=text, size_hint_y=None, height=50)
            btn.bind(on_press=lambda x, cb=callback: self._close_popup_and_run(cb))
            content.add_widget(btn)

        self.popup = Popup(title="Navigation", content=content, size_hint=(0.8, 0.6))
        self.popup.open()

    def _close_popup_and_run(self, callback):
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()
        callback()

    # ── Helpers ─────────────────────────────────────────────────────────────
    def _update_rect(self, instance, value):
        self.header_rect.pos  = instance.pos
        self.header_rect.size = instance.size


if __name__ == '__main__':
    PixelEditionApp().run()
