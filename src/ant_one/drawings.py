
import math


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


def draw_ant(
        context,
        pimp_color_legs,
        pimp_color_antennae,
        pimp_color_body,
        translate=(0, 0), 
        scale=0.2, 
        rotate=0
    ):
    """ Inserts the drawing of an ant on the canvas
    translate: possibility to move the drawing
    scale: scaling factor, <1 to reduce size
    rotation: rotation in radians"""

    context.translate(*translate)
    context.scale(scale, scale)
    context.rotate(rotate)
    # self.pimp_canvas.context.translate(*translate)
    # self.pimp_canvas.context.scale(scale, scale)
    # self.pimp_canvas.context.rotate(rotate)

    def get_line_width(at_scale_1, scale):
        return scale*at_scale_1
    
    # Draw legs
    leg_points = {
        'top': [(35, 0), (45, 90), (50, 150)],
        'mid': [(45, 0), (50, 80), (50, 30)],
        'back': [(60, 0), (40, 60), (50, 20)]
    }
    with (
        context.Stroke(
            0, 0, color=pimp_color_legs, line_width=get_line_width(5, scale)
        ) as stroke,
        context.Fill(
            color=pimp_color_legs
        ) as fill
    ):
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
    with context.Stroke(0, 0, color=pimp_color_antennae, line_width=get_line_width(2, scale)) as stroke:
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
    with context.Fill(color=pimp_color_body) as fill:
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