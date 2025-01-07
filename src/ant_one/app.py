"""
Build Ant One's destiny
"""

import math

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class PlayScreen(toga.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Layout elements
        title = toga.Label('Ant One', style=Pack(padding=5, flex=1))
        self.bg_canvas = self.generate_bg_canvas()
        
        # Layout assembly
        self.style.update(direction=COLUMN)
        self.add(title)
        self.add(self.bg_canvas)

    def generate_bg_canvas(self):
        """ Generates a background canvas."""     
        canvas = toga.Canvas(
            style=Pack(padding=10, flex=4, background_color='beige'),
            on_press=self.on_press_canvas,
        )
        return canvas

    def on_press_canvas(self, widget, x, y):
        print(f'Canvas pressed @ {x} x {y}')


class PimpScreen(toga.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Layout elements
        title = toga.Label('Pimp my ant', style=Pack(padding=5, flex=1))
        self.bg_canvas = self.generate_pimp_canvas()
        
        # Layout assembly
        self.style.update(direction=COLUMN)
        self.add(title)
        self.add(self.bg_canvas)

    def generate_pimp_canvas(self):
        """ Generates a background canvas."""     
        canvas = toga.Canvas(
            style=Pack(padding=10, flex=4, background_color='beige'),
            on_press=self.on_press_canvas,
        )
        return canvas

    def on_press_canvas(self, widget, x, y):
        print(f'Canvas pressed @ {x} x {y}')


class AntOne(toga.App):
    def startup(self):
        """Construct and show the Toga application.
        """
        # Apps parameters
        self.app_size = (640, 480)

        # Screens
        self.playscreen = PlayScreen()
        self.pimpscreen = PimpScreen()

        # Layout assembly
        self.main_window = toga.MainWindow(
            title=self.formal_name,
            size=self.app_size,
            resizable=False
        )
        self.main_window.content = self.pimpscreen
        self.main_window.show()
    

def main():
    return AntOne()
