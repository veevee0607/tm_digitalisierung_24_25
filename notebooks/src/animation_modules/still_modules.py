import copy
from typing import Tuple, Any
from ipycanvas import Canvas
import math as m

from src.utils.helper import abs_value

"""Module containing functions to draw still objects.
    Note:  All lengths and distances should be passed as percentage of
        either canvas.width or canvas.height.
"""
MID_POINT: Tuple[int, int]


def draw_still_frame(
    canvas: Canvas,
    padding_width: int,
    padding_height: int,
    width: int,
    height: int,
    stroke_length: int = 15,
    width_num_strokes: int = 30,
    height_num_strokes: int = 15,
    alpha_height: int = 30,
    alpha_width: int = 30,
):
    """Function to draw a still frame for animations of mechanical/oscillating
        systems. All lengths and distances should be passed as percentage of
        either canvas.width or canvas.height.

    Args:
        canvas (Canvas): Canvas to draw on.
        padding_width (int): Distance between border of canvas and frame on
            horizontal axis.
        padding_height (int): Distance between border of canvas and frame on
            vertical axis.
        width (int): Width of the frame.
        height (int): Height of the frame.
        stroke_length (int, optional): Length of strokes on left side of frame.
            Defaults to 15.
        width_num_strokes (int, optional): Number of strokes on horizontal axis
            of frame. Defaults to 30.
        height_num_strokes (int, optional): Number of strokes on vertical axis
            of frame. Defaults to 15.
        alpha_height (int, optional): Angle of strokes on vertical axis.
            Defaults to 30.
        alpha_width (int, optional): Angle of strokes on horizontal axis.
            Defaults to 30.

    Raises:
        NotImplementedError: _description_
        NotImplementedError: _description_
    """
    # padding absolute values
    p_w_abs = abs_value(canvas.width, padding_width)
    p_h_abs = abs_value(canvas.height, padding_height)

    # width and height absolute values
    w_abs = abs_value(canvas.width, width)
    h_abs = abs_value(canvas.height, height)

    # define points in 2d space
    h_start_point = (p_w_abs, p_h_abs)
    h_end_point = (p_w_abs, p_h_abs + h_abs)
    w_end_point = (p_w_abs + w_abs, p_h_abs + h_abs)

    # midpoint to use later
    global MID_POINT
    MID_POINT = (p_w_abs, p_h_abs + h_abs / 2)

    # draw frame
    canvas.stroke_lines(
        [
            h_start_point,
            h_end_point,
            w_end_point,
        ]
    )

    # add angled strokes to frame
    gamma = 90
    beta_height = 180 - gamma - alpha_height
    if alpha_height + beta_height + gamma != 180:
        raise NotImplementedError("alpha beta and gamma dont add up to 180")

    # calculate y axis offset
    y_offset_height = -(stroke_length / m.sin(gamma)) * m.sin(
        alpha_height
    )  # a = (c/sin(gamma))*sin(alpha)

    # calculate x axis offset
    x_offset_height = -(stroke_length / m.sin(gamma)) * m.sin(
        beta_height
    )  # b = (c/sin(gamma))*sin(beta)

    # move down the vertical line and add strokes
    temp_start = (h_start_point[0], h_start_point[0])
    temp_vertical_start = copy.deepcopy(p_h_abs)
    # calculate space between strokes
    height_stroke_space = int(h_abs / height_num_strokes)
    width_stroke_space = int(w_abs / width_num_strokes)
    counter = 0
    # set line width to 0.5 for strokes
    canvas.line_width = 0.5
    while (
        temp_vertical_start < p_h_abs + h_abs - width_stroke_space
        and counter < height_num_strokes
    ):
        canvas.stroke_line(
            temp_start[0],
            temp_start[1],
            temp_start[0] - x_offset_height,
            temp_start[1] + y_offset_height,
        )

        temp_vertical_start += height_stroke_space
        temp_start = (temp_start[0], temp_start[1] + height_stroke_space)
        counter += 1

    beta_width = 180 - gamma - alpha_width
    if alpha_width + beta_width + gamma != 180:
        raise NotImplementedError("alpha beta and gamma dont add up to 180")

    # calculate y axis offset
    y_offset_width = -(stroke_length / m.sin(gamma)) * m.sin(
        alpha_width
    )  # a = (c/sin(gamma))*sin(alpha)

    # calculate x axis offset
    x_offset_width = -(stroke_length / m.sin(gamma)) * m.sin(
        beta_width
    )  # b = (c/sin(gamma))*sin(beta)

    # move down horizontal line and add strokes
    temp_start = (h_end_point[0], h_end_point[1])
    temp_horizontal_start = copy.deepcopy(p_w_abs)
    counter = 0
    while temp_horizontal_start < p_w_abs + w_abs and counter < width_num_strokes:
        canvas.stroke_line(
            temp_start[0],
            temp_start[1],
            temp_start[0] - x_offset_width,
            temp_start[1] + y_offset_width,
        )

        temp_horizontal_start += width_stroke_space
        temp_start = (temp_start[0] + width_stroke_space, temp_start[1])


def draw_arrow(
    canvas: Canvas,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    base_length: int,
    num_base_strokes: int = 4,
    stroke_len: int = 5,
    spacing_padding: int = 5,
    alpha: int = 30,
    arrow_length: int = 15,
    arrow_angle: int = 30,
    description: str | Any = None,
    description_padding_x: int | Any = None,
    description_padding_y: int | Any = None,
    description_font_size: int | Any = None,
    description_max_width: int | Any = None,
):
    """Function to draw an arrow with a base and optional description.

    Args:
        canvas (Canvas): Canvas to draw on.
        x1 (int): X value of arrow starting point.
        y1 (int): Y value of arrow starting point.
        x2 (int): X value of arrow end point.
        y2 (int): Y value of arrow end point.
        base_length (int): Length of arrow base.
        num_base_strokes (int, optional): Number of strokes
            on arrow base. Defaults to 4.
        stroke_len (int, optional): Length of strokes
            on arrow base. Defaults to 5.
        spacing_padding (int, optional): Padding to increase space between
             strokes. Defaults to 5.
        alpha (int, optional): Angle of strokes. Defaults to 30.
        arrow_length (int, optional): Length of arrow tip. Defaults to 15.
        arrow_angle (int, optional): Angle of arrow tip. Defaults to 30.
        description (str | Any, optional): Description of arrow. Defaults to None.
        description_padding_x (int | Any, optional): Padding on starting point of
            arrow. Defaults to None.
        description_padding_y (int | Any, optional): Padding to put description
            slightly above arrow. Defaults to None.
        description_font_size (int | Any, optional): Description font size. Must
            be passed as percentage of canvas.width or canvas.height. Defaults to None.
        description_max_width (int | Any, optional): Max width of description.
            Must be passed as percentage of canvas.width or canvas.height.
            Defaults to None.

    Raises:
        NotImplementedError: _description_
    """
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

    # if arrow has description add it
    if description is not None:
        center = (
            x1 + abs_value(canvas.width, description_padding_x),
            y1 - abs_value(canvas.height, description_padding_y),
        )
        canvas.line_width = 0.9
        canvas.font = f"{abs_value(canvas.width, description_font_size)}px euklid"
        canvas.fill_text(
            description,
            center[0],
            center[1],
            max_width=abs_value(canvas.width, description_max_width),
        )
