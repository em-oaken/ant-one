"""
Build Ant One's destiny
"""


import toga

from .playscreen import PlayScreen
from .pimpscreen import PimpScreen
from .user_settings import UserSettings


class AntOne(toga.App):
    def startup(self):
        """Construct and show the Toga application.
        """
        # Apps parameters
        self.app_size = (1000, 600)
        self.screen_size = self.screens[0].size

        if self.app_size[0] > self.screen_size[0] or self.app_size[1] > self.screen_size[1]:
            return 'Program terminated due to screen too small'
        app_posx = (self.screen_size[0]-self.app_size[0])/2
        app_posy = (self.screen_size[1]-self.app_size[1])/2

        # User settings
        user_setting_path = self.paths.data / 'user_settings.pkl'
        settings = UserSettings(user_setting_path)

        # Screens
        self.playscreen = PlayScreen(settings, self.game_controls)
        self.pimpscreen = PimpScreen(settings, self.game_controls)

        # Layout assembly
        self.main_window = toga.Window(
            title=self.formal_name,
            size=self.app_size,
            resizable=False,
            position=(app_posx, app_posy)
        )
        self.main_window.content = self.pimpscreen  # Required to ensure canvas size is not 0x0
        self.main_window.content = self.playscreen
        self.main_window.show()
        self.pimpscreen.draw_on_canvas()

    def game_controls(self, what):
        match what:
            case 'go to pimp':
                self.main_window.content = self.pimpscreen
            case 'go to game':
                self.main_window.content = self.playscreen
            case _:
                print('Action not defined')

    

def main():
    return AntOne()
