"""
Game library screen - Browse all games
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


class LibraryScreen(BoxLayout):
    """
    Game library browser
    """
    
    def __init__(self, app=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app = app
        self.padding = '12dp'
        self.spacing = '12dp'
        
        # Search bar
        search_layout = BoxLayout(size_hint_y=0.08, spacing='8dp')
        
        self.search_input = TextInput(
            hint_text='Search games...',
            multiline=False,
            size_hint_x=0.85
        )
        search_layout.add_widget(self.search_input)
        
        search_btn = Button(text='🔍', size_hint_x=0.15, font_size='20sp')
        search_layout.add_widget(search_btn)
        
        self.add_widget(search_layout)
        
        # Filter buttons
        filter_layout = BoxLayout(size_hint_y=0.08, spacing='8dp')
        
        for filter_name in ['All', 'PS1', 'PS2', 'PSP', 'Arcade', 'Favorites']:
            btn = Button(text=filter_name, size_hint_x=1/6)
            filter_layout.add_widget(btn)
        
        self.add_widget(filter_layout)
        
        # Library grid
        library_scroll = ScrollView()
        library_grid = GridLayout(
            cols=3,
            spacing='12dp',
            size_hint_y=None,
            padding='12dp'
        )
        library_grid.bind(minimum_height=library_grid.setter('height'))
        
        for i in range(12):
            game_btn = Button(
                text=f'Game {i+1}',
                size_hint_y=None,
                height='200dp',
                background_color=(0.2, 0.2, 0.24, 1)
            )
            library_grid.add_widget(game_btn)
        
        library_scroll.add_widget(library_grid)
        self.add_widget(library_scroll)
