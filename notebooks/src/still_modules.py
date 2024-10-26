import copy
from ipycanvas import Canvas, hold_canvas
import math as m


def draw_still_frame(
    canvas: Canvas,
    padding_width,
    padding_height,
    width,
    height,
    stroke_length=15,
    width_num_strokes=30,
    height_num_strokes=15,
    alpha=30,
    beta=60,
):
    """
    padding width: in percentage of canvas width
    padding height: in percentag of canvas height
    width, height: in percentage of cnavas height
    """

    # padding absolute values
    p_w_abs = padding_width / 100 * canvas.width
    p_h_abs = padding_height / 100 * canvas.height

    # width and height absolute values
    w_abs = width / 100 * canvas.width
    h_abs = height / 100 * canvas.height

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
    if alpha + beta + gamma != 180:
        raise NotImplementedError("alpha beta and gamma dont add up to 180")

    # calculate y axis offset
    y_offset = -(stroke_length / m.sin(gamma)) * m.sin(
        alpha
    )  # a = (c/sin(gamma))*sin(alpha)

    # calculate x axis offset
    x_offset = -(stroke_length / m.sin(gamma)) * m.sin(
        beta
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
            temp_start[0] - x_offset,
            temp_start[1] + y_offset,
        )

        temp_vertical_start += height_stroke_space
        temp_start = (temp_start[0], temp_start[1] + height_stroke_space)
        counter += 1

    # move down horizontal line and add strokes
    temp_start = (h_end_point[0], h_end_point[1])
    temp_horizontal_start = copy.deepcopy(p_w_abs)
    counter = 0
    while temp_horizontal_start < p_w_abs + w_abs and counter < width_num_strokes:
        canvas.stroke_line(
            temp_start[0],
            temp_start[1],
            temp_start[0] - x_offset,
            temp_start[1] + y_offset,
        )

        temp_horizontal_start += width_stroke_space
        temp_start = (temp_start[0] + width_stroke_space, temp_start[1])
