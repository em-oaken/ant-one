
import logging
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .game_resources import World, Ant, Colony, Nest, Food, ConstructionMaterial
from .drawings import draw_nest_entrance, draw_mini_ant


class PlayScreen(toga.Box):
    def __init__(self, settings, game_controls, tau, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settings
        self.game_controls = game_controls
        self.tau = tau
        self.build_interface()
        logging.info('Built interface of play screen')

    def initialize_game_engine(self):
        self.world = World(
            tau=self.tau,
            px_size=(
                self.canvas.layout.width,
                self.canvas.layout.height
            )
        )
        self.nest = Nest(self.world)
        self.colony = Colony(self.nest)
        self.colony.populate(10)
        
        self.tau.add_world(self.world)
        self.tau.add_render(self.render)
        logging.info('Game initialised')

    def render(self):
        context = self.canvas.context
        context.clear()
        
        for object in self.world.nonliving_objects:
            object.draw(context, self.world.to_px)

        for ant in self.colony.population:
            draw_mini_ant(context, self.world.to_px, ant.x, ant.y, ant.o)
        
        # Update top bar
        self.top_bar_infos[0].text = f'{self.tau.loopno:04}  |  {self.tau.game_duration:.2f}s'
        self.top_bar_infos[1].text = f'Day {self.tau.vtime:%d %H:%M:%S}'
        self.top_bar_infos[2].text = f'{len(self.colony.population)} ants'
        self.top_bar_infos[4].text = f'{1/self.tau.rt_loop_duration.total_seconds():.0f} fps'

    # Event handlers
    def on_press_canvas(self, widget, x, y):
        logging.info(f'Canvas pressed @ {x} x {y}')
    
    def goto_pimp(self, widget):
        self.game_controls('go to pimp')
    
    def on_change_speedoftime(self, widget):
        new_speedoftime = self.tau.speeds_of_time[int(widget.value)]
        self.tau.time_factor = new_speedoftime
        self.time_control_lbl.value = f'Time x{self.tau.time_factor}'
    
    # Interface
    def build_interface(self):
        # Top bar
        self.top_bar_infos = [toga.Label('...', style=Pack(flex=1)) for _ in range(5)]
        top_bar = toga.Box(children=self.top_bar_infos, style=Pack(direction=ROW))

        # Main canvas
        self.canvas = toga.Canvas(
            style=Pack(padding=10, flex=15, background_color='#E9F0CF'),
            on_press=self.on_press_canvas,
        )

        # Side pane
        self.time_control_lbl = toga.Label('Time control', style=Pack(padding=15))
        time_slider = toga.Slider(
            value=0,
            min=0,
            max=len(self.tau.speeds_of_time)-1,
            tick_count=len(self.tau.speeds_of_time),
            on_change=self.on_change_speedoftime,
            style=Pack(direction=ROW, flex=1, padding=(10, 5, 0, 5))
        )
        time_slider_labels = toga.Box(
            children=[
                toga.Label(f'x{speed}', style=Pack(flex=1, text_align='center'))
                for speed in self.tau.speeds_of_time
            ],
            style=Pack(direction=ROW, flex=1, padding=(0, 0, 10, 0))
        )
        time_control_block = toga.Box(
            children=[self.time_control_lbl, time_slider, time_slider_labels],
            style=Pack(direction=COLUMN, flex=6)
        )
        config_block = toga.Box(
            children=[toga.Button('Pimp '+self.settings.name, on_press=self.goto_pimp)],
            style=Pack(direction=COLUMN, flex=3)
        )
        side_pane = toga.Box(
            children=[
                toga.Box(style=Pack(flex=1)),
                toga.Divider(),
                time_control_block,
                toga.Divider(),
                config_block
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

