
import math

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from travertino.constants import BOLD

from .drawings import draw_ant


class PimpScreen(toga.Box):
    def __init__(self, settings, game_controls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settings
        self.game_controls = game_controls

        self.color_choices = ['#393A3E', '#422E13', '#7F5F16', '#537636', '#878532', '#DBB95F']
        def get_color_idx(hex_color):
            try:
                return self.color_choices.index(hex_color)
            except:
                return 0

        # Layout elements
        self.top_title = toga.Label(
            f'Hi {self.settings.name}, how are you today?',
            style=Pack(
                padding=(30, 30),
                flex=1,
                font_weight=BOLD,
                font_size=16,
                color='#393A3E',
            )
        )
        self.pimp_canvas = self.generate_pimp_canvas()

        content_box = toga.Box(
            children=[
                self.pimp_canvas,
                toga.Box(
                    children=[
                        toga.Box(
                            style=Pack(direction=ROW, padding=(40,0)),
                            children=[
                                toga.Label('Name', style=Pack(flex=1)),
                                toga.TextInput(
                                    value=self.settings.name,
                                    style=Pack(flex=3),
                                    on_change=self.on_change_name
                                )
                            ],
                        ),
                        toga.Box(
                            style=Pack(direction=ROW),
                            children=[
                                toga.Label('Antennae', style=Pack(flex=1)),
                                toga.Slider(
                                    min=0,
                                    max=len(self.color_choices)-1,
                                    tick_count=len(self.color_choices),
                                    value=get_color_idx(self.settings.pimp_color_antennae),
                                    style=Pack(flex=3),
                                    on_change=self.on_change_antennaecolor
                                    )
                            ]
                        ),
                        toga.Box(
                            style=Pack(direction=ROW),
                            children=[
                                toga.Label('Body', style=Pack(flex=1)),
                                toga.Slider(
                                    min=0,
                                    max=len(self.color_choices)-1,
                                    tick_count=len(self.color_choices),
                                    value=get_color_idx(self.settings.pimp_color_body),
                                    style=Pack(flex=3),
                                    on_change=self.on_change_bodycolor
                                )
                            ]
                        ),
                        toga.Box(
                            style=Pack(direction=ROW),
                            children=[
                                toga.Label('Legs', style=Pack(flex=1)),
                                toga.Slider(
                                    min=0,
                                    max=len(self.color_choices)-1,
                                    tick_count=len(self.color_choices),
                                    value=get_color_idx(self.settings.pimp_color_legs),
                                    style=Pack(flex=3),
                                    on_change=self.on_change_legscolor
                                )
                            ]
                        ),
                        toga.Button(
                            'Back to the game!',
                            style=Pack(padding=30),
                            on_press=self.goto_game
                        )
                    ],
                    style=Pack(flex=3, direction=COLUMN, padding=30)
                )
            ],
            style=Pack(flex=1, direction=ROW)
        )
        
        # Layout assembly
        self.style.update(direction=COLUMN)
        self.add(self.top_title)
        self.add(content_box)


    def draw_on_canvas(self):
        self.pimp_canvas.context.clear()
        self.pimp_canvas_size = (
            self.pimp_canvas.layout.width,
            self.pimp_canvas.layout.height
        )
        draw_ant(
            self.pimp_canvas.context,
            self.settings.pimp_color_legs,
            self.settings.pimp_color_antennae,
            self.settings.pimp_color_body,
            translate=(self.pimp_canvas_size[0]/2, self.pimp_canvas_size[1]/2-60),
            scale=1.2,
            rotate=math.pi/2
        )
    
    # Event handlers
    def on_change_name(self, widget):
        self.top_title.text = f'Hi {widget.value}, how are you today?'
        self.settings.name = widget.value
        self.settings.save()
    
    def on_change_antennaecolor(self, widget):
        self.settings.pimp_color_antennae = self.color_choices[int(widget.value)]
        self.settings.save()
        self.draw_on_canvas()
    
    def on_change_bodycolor(self, widget):
        self.settings.pimp_color_body = self.color_choices[int(widget.value)]
        self.settings.save()
        self.draw_on_canvas()
    
    def on_change_legscolor(self, widget):
        self.settings.pimp_color_legs = self.color_choices[int(widget.value)]
        self.settings.save()
        self.draw_on_canvas()

    def on_press_canvas(self, widget, x, y):
        print(f'Canvas pressed @ {x} x {y}')
    
    def goto_game(self, widget):
        self.game_controls('go to game')

    def generate_pimp_canvas(self):
        """ Generates a background canvas."""     
        canvas = toga.Canvas(
            style=Pack(padding=10, flex=4),
            on_press=self.on_press_canvas,
        )
        return canvas
