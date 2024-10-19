from typing import Tuple, List
from ipycanvas import Canvas, hold_canvas
import numpy as np
import math as m
import copy
import sys, os
import time

from ..animation_modules.spring import Spring
from ..animation_modules.shapes import Rectangle


def einmassenschwinger(canvas: Canvas):
    # set markers for frame
    horizontal_start = canvas.width / 20
    vertical_start = canvas.height / 20
    vertical_length = canvas.height - 4 * (canvas.height / 20)
    horizontal_length = canvas.width - 2 * (canvas.width / 20)
    vertical_start_point = (horizontal_start, vertical_start)
    vertical_end_point = (horizontal_start, vertical_start + vertical_length)
    horizontal_end_point = (
        horizontal_start + horizontal_length,
        vertical_start + vertical_length,
    )
    mid_point = (horizontal_start, vertical_start + vertical_length / 2)

    # make frame
    make_frame(
        canvas,
        horizontal_start,
        vertical_start,
        vertical_length,
        horizontal_length,
        vertical_start_point,
        vertical_end_point,
        horizontal_end_point,
        mid_point,
    )

    # animate spring
    animate_spring_and_mass(canvas, list(mid_point))


def make_frame(
    canvas: Canvas,
    horizontal_start,
    vertical_start,
    vertical_length,
    horizontal_length,
    vertical_start_point,
    vertical_end_point,
    horizontal_end_point,
    mid_point,
):
    # make rectangular frame in the middle of canvas
    canvas[0].line_width = 1.0
    canvas[0].stroke_style = "black"

    canvas[0].stroke_lines(
        [
            vertical_start_point,
            mid_point,
            vertical_end_point,
            horizontal_end_point,
        ]
    )

    # add angled strokes to frame
    stroke_length = 15
    beta = 60
    alpha = 30
    gamma = 90
    num_strokes = int(canvas[0].height / 8)
    horizontal_num_strokes = int(canvas[0].width / 32)

    # calculate y axis offset
    # a = (c/sin(gamma))*sin(alpha)
    y_offset = -(stroke_length / m.sin(gamma)) * m.sin(alpha)
    # calculate x axis offset
    # b = (c/sin(gamma))*sin(beta)
    x_offset = -(stroke_length / m.sin(gamma)) * m.sin(beta)

    # move down the vertical line and add strokes
    temp_start = (vertical_start_point[0], vertical_start_point[0] + 5)
    temp_vertical_start = copy.deepcopy(vertical_start)
    canvas[0].line_width = 0.5
    while temp_vertical_start + 20 <= vertical_start + vertical_length:
        canvas[0].stroke_line(
            temp_start[0],
            temp_start[1],
            temp_start[0] - x_offset,
            temp_start[1] + y_offset,
        )

        temp_vertical_start += num_strokes
        temp_start = (temp_start[0], temp_start[1] + num_strokes)

    # # move down horizontal line and add strokes
    temp_start = (horizontal_start, vertical_start + vertical_length)
    temp_horizontal_start = copy.deepcopy(horizontal_start)
    while temp_horizontal_start + 20 <= horizontal_start + horizontal_length:
        canvas[0].stroke_line(
            temp_start[0],
            temp_start[1],
            temp_start[0] - x_offset,
            temp_start[1] + y_offset,
        )

        temp_horizontal_start += horizontal_num_strokes
        temp_start = (temp_start[0] + horizontal_num_strokes, temp_start[1])


def animate_spring_and_mass(canvas: Canvas, spring_anker_point: List[int]):
    # make spring
    end = [spring_anker_point[0] + 10, spring_anker_point[1]]
    spring_obj = Spring(start=spring_anker_point, end=end, nodes=15, width=50)

    # make mass object
    center = (spring_anker_point[0] + 50, spring_anker_point[1])
    mass_obj = Rectangle(
        center=center,
        width=100,
        height=50,
        upper_left_corner=(spring_anker_point[0], spring_anker_point[1] + 25),
    )

    # calculate dummy solution for animation
    x = np.linspace(0, 1 * np.pi, 100)
    y = list(np.sin(0.1 * x) * 100 + 1.1)
    pos_vec = [(spring_anker_point[0] + 10, spring_anker_point[1])]
    for val in y:
        pos_vec.append((spring_anker_point[0] + 10 + int(val), spring_anker_point[1]))

    # run animation
    canvas[1].line_width = 0.65
    while True:
        for t, pos in list(zip(x, pos_vec)):
            with hold_canvas():
                spring_obj.animate(canvas=canvas[1], time_vec=t, pos_vec=pos)

            with hold_canvas():
                mass_obj.animate(canvas=canvas[2], time_vec=t, pos_vec=pos)

            time.sleep(0.02)
        pos_vec.reverse()
