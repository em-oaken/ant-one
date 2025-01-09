"""
Build Ant One's destiny
"""

import math

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from travertino.constants import BOLD


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
        title_box = toga.Box(
            children=[
                toga.Label(
                    'Pimp my ant',
                    style=Pack(
                        padding=(5, 20),
                        flex=1,
                        font_weight=BOLD,
                        font_size=18,
                        color='#393A3E',
                    )
                )
            ]
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
                                toga.Label('Name:', style=Pack(flex=1)),
                                toga.TextInput(style=Pack(flex=2))
                            ],
                        ),
                        toga.Box(
                            style=Pack(direction=ROW),
                            children=[
                                toga.Label('Antennae', style=Pack(flex=1)),
                                toga.Slider(min=0, max=4, tick_count=5, style=Pack(flex=2))
                            ]
                        ),
                        toga.Box(
                            style=Pack(direction=ROW),
                            children=[
                                toga.Label('Body', style=Pack(flex=1)),
                                toga.Slider(min=0, max=4, tick_count=5, style=Pack(flex=2))
                            ]
                        ),
                        toga.Box(
                            style=Pack(direction=ROW),
                            children=[
                                toga.Label('Legs', style=Pack(flex=1)),
                                toga.Slider(min=0, max=4, tick_count=5, style=Pack(flex=2))
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
        self.add(title_box)
        self.add(content_box)


    def on_screen_opened(self):
        self.pimp_canvas_size = (
            self.pimp_canvas.layout.width,
            self.pimp_canvas.layout.height
        )
        self.draw_ant(
            scale=1.2,
            translate=(self.pimp_canvas_size[0]/2, self.pimp_canvas_size[1]/2-60),
            rotate=math.pi/2
        )

    def generate_pimp_canvas(self):
        """ Generates a background canvas."""     
        canvas = toga.Canvas(
            style=Pack(padding=10, flex=4),#, background_color='beige'),
            on_press=self.on_press_canvas,
        )
        return canvas

    def on_press_canvas(self, widget, x, y):
        print(f'Canvas pressed @ {x} x {y}')
    
    def draw_ant(self, scale=0.2, translate=(0, 0), rotate=0):
        self.pimp_canvas.context.translate(*translate)
        self.pimp_canvas.context.scale(scale, scale)
        self.pimp_canvas.context.rotate(rotate)

        ant_color = '#393A3E'

        def get_line_width(at_scale_1, scale):
            return scale*at_scale_1
        
        # Draw body
        head1_st = (0, -20)
        head1_end = (0, 20)
        head1_cp1 = (-30, -10)
        head1_cp2 = (-30, 10)
        head2_st = (0, -20)
        head2_end = (0, 20)
        head2_cp1 = (25, -25)
        head2_cp2 = (25, 25)
        with self.pimp_canvas.context.Fill(color=ant_color) as fill:
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
        
        # Draw legs
        leg_points = {
            'top': [(35, 0), (45, 90), (50, 150)],
            'mid': [(45, 0), (50, 80), (50, 30)],
            'back': [(60, 0), (40, 60), (50, 20)]
        }
        with self.pimp_canvas.context.Stroke(0, 0, color=ant_color, line_width=get_line_width(5, scale)) as stroke, self.pimp_canvas.context.Fill(color=ant_color) as fill:
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
        with self.pimp_canvas.context.Stroke(0, 0, color=ant_color, line_width=get_line_width(2, scale)) as stroke:
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
        self.pimpscreen.on_screen_opened()
    

def main():
    return AntOne()
