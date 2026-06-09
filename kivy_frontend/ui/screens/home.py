"""
Home screen - Game discovery and quick access
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class HomeScreen(BoxLayout):
    """
    Home screen with featured games and recent games
    """
    
    def __init__(self, app=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app = app
        self.padding = '12dp'
        self.spacing = '12dp'
        
        # Featured section
        featured_label = Label(
            text='Featured Games',
            size_hint_y=None,
            height='40dp',
            font_size='18sp',
            bold=True
        )
        self.add_widget(featured_label)
        
        # Featured games scroll
        featured_scroll = ScrollView(size_hint_y=0.4)
        featured_grid = GridLayout(
            cols=1,
            spacing='12dp',
            size_hint_y=None,
            height=600
        )
        featured_grid.bind(minimum_height=featured_grid.setter('height'))
        
        for i in range(3):
            btn = Button(
                text=f'Featured Game {i+1}',
                size_hint_y=None,
                height='150dp',
                background_color=(0.2, 0.4, 0.8, 1)
            )
            featured_grid.add_widget(btn)
        
        featured_scroll.add_widget(featured_grid)
        self.add_widget(featured_scroll)
        
        # Recent games section
        recent_label = Label(
            text='Recently Played',
            size_hint_y=None,
            height='40dp',
            font_size='18sp',
            bold=True
        )
        self.add_widget(recent_label)
        
        # Recent games scroll
        recent_scroll = ScrollView(size_hint_y=0.4)
        recent_grid = GridLayout(
            cols=2,
            spacing='12dp',
            size_hint_y=None
        )
        recent_grid.bind(minimum_height=recent_grid.setter('height'))
        
        for i in range(4):
            btn = Button(
                text=f'Game {i+1}',
                size_hint_y=None,
                height='120dp',
                background_color=(0.2, 0.2, 0.24, 1)
            )
            recent_grid.add_widget(btn)
        
        recent_scroll.add_widget(recent_grid)
        self.add_widget(recent_scroll)
