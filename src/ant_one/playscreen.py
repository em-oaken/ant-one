
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class PlayScreen(toga.Box):
    def __init__(self, settings, game_controls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settings
        self.game_controls = game_controls

        # Layout elements
        top_bar = toga.Box(
            children=[
                toga.Label('Time info', style=Pack(flex=1)),
                toga.Label('Population info', style=Pack(flex=1)),
                toga.Label('Resource info', style=Pack(flex=1)),
                toga.Label('Other info', style=Pack(flex=1)),
                toga.Label('Other info', style=Pack(flex=1)),
                ],
            style=Pack(direction=ROW)
        )
        self.bg_canvas = self.generate_bg_canvas()
        side_pane = toga.Box(
            children=[
                toga.Label('Side pane'),
                toga.Button(
                    'Pimp '+settings.name,
                    on_press=self.goto_pimp
                )
            ],
            style=Pack(flex=1, direction=COLUMN)
        )

        content_box = toga.Box(
            style=Pack(direction=ROW, flex=10),
            children=[
                toga.Box(
                    children=[
                        top_bar,
                        self.bg_canvas,
                    ],
                    style=Pack(direction=COLUMN, flex=3)
                ),
                side_pane
            ]
        )
        
        # Layout assembly
        self.style.update(direction=COLUMN)
        self.add(content_box)

    def generate_bg_canvas(self):
        """ Generates a background canvas."""     
        canvas = toga.Canvas(
            style=Pack(padding=10, flex=15, background_color='#E9F0CF'),
            on_press=self.on_press_canvas,
        )
        return canvas

    def on_press_canvas(self, widget, x, y):
        print(f'Canvas pressed @ {x} x {y}')
    
    def goto_pimp(self, widget):
        self.game_controls('go to pimp')
