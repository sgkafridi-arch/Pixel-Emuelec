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
    """
    Core downloader with one-click installation
    Manages ROM directories and BIOS files automatically
    """
    
    def __init__(self, app=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app = app
        self.padding = '12dp'
        self.spacing = '12dp'
        
        self.downloading_cores = {}  # Track downloads in progress
        
        # Initialize core manager
        try:
            from core.core_manager import CoreManager
            if app and app.db_session:
                self.core_manager = CoreManager(app.db_session)
            else:
                self.core_manager = None
        except Exception as e:
            self.core_manager = None
            print(f"Core manager error: {e}")
        
        # Title
        title = Label(
            text='Download Emulator Cores',
            size_hint_y=0.08,
            font_size='22sp',
            bold=True
        )
        self.add_widget(title)
        
        # Instructions
        instructions = Label(
            text='One-click download. ROMs & BIOS folders created automatically.',
            size_hint_y=0.06,
            font_size='11sp',
            color=(0.8, 0.8, 0.5, 1.0)
        )
        self.add_widget(instructions)
        
        # Cores list scroll
        cores_scroll = ScrollView(size_hint_y=0.86)
        self.cores_grid = GridLayout(
            cols=1,
            spacing='8dp',
            size_hint_y=None,
            padding='8dp'
        )
        self.cores_grid.bind(minimum_height=self.cores_grid.setter('height'))
        
        # Get all consoles from manifest
        try:
            from core.cores_manifest import CORES_MANIFEST
            consoles = list(CORES_MANIFEST.keys())
        except:
            consoles = []
        
        # Create download card for each console
        for console_name in consoles:
            self._add_console_card(console_name)
        
        cores_scroll.add_widget(self.cores_grid)
        self.add_widget(cores_scroll)
    
    def _add_console_card(self, console_name):
        """
        Add a console download card
        """
        try:
            from core.cores_manifest import CORES_MANIFEST, get_bios_info, needs_bios
            
            console_info = CORES_MANIFEST.get(console_name, {})
            
            # Main card layout
            card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height='120dp',
                padding='8dp',
                spacing='4dp'
            )
            
            # Header with console name and status
            header = BoxLayout(size_hint_y=0.35, spacing='8dp')
            
            title = Label(
                text=f"{console_info.get('name', console_name)}",
                font_size='14sp',
                bold=True,
                size_hint_x=0.6
            )
            header.add_widget(title)
            
            # Status label
            status_key = f"{console_name}_status"
            if self.core_manager and self.core_manager.is_core_downloaded(console_name):
                status_text = "✓ Downloaded"
                status_color = (0.2, 1.0, 0.2, 1.0)
            else:
                status_text = "Not Downloaded"
                status_color = (0.8, 0.8, 0.5, 1.0)
            
            status_label = Label(
                text=status_text,
                font_size='11sp',
                color=status_color,
                size_hint_x=0.4
            )
            header.add_widget(status_label)
            card.add_widget(header)
            
            # Info line
            info_text = f"Size: {console_info.get('file_size_mb', 0)}MB"
            if needs_bios(console_name):
                bios_info = get_bios_info(console_name)
                info_text += f" | BIOS: {', '.join(bios_info.get('required_files', [])[:2])}..."
            
            info_label = Label(
                text=info_text,
                font_size='10sp',
                color=(0.7, 0.7, 0.7, 1.0),
                size_hint_y=0.25
            )
            card.add_widget(info_label)
            
            # Progress bar (hidden by default)
            progress = ProgressBar(
                value=0,
                max=100,
                size_hint_y=0.15
            )
            progress.id = f"{console_name}_progress"
            card.add_widget(progress)
            
            # Buttons
            button_layout = BoxLayout(size_hint_y=0.25, spacing='4dp')
            
            # Download button
            download_btn = Button(
                text='Download',
                background_color=(0.2, 0.6, 1.0, 1.0),
                size_hint_x=0.5
            )
            download_btn.bind(on_press=lambda x: self.download_console(console_name))
            button_layout.add_widget(download_btn)
            
            # ROM Folder button
            rom_btn = Button(
                text='ROM Folder',
                background_color=(0.2, 0.8, 0.6, 1.0),
                size_hint_x=0.5
            )
            rom_btn.bind(on_press=lambda x: self.show_rom_folder(console_name))
            button_layout.add_widget(rom_btn)
            
            card.add_widget(button_layout)
            self.cores_grid.add_widget(card)
            
        except Exception as e:
            print(f"Error adding console card: {e}")
    
    def download_console(self, console_name):
        """
        Download core for console
        """
        if not self.core_manager:
            self._show_message('Error', 'Core manager not available')
            return
        
        # Start download in background
        thread = threading.Thread(
            target=self._download_thread,
            args=(console_name,),
            daemon=True
        )
        thread.start()
    
    def _download_thread(self, console_name):
        """
        Background download thread
        """
        try:
            from core.cores_manifest import CORES_MANIFEST
            
            # Create ROM directory
            self.core_manager.create_console_rom_directory(console_name)
            
            # Download core
            result = self.core_manager.download_core(
                console_name,
                progress_callback=self._update_progress
            )
            
            if result['success']:
                # Create ROM folder structure
                rom_dir = self.core_manager.get_console_directory(console_name)
                self._update_ui_success(console_name)
            else:
                self._update_ui_error(console_name, result.get('error', 'Unknown error'))
                
        except Exception as e:
            self._update_ui_error(console_name, str(e))
    
    def _update_progress(self, downloaded, total):
        """
        Update progress bar
        """
        if total > 0:
            progress = (downloaded / total) * 100
            # Update UI
    
    @mainthread
    def _update_ui_success(self, console_name):
        """
        Update UI after successful download
        """
        self._show_message(
            'Success',
            f'{console_name} core downloaded!\n\nROMs folder created at:\n~/.pixel_edition/roms/{console_name.lower()}'
        )
    
    @mainthread
    def _update_ui_error(self, console_name, error):
        """
        Update UI after download error
        """
        self._show_message('Error', f'Failed to download {console_name}:\n{error}')
    
    def show_rom_folder(self, console_name):
        """
        Show ROM folder location and instructions
        """
        if not self.core_manager:
            self._show_message('Error', 'Core manager not available')
            return
        
        rom_dir = self.core_manager.get_console_directory(console_name)
        
        try:
            from core.cores_manifest import needs_bios, get_bios_info
            
            message = f"ROM Directory:\n{rom_dir}\n\n"
            
            if needs_bios(console_name):
                bios_dir = self.core_manager.get_bios_directory(console_name)
                bios_info = get_bios_info(console_name)
                message += f"BIOS Directory:\n{bios_dir}\n\n"
                message += f"Required BIOS Files:\n{', '.join(bios_info.get('required_files', []))}\n\n"
            
            # Check BIOS status
            if needs_bios(console_name):
                bios_check = self.core_manager.verify_bios_files(console_name)
                if bios_check['complete']:
                    message += "✓ All BIOS files found!"
                else:
                    message += f"❌ Missing BIOS: {', '.join(bios_check['missing'])}"
            else:
                message += "✓ No BIOS required for this console"
            
            self._show_message('Console Directory', message)
            
        except Exception as e:
            self._show_message('Error', str(e))
    
    def _show_message(self, title, message):
        """
        Show information popup
        """
        content = BoxLayout(orientation='vertical', padding='12dp', spacing='8dp')
        
        scroll = ScrollView()
        msg_label = Label(
            text=message,
            font_size='12sp',
            markup=True,
            size_hint_y=None
        )
        msg_label.bind(texture_size=msg_label.setter('size'))
        scroll.add_widget(msg_label)
        content.add_widget(scroll)
        
        close_btn = Button(text='Close', size_hint_y=0.2)
        content.add_widget(close_btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.9, 0.7))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
