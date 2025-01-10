"""
Build Ant One's destiny
"""

import math

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from travertino.constants import BOLD

from .user_settings import UserSettings


def line_segments_gen(points, x_mirror=False):
    """Generator for points in the same continuous segmented line
    points: a list of coordinates for the line
    x_mirror: defines if angles should be reversed to draw other side of the body
    
    Coordinates are in polar form: radius, theta in degrees for convenience
    Points are relative to one another. Theta is in original reference system
    """
    x, y = 0, 0
    for i in range(len(points)):
        x += points[i][0] * math.cos(
            points[i][1] * math.pi/180 * (-1)**(x_mirror)
            )
        y += -points[i][0] * math.sin(
            points[i][1] * math.pi/180 * (-1)**(x_mirror)
            )
        yield round(x), round(y)


class PlayScreen(toga.Box):
    def __init__(self, settings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settings

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
                toga.Label('Side pane')
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


class PimpScreen(toga.Box):
    def __init__(self, settings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settings

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
                padding=(5, 10),
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
                                    style=Pack(flex=2),
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
                                    style=Pack(flex=2),
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
                                    style=Pack(flex=2),
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
                                    style=Pack(flex=2),
                                    on_change=self.on_change_legscolor
                                )
                            ]
                        )
                    ],
                    style=Pack(flex=3, direction=COLUMN, padding=10)
                )
            ],
            style=Pack(flex=1, direction=ROW)
        )
        
        # Layout assembly
        self.style.update(direction=COLUMN)
        self.add(self.top_title)
        self.add(content_box)


    def generate_ant_drawing(self):
        self.pimp_canvas_size = (
            self.pimp_canvas.layout.width,
            self.pimp_canvas.layout.height
        )
        self.draw_ant(
            translate=(self.pimp_canvas_size[0]/2, self.pimp_canvas_size[1]/2-60),
            scale=1.2,
            rotate=math.pi/2
        )
    
    def on_change_name(self, widget):
        self.top_title.text = f'Hi {widget.value}, how are you today?'
        self.settings.name = widget.value
        self.settings.save()
    
    def on_change_antennaecolor(self, widget):
        self.settings.pimp_color_antennae = self.color_choices[int(widget.value)]
        self.settings.save()
        self.draw_ant(scale=1)
    
    def on_change_bodycolor(self, widget):
        self.settings.pimp_color_body = self.color_choices[int(widget.value)]
        self.settings.save()
        self.draw_ant(scale=1)
    
    def on_change_legscolor(self, widget):
        self.settings.pimp_color_legs = self.color_choices[int(widget.value)]
        self.settings.save()
        self.draw_ant(scale=1)

    def generate_pimp_canvas(self):
        """ Generates a background canvas."""     
        canvas = toga.Canvas(
            style=Pack(padding=10, flex=4),#, background_color='beige'),
            on_press=self.on_press_canvas,
        )
        return canvas

    def on_press_canvas(self, widget, x, y):
        print(f'Canvas pressed @ {x} x {y}')
    
    def draw_ant(self, translate=(0, 0), scale=0.2, rotate=0):
        """ Inserts the drawing of an ant on the canvas
        translate: possibility to move the drawing
        scale: scaling factor, <1 to reduce size
        rotation: rotation in radians"""

        self.pimp_canvas.context.translate(*translate)
        self.pimp_canvas.context.scale(scale, scale)
        self.pimp_canvas.context.rotate(rotate)

        def get_line_width(at_scale_1, scale):
            return scale*at_scale_1
        
        # Draw legs
        leg_points = {
            'top': [(35, 0), (45, 90), (50, 150)],
            'mid': [(45, 0), (50, 80), (50, 30)],
            'back': [(60, 0), (40, 60), (50, 20)]
        }
        with self.pimp_canvas.context.Stroke(0, 0, color=self.settings.pimp_color_legs, line_width=get_line_width(5, scale)) as stroke, self.pimp_canvas.context.Fill(color=self.settings.pimp_color_legs) as fill:
            for leg in leg_points.keys():
                for i, coords in enumerate(line_segments_gen(leg_points[leg])):
                    if i == 0:
                        stroke.move_to(*coords)
                    else:
                        stroke.line_to(*coords)
                        fill.move_to(*coords)
                        fill.arc(*coords, radius=4)
                for i, coords in enumerate(line_segments_gen(leg_points[leg], x_mirror=True)):
                    if i == 0:
                        stroke.move_to(*coords)
                    else:
                        stroke.line_to(*coords)
                        fill.move_to(*coords)
                        fill.arc(*coords, radius=4)

        # Draw antennae
        antenna_points = {
            '_': [(0, 0), (30, 90+45), (30, 160)]
        }
        with self.pimp_canvas.context.Stroke(0, 0, color=self.settings.pimp_color_antennae, line_width=get_line_width(2, scale)) as stroke:
            for i, coords in enumerate(line_segments_gen(antenna_points['_'])):
                if i == 0:
                    stroke.move_to(*coords)
                else:
                    stroke.line_to(*coords)
                    fill.move_to(*coords)
            for i, coords in enumerate(line_segments_gen(antenna_points['_'], x_mirror=True)):
                if i == 0:
                    stroke.move_to(*coords)
                else:
                    stroke.line_to(*coords)
                    fill.move_to(*coords)

        # Draw body
        head1_st = (0, -20)
        head1_end = (0, 20)
        head1_cp1 = (-30, -10)
        head1_cp2 = (-30, 10)
        head2_st = (0, -20)
        head2_end = (0, 20)
        head2_cp1 = (25, -25)
        head2_cp2 = (25, 25)
        with self.pimp_canvas.context.Fill(color=self.settings.pimp_color_body) as fill:
            # Head
            fill.move_to(*head1_st)
            fill.bezier_curve_to(*head1_cp1, *head1_cp2, *head1_end)
            fill.move_to(*head2_st)
            fill.bezier_curve_to(*head2_cp1, *head2_cp2, *head2_end)
            # Thorax
            fill.move_to(45, 0)
            fill.ellipse(x=45, y=0, radiusx=30, radiusy=12)
            # Abdomen
            fill.move_to(70, 0)
            fill.quadratic_curve_to(95, -50, 140, 0)
            fill.move_to(70, 0)
            fill.quadratic_curve_to(95, 50, 140, 0)


class AntOne(toga.App):
    def startup(self):
        """Construct and show the Toga application.
        """
        # Apps parameters
        self.app_size = (640, 480)

        # User settings
        user_setting_path = self.paths.data / 'user_settings.pkl'
        settings = UserSettings(user_setting_path)

        # Screens
        self.playscreen = PlayScreen(settings)
        self.pimpscreen = PimpScreen(settings)

        # Layout assembly
        self.main_window = toga.Window(
            title=self.formal_name,
            size=self.app_size,
            resizable=False
        )
        self.main_window.content = self.playscreen
        self.main_window.show()
        self.pimpscreen.generate_ant_drawing()
    

def main():
    return AntOne()
