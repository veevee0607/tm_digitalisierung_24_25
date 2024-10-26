from typing import Tuple, List, Any
from ipycanvas import Canvas, hold_canvas
import numpy as np
import math as m
import time

from ..animation_modules.spring import Spring
from ..animation_modules.shapes import Rectangle
import src.still_modules as still_modules
from ..still_modules import draw_still_frame


def einmassenschwinger(canvas: Canvas):
    canvas[0].stroke_style = "black"
    # make frame for animation
    draw_still_frame(
        canvas=canvas[0],
        padding_width=5,
        padding_height=10,
        width=40,
        height=80,
        width_num_strokes=30,
        height_num_strokes=16,
    )
    # cosmetic line where spring is attached
    mid_point = still_modules.MID_POINT
    canvas[0].line_width = 0.65
    line_endpoint = (mid_point[0] + 5, mid_point[1])
    canvas[0].stroke_line(
        mid_point[0], mid_point[1], line_endpoint[0], line_endpoint[1]
    )

    # add text (static)
    canvas[0].font = "23px euklid"
    canvas[0].fill_text(text="c", x=mid_point[0] + 10, y=mid_point[1] - 30, max_width=6)

    # draw arrow
    center = (mid_point[0] + 50, mid_point[1])
    canvas[0].line_width = 0.9
    canvas[0].font = "21px euklid"
    canvas[0].fill_text("x", center[0] + 6, center[1] - 84, max_width=6)
    draw_arrow(
        canvas=canvas[0],
        x1=center[0],
        y1=center[1] - 80,
        x2=center[0] + 20,
        y2=center[1] - 80,
        base_length=20,
        num_base_strokes=3,
        alpha=30,
        stroke_len=10,
        spacing_padding=3,
        arrow_length=5,
        arrow_angle=40,
    )

    # animate spring and mass
    animate_spring_and_mass(canvas, list(line_endpoint))


def animate_spring_and_mass(canvas: Canvas, spring_anker_point: List[int]):
    # make spring
    end = [spring_anker_point[0] + 10, spring_anker_point[1]]
    spring_obj = Spring(start=spring_anker_point, end=end, nodes=25, width=30)

    # make mass object
    center = (spring_anker_point[0] + 50, spring_anker_point[1])
    height = 50
    mass_obj = U1_1_Rectangle(
        center=center,
        width=80,
        height=height,
        upper_left_corner=(
            spring_anker_point[0] + 5,
            spring_anker_point[1] + height / 2,
        ),
    )

    # calculate dummy solution for animation
    x = np.linspace(0, 1 * np.pi, 100)
    y = list(np.sin(0.2 * x) * 100 + 1.1)
    pos_vec = [(spring_anker_point[0] + 10, spring_anker_point[1])]
    for val in y:
        pos_vec.append((spring_anker_point[0] + 10 + int(val), spring_anker_point[1]))

    # run animation
    canvas[1].line_width = 0.65
    canvas[2].line_width = 0.65
    while True:
        for t, pos in list(zip(x, pos_vec)):
            with hold_canvas():
                spring_obj.animate(canvas=canvas[1], time_vec=t, pos_vec=pos)
            with hold_canvas():
                mass_obj.animate(canvas=canvas[2], time_vec=t, pos_vec=pos)

            time.sleep(0.009)

        pos_vec.reverse()


def draw_arrow(
    canvas,
    x1,
    y1,
    x2,
    y2,
    base_length,
    num_base_strokes=4,
    stroke_len=5,
    spacing_padding=5,
    alpha=30,
    arrow_length=15,
    arrow_angle=30,
):
    # draw main line
    canvas.line_width = 0.9
    canvas.stroke_line(x1, y1, x2, y2)
    # draw base line
    canvas.stroke_line(x1, y1 - base_length / 2, x1, y1 + base_length / 2)

    # add angled lines
    line_space = m.ceil(base_length / num_base_strokes) + spacing_padding
    gamma = 90
    beta = 180 - 90 - alpha
    if alpha + beta + gamma != 180:
        raise NotImplementedError("alpha beta and gamma dont add up to 180")
    # calculate y axis offset
    y_offset = -(stroke_len / m.sin(gamma)) * m.sin(
        alpha
    )  # a = (c/sin(gamma))*sin(alpha)
    # calculate x axis offset
    x_offset = -(stroke_len / m.sin(gamma)) * m.sin(
        beta
    )  # b = (c/sin(gamma))*sin(beta)
    canvas.line_width = 0.5
    temp_start = (x1, y1 - base_length / 2)
    counter = 0
    while (
        counter
        < num_base_strokes  # temp_start[1] < y1 - base_length / 2 + base_length and
    ):
        canvas.stroke_line(
            temp_start[0],
            temp_start[1],
            temp_start[0] - x_offset,
            temp_start[1] - y_offset,
        )
        temp_start = (temp_start[0], temp_start[1] + line_space)
        counter += 1

    # calculate the angle of the line
    angle = m.atan2(y2 - y1, x2 - x1)

    # calculate coordinates for the two arrowhead lines
    arrow_angle_rad = m.radians(arrow_angle)

    x3 = x2 - arrow_length * m.cos(angle - arrow_angle_rad)
    y3 = y2 - arrow_length * m.sin(angle - arrow_angle_rad)

    x4 = x2 - arrow_length * m.cos(angle + arrow_angle_rad)
    y4 = y2 - arrow_length * m.sin(angle + arrow_angle_rad)

    # strke arrow head lines
    canvas.stroke_line(x2, y2, x3, y3)
    canvas.stroke_line(x2, y2, x4, y4)


# overwrite rectangle class to adjust animation method
class U1_1_Rectangle(Rectangle):

    def __init__(
        self,
        center: Tuple[int, int],
        width: int | Any = None,
        height: int | Any = None,
        upper_left_corner: Tuple[int] | Any = None,
    ) -> None:
        super().__init__(center, width, height, upper_left_corner)

    def animate(
        self, canvas: Canvas, time_vec: List[int], pos_vec: List[Tuple[int]]
    ) -> None:
        self.height = 100
        # loop through time vector to animate circle
        # for _, pos in zip(time_vec, pos_vec):
        canvas.fill_style = "#bebebe"  #  #d3d3d3
        canvas.font = "22px euklid"
        with hold_canvas():
            canvas.clear()
            canvas.fill_rect(
                x=pos_vec[0] + 5,
                y=pos_vec[1] - self.height / 2,
                width=self.width,
                height=self.height,
            )
            canvas.stroke_rect(
                x=pos_vec[0] + 5,
                y=pos_vec[1] - self.height / 2,
                width=self.width,
                height=self.height,
            )
            # animate text
            canvas.fill_style = "black"
            canvas.fill_text(
                "m",
                x=pos_vec[0] + self.width / 2,
                y=pos_vec[1] - self.height / 2 + self.height / 2 + 2,
                max_width=8,
            )
