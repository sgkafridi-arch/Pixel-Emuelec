"""
Core Downloader Screen - One-click core downloads with BIOS management
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.clock import mainthread
import threading


class CoreDownloaderScreen(BoxLayout):

    def __init__(self, app=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app = app
        self.padding = '12dp'
        self.spacing = '12dp'
        self.downloading_cores = {}

        # ── Core manager — use the one already on app if available ──────────
        self.core_manager = getattr(app, 'core_manager', None)
        if self.core_manager is None:
            try:
                from core.core_manager import CoreManager
                self.core_manager = CoreManager()
            except Exception as e:
                print(f"[Downloader] CoreManager unavailable: {e}")

        # ── Title ────────────────────────────────────────────────────────────
        self.add_widget(Label(
            text='Download Emulator Cores',
            size_hint_y=0.08,
            font_size='22sp',
            bold=True
        ))

        self.add_widget(Label(
            text='One-click download. ROMs & BIOS folders created automatically.',
            size_hint_y=0.06,
            font_size='11sp',
            color=(0.8, 0.8, 0.5, 1.0)
        ))

        # ── Scrollable core list ─────────────────────────────────────────────
        cores_scroll = ScrollView(size_hint_y=0.86)
        self.cores_grid = GridLayout(
            cols=1, spacing='8dp', size_hint_y=None, padding='8dp'
        )
        self.cores_grid.bind(minimum_height=self.cores_grid.setter('height'))

        try:
            from core.cores_manifest import CORES_MANIFEST
            for console_name in CORES_MANIFEST:
                self._add_console_card(console_name)
        except Exception as e:
            print(f"[Downloader] Could not load CORES_MANIFEST: {e}")
            self.cores_grid.add_widget(Label(
                text='No cores manifest found.\nAdd core/cores_manifest.py to populate this list.',
                font_size='13sp',
                color=(1, 0.4, 0.4, 1),
                size_hint_y=None,
                height='80dp',
                halign='center'
            ))

        cores_scroll.add_widget(self.cores_grid)
        self.add_widget(cores_scroll)

    def _add_console_card(self, console_name):
        try:
            from core.cores_manifest import CORES_MANIFEST, get_bios_info, needs_bios
            console_info = CORES_MANIFEST.get(console_name, {})

            card = BoxLayout(
                orientation='vertical',
                size_hint_y=None, height='120dp',
                padding='8dp', spacing='4dp'
            )

            # Header row
            header = BoxLayout(size_hint_y=0.35, spacing='8dp')
            header.add_widget(Label(
                text=console_info.get('name', console_name),
                font_size='14sp', bold=True, size_hint_x=0.6
            ))

            if self.core_manager and self.core_manager.is_core_downloaded(console_name):
                status_text, status_color = "✓ Downloaded", (0.2, 1.0, 0.2, 1.0)
            else:
                status_text, status_color = "Not Downloaded", (0.8, 0.8, 0.5, 1.0)

            header.add_widget(Label(
                text=status_text, font_size='11sp',
                color=status_color, size_hint_x=0.4
            ))
            card.add_widget(header)

            # Info line
            info_text = f"Size: {console_info.get('file_size_mb', 0)}MB"
            if needs_bios(console_name):
                bios_files = get_bios_info(console_name).get('required_files', [])[:2]
                info_text += f" | BIOS: {', '.join(bios_files)}..."
            card.add_widget(Label(
                text=info_text, font_size='10sp',
                color=(0.7, 0.7, 0.7, 1.0), size_hint_y=0.25
            ))

            # Progress bar
            card.add_widget(ProgressBar(value=0, max=100, size_hint_y=0.15))

            # Action buttons
            btn_row = BoxLayout(size_hint_y=0.25, spacing='4dp')
            dl_btn = Button(
                text='Download',
                background_color=(0.2, 0.6, 1.0, 1.0), size_hint_x=0.5
            )
            dl_btn.bind(on_press=lambda x, c=console_name: self.download_console(c))
            btn_row.add_widget(dl_btn)

            rom_btn = Button(
                text='ROM Folder',
                background_color=(0.2, 0.8, 0.6, 1.0), size_hint_x=0.5
            )
            rom_btn.bind(on_press=lambda x, c=console_name: self.show_rom_folder(c))
            btn_row.add_widget(rom_btn)

            card.add_widget(btn_row)
            self.cores_grid.add_widget(card)

        except Exception as e:
            print(f"[Downloader] Error adding card for {console_name}: {e}")

    def download_console(self, console_name):
        if not self.core_manager:
            self._show_message('Error', 'Core manager not available')
            return
        threading.Thread(
            target=self._download_thread,
            args=(console_name,), daemon=True
        ).start()

    def _download_thread(self, console_name):
        try:
            self.core_manager.create_console_rom_directory(console_name)
            result = self.core_manager.download_core(
                console_name,
                progress_callback=self._update_progress
            )
            if result.get('success'):
                self._update_ui_success(console_name)
            else:
                self._update_ui_error(console_name, result.get('error', 'Unknown error'))
        except Exception as e:
            self._update_ui_error(console_name, str(e))

    def _update_progress(self, downloaded, total):
        if total > 0:
            pass  # Hook progress bar update here when wired to a widget ref

    @mainthread
    def _update_ui_success(self, console_name):
        self._show_message(
            'Success',
            f'{console_name} core downloaded!\n\nROMs folder:\n~/.pixel_edition/roms/{console_name.lower()}'
        )

    @mainthread
    def _update_ui_error(self, console_name, error):
        self._show_message('Error', f'Failed to download {console_name}:\n{error}')

    def show_rom_folder(self, console_name):
        if not self.core_manager:
            self._show_message('Error', 'Core manager not available')
            return
        try:
            from core.cores_manifest import needs_bios, get_bios_info
            rom_dir = self.core_manager.get_console_directory(console_name)
            message = f"ROM Directory:\n{rom_dir}\n\n"
            if needs_bios(console_name):
                bios_dir  = self.core_manager.get_bios_directory(console_name)
                bios_info = get_bios_info(console_name)
                message += f"BIOS Directory:\n{bios_dir}\n\n"
                message += f"Required BIOS:\n{', '.join(bios_info.get('required_files', []))}\n\n"
                bios_check = self.core_manager.verify_bios_files(console_name)
                if bios_check.get('complete'):
                    message += "✓ All BIOS files found!"
                else:
                    message += f"❌ Missing: {', '.join(bios_check.get('missing', []))}"
            else:
                message += "✓ No BIOS required"
            self._show_message('Console Directory', message)
        except Exception as e:
            self._show_message('Error', str(e))

    def _show_message(self, title, message):
        content = BoxLayout(orientation='vertical', padding='12dp', spacing='8dp')
        scroll = ScrollView()
        lbl = Label(text=message, font_size='12sp', size_hint_y=None)
        lbl.bind(texture_size=lbl.setter('size'))
        scroll.add_widget(lbl)
        content.add_widget(scroll)
        close_btn = Button(text='Close', size_hint_y=0.2)
        popup = Popup(title=title, content=content, size_hint=(0.9, 0.7))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()
