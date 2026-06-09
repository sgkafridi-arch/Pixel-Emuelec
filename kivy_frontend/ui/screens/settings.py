"""
Settings screen - Configuration and preferences
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView


class SettingsScreen(BoxLayout):
    """
    Settings and preferences screen
    """
    
    def __init__(self, app=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app = app
        self.padding = '12dp'
        self.spacing = '12dp'
        
        title = Label(
            text='Settings',
            size_hint_y=0.08,
            font_size='22sp',
            bold=True
        )
        self.add_widget(title)
        
        settings_scroll = ScrollView()
        settings_layout = GridLayout(
            cols=1,
            spacing='16dp',
            size_hint_y=None,
            padding='12dp'
        )
        settings_layout.bind(minimum_height=settings_layout.setter('height'))
        
        # Performance Profile
        perf_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp',
            spacing='12dp'
        )
        perf_label = Label(text='Performance:', size_hint_x=0.5)
        perf_layout.add_widget(perf_label)
        perf_spinner = Spinner(
            text='Balanced',
            values=('Battery Saver', 'Balanced', 'Performance', 'Ultra'),
            size_hint_x=0.5
        )
        perf_layout.add_widget(perf_spinner)
        settings_layout.add_widget(perf_layout)
        
        # Graphics Backend
        graphics_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp',
            spacing='12dp'
        )
        graphics_label = Label(text='Graphics:', size_hint_x=0.5)
        graphics_layout.add_widget(graphics_label)
        graphics_spinner = Spinner(
            text='Vulkan',
            values=('Vulkan', 'OpenGL ES'),
            size_hint_x=0.5
        )
        graphics_layout.add_widget(graphics_spinner)
        settings_layout.add_widget(graphics_layout)
        
        # Device Info
        device_info_btn = Button(
            text='Device Information',
            size_hint_y=None,
            height='50dp'
        )
        settings_layout.add_widget(device_info_btn)
        
        settings_scroll.add_widget(settings_layout)
        self.add_widget(settings_scroll)
