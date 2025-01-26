
import logging
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
    """ Inserts the drawing of an ant on the given canvas context
    context: context of the canvas where to draw
    pimp_color_legs: legs
    pimp_color_antennae: antennae
    pimp_color_body: body (head, thorax, abdomen)    
    translate: possibility to move the drawing
    scale: scaling factor, <1 to reduce size
    rotation: rotation in radians"""

    context.translate(*translate)
    context.scale(scale, scale)
    context.rotate(rotate)

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


def draw_nest_entrance(
        context,
        to_px,
        x,
        y,
        radius
    ):
    with context.Fill(color='orange') as fill:
        fill.move_to(to_px(x), to_px(y))
        fill.arc(x=to_px(x), y=to_px(y), radius=to_px(radius))


def draw_food(
        context,
        to_px,
        x,
        y
    ):
    with context.Fill(color='blue') as fill:
        fill.move_to(to_px(x), to_px(y))
        fill.arc(x=to_px(x), y=to_px(y), radius=5)


def draw_mini_ant(
        context,
        to_px,
        x,
        y,
        o
    ):
    body_clr = '#9BC3E5'
    contour_clr = '#5B9BD5'
    with context.Context() as sub_context:
        sub_context.translate(to_px(x), to_px(y))
        sub_context.rotate(o-math.pi/4)

        with sub_context.Fill(color=contour_clr) as fill:
            fill.rect(x=0, y=0, width=6, height=6)
        with sub_context.Stroke(color=contour_clr, line_width=1) as fill:
            fill.rect(x=0, y=0, width=6, height=6)
        with sub_context.Fill(color=body_clr) as fill:
            fill.arc(x=5, y=5, radius=5)
        with sub_context.Stroke(color=contour_clr, line_width=1) as fill:
            fill.arc(x=5, y=5, radius=5)
        
        context.append(sub_context)
    
