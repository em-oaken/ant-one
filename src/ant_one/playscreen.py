
import logging
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .game_resources import World, Ant, Colony, Nest, Food, ConstructionMaterial
from .drawings import draw_nest, draw_mini_ant


class PlayScreen(toga.Box):
    def __init__(self, settings, game_controls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settings
        self.game_controls = game_controls
        self.build_interface()
        logging.info('Built interface of play screen')

    def initialize_game_engine(self):
        self.world = World(
            px_size=(
                self.canvas.layout.width,
                self.canvas.layout.height
            )
        )
        self.nest = Nest(self.world)
        self.colony = Colony(self.nest)
        self.colony.populate(5)
        self.render()
        logging.info('Game initialised')


    def render(self):
        context = self.canvas.context
        context.clear()
        draw_nest(context, self.world.to_px, self.nest.x, self.nest.y, self.nest.radius)
        for ant in self.colony.population:
            draw_mini_ant(context, self.world.to_px, ant.x, ant.y, ant.o)

    # Event handlers
    def on_press_canvas(self, widget, x, y):
        logging.info(f'Canvas pressed @ {x} x {y}')
    
    def goto_pimp(self, widget):
        self.game_controls('go to pimp')
    
    # Interface
    def build_interface(self):
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
        self.canvas = toga.Canvas(
            style=Pack(padding=10, flex=15, background_color='#E9F0CF'),
            on_press=self.on_press_canvas,
        )
        side_pane = toga.Box(
            children=[
                toga.Label('Side pane'),
                toga.Button(
                    'Pimp '+self.settings.name,
                    on_press=self.goto_pimp
                )
            ],
            style=Pack(flex=1, direction=COLUMN)
        )

        # Layout assembly
        main_box = toga.Box(
            style=Pack(direction=ROW, flex=1),
            children=[
                toga.Box(
                    children=[top_bar, self.canvas],
                    style=Pack(direction=COLUMN, flex=3)
                ),
                side_pane
            ]
        )
        
        self.style.update(direction=COLUMN)
        self.add(main_box)

