"""
Build Ant One's destiny
"""

import math

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


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
        title = toga.Label('Pimp my ant', style=Pack(padding=5, flex=1))
        self.pimp_canvas = self.generate_pimp_canvas()
        self.draw_ant()
        
        # Layout assembly
        self.style.update(direction=COLUMN)
        self.add(title)
        self.add(self.pimp_canvas)

    def generate_pimp_canvas(self):
        """ Generates a background canvas."""     
        canvas = toga.Canvas(
            style=Pack(padding=10, flex=4, background_color='beige'),
            on_press=self.on_press_canvas,
        )
        return canvas

    def on_press_canvas(self, widget, x, y):
        print(f'Canvas pressed @ {x} x {y}')
    
    def draw_ant(self):
        self.pimp_canvas.context.translate(200, 200)
        self.pimp_canvas.context.rotate(0)

        ant_color = '#393A3E'
        
        # Draw body
        with self.pimp_canvas.context.Fill(color=ant_color) as fill:
            ant_head = fill.ellipse(x=0, y=0, radiusx=20, radiusy=18)  # Head
        # with self.pimp_canvas.context.Fill(color="black") as fill:
            ant_body = fill.ellipse(x=45, y=0, radiusx=30, radiusy=10)  # Mesosoma / Thorax
        # with self.pimp_canvas.context.Fill(color="black") as fill:
            ant_tail = fill.ellipse(x=110, y=0, radiusx=40, radiusy=20)  # Metasoma / Abdomen
        
        # Draw legs
        leg_points = {
            'top': [(35, 0), (45, 90), (50, 150)],
            'mid': [(45, 0), (50, 80), (50, 30)],
            'back': [(60, 0), (40, 60), (50, 20)]
        }
        
        with self.pimp_canvas.context.Stroke(0, 0, color=ant_color, line_width=5) as stroke, self.pimp_canvas.context.Fill(color=ant_color) as fill:
            for leg in ['top', 'mid', 'back']:
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
        
        with self.pimp_canvas.context.Stroke(0, 0, color=ant_color, line_width=2) as stroke:
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
    

def main():
    return AntOne()
