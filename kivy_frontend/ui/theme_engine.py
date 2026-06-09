"""
Material You theme engine for Pixel Edition
"""

from kivy.core.window import Window


class MaterialYouTheme:
    """
    Material You dynamic theming system
    """
    
    # Material You color palette (Pixel default)
    COLORS = {
        'primary': (0.40, 0.60, 1.00, 1.0),
        'primary_container': (0.20, 0.45, 0.95, 1.0),
        'secondary': (0.80, 0.60, 0.95, 1.0),
        'secondary_container': (0.70, 0.50, 0.90, 1.0),
        'tertiary': (0.95, 0.80, 0.50, 1.0),
        'surface': (0.10, 0.10, 0.12, 1.0),
        'surface_dim': (0.08, 0.08, 0.10, 1.0),
        'surface_bright': (0.20, 0.20, 0.22, 1.0),
        'on_surface': (0.95, 0.95, 0.95, 1.0),
        'on_primary': (1.0, 1.0, 1.0, 1.0),
        'error': (1.0, 0.40, 0.40, 1.0),
        'outline': (0.50, 0.50, 0.55, 1.0),
    }
    
    SPACING = {
        'xs': '4dp',
        'sm': '8dp',
        'md': '12dp',
        'lg': '16dp',
        'xl': '24dp',
    }
    
    def __init__(self):
        self.current_colors = self.COLORS.copy()
        Window.clearcolor = self.COLORS['surface']
    
    def get_color(self, name: str):
        """Get a color from the theme"""
        return self.current_colors.get(name, self.COLORS['surface'])
    
    def get_spacing(self, size: str):
        """Get spacing value"""
        return self.SPACING.get(size, '12dp')
