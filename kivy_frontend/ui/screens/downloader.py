"""
Core downloader screen - Download and manage emulator cores
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class CoreDownloaderScreen(BoxLayout):
    """
    Emulator core downloader screen
    """
    
    AVAILABLE_CORES = [
        {'name': 'FBNeo', 'version': '1.0.0', 'size': '45.5MB', 'type': 'Arcade'},
        {'name': 'Flycast', 'version': '2.0', 'size': '52.3MB', 'type': 'Dreamcast'},
        {'name': 'PPSSPP', 'version': '1.15.4', 'size': '38.7MB', 'type': 'PSP'},
        {'name': 'YabaSanshiro', 'version': '1.5', 'size': '35.2MB', 'type': 'Saturn'},
        {'name': 'PCSX2', 'version': '1.7.4', 'size': '61.8MB', 'type': 'PS2'},
    ]
    
    def __init__(self, app=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app = app
        self.padding = '12dp'
        self.spacing = '12dp'
        
        title = Label(
            text='Download Emulator Cores',
            size_hint_y=0.08,
            font_size='22sp',
            bold=True
        )
        self.add_widget(title)
        
        info = Label(
            text='Select cores to download from official GitHub repositories',
            size_hint_y=0.06,
            font_size='11sp',
            color=(0.8, 0.8, 0.8, 1)
        )
        self.add_widget(info)
        
        cores_scroll = ScrollView()
        cores_grid = GridLayout(
            cols=1,
            spacing='12dp',
            size_hint_y=None,
            padding='12dp'
        )
        cores_grid.bind(minimum_height=cores_grid.setter('height'))
        
        for core in self.AVAILABLE_CORES:
            core_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height='80dp',
                spacing='8dp'
            )
            
            info_layout = BoxLayout(orientation='vertical', size_hint_x=0.6, spacing='4dp')
            title_label = Label(
                text=f"{core['name']} v{core['version']}",
                font_size='14sp',
                bold=True
            )
            info_layout.add_widget(title_label)
            
            size_label = Label(
                text=f"Size: {core['size']} | {core['type']}",
                font_size='11sp',
                color=(0.8, 0.8, 0.8, 1)
            )
            info_layout.add_widget(size_label)
            core_layout.add_widget(info_layout)
            
            download_btn = Button(text='Download', size_hint_x=0.4)
            core_layout.add_widget(download_btn)
            
            cores_grid.add_widget(core_layout)
        
        cores_scroll.add_widget(cores_grid)
        self.add_widget(cores_scroll)
