"""
Build Ant One's destiny
"""


import logging
import toga

from .playscreen import PlayScreen
from .pimpscreen import PimpScreen
from .user_settings import UserSettings
from .tau import Tau


logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO
    )


class AntOne(toga.App):
    def startup(self):
        """Construct and show the Toga application.
        """
        # Apps parameters
        self.app_size = (1000, 600)
        self.screen_size = self.screens[0].size

        if self.app_size[0] > self.screen_size[0] or self.app_size[1] > self.screen_size[1]:
            logging.critical('Program terminated due to screen too small')
            return
        app_posx = (self.screen_size[0]-self.app_size[0])/2
        app_posy = (self.screen_size[1]-self.app_size[1])/2

        # User settings
        user_setting_path = self.paths.data / 'user_settings.pkl'
        self.settings = UserSettings(user_setting_path)

        # Screens
        self.playscreen_is_open = False
        self.pimpscreen_is_open = False

        # Time engine
        self.tau = Tau()

        # Layout assembly
        self.main_window = toga.Window(
            title=self.formal_name,
            size=self.app_size,
            resizable=False,
            position=(app_posx, app_posy)
        )
        self.app_controls('go to game')
        self.main_window.show()

    def app_controls(self, request):
        match request:
            case 'go to pimp':
                if not self.pimpscreen_is_open:
                    self.pimpscreen = PimpScreen(self.settings, self.app_controls)
                    self.pimpscreen_is_open = True
                self.main_window.content = self.pimpscreen
                self.pimpscreen.draw_on_canvas()

            case 'go to game':
                if not self.playscreen_is_open:
                    self.playscreen = PlayScreen(self.settings, self.app_controls, self.tau)
                    self.playscreen_is_open = True
                    self.main_window.content = self.playscreen
                    self.playscreen.initialize_game_engine()
                else:
                    self.main_window.content = self.playscreen

            case _:
                logging.critical('Action not defined')
    
    async def on_running(self, **kwargs):
        await self.tau.event_loop_manager()

    
def main():
    return AntOne()

if __name__ == "__main__":
    app = main()
    app.main_loop()
