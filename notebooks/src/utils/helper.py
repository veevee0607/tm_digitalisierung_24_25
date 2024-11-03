from typing import Tuple
from ipycanvas import Canvas, hold_canvas

"""Modules containing helper functions.
"""


def abs_value(whole: int, percentage: int) -> int:
    """Function to calculate the actual value given
        a percentage and a whole.

    Args:
        whole (int): Whole.
        percentage (int): Percentage.

    Returns:
        int: Actual value.
    """

    return int((percentage / 100) * whole)


def calculate_percentage(value: int, whole: int) -> int:
    """Function to calculate the percentage given
        a percentage and a whole.

    Args:
        value (int): Actual value.
        whole (int): Whole.

    Raises:
        NotImplementedError: _description_

    Returns:
        int: Percentage.
    """
    if whole == 0:
        raise NotImplementedError
    return int(value / whole) * 100


def map_value(
    value: int, original_min: int, original_max: int, target_min: int, target_max: int
) -> int:
    """Function to map a value form original domain to target domain.

    Args:
        value (int): Value to map.
        original_min (int): Lower bound of original domain.
        original_max (int): Upper bound of original domain.
        target_min (int): Lower bound of target domain.
        target_max (int): Upper bound of target domain.

    Raises:
        ValueError: _description_

    Returns:
        int: Mapped value.
    """
    # check for zero range to avoid division by zero
    if original_min == original_max:
        raise ValueError("The original range cannot be zero.")

    # calculate the mapped value
    mapped_value = (value - original_min) / (original_max - original_min) * (
        target_max - target_min
    ) + target_min
    return int(mapped_value)


def animate_text(
    canvas: Canvas,
    pos: Tuple[int, int],
    text: str,
    font_size: int,
    max_width: int,
    fill_style: str,
    x_padding: int,
    y_padding: int,
) -> None:
    """Function to draw/animate text at a specific location.

    Args:
        canvas (Canvas): _description_
        pos (Tuple[int, int]): _description_
        font_size (int): _description_
        max_width (int): _description_
    """
    with hold_canvas():
        canvas.clear()
        canvas.fill_style = fill_style
        canvas.font = f"{abs_value(canvas.width, font_size)}px euklid"
        max_width = abs_value(canvas.width, max_width)
        canvas.fill_text(
            text,
            x=pos[0] + abs_value(canvas.width, x_padding),
            y=pos[1] + abs_value(canvas.width, y_padding),
            max_width=max_width,
        )
