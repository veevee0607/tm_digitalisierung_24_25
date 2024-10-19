import time, os, sys
from typing import Tuple, List, Any
import numpy as np
from ipycanvas import Canvas, hold_canvas


from ..animation_modules.modules import Shape
from ..external_utilities.spring import spring_module


class Spring(Shape):
    def __init__(
        self, start: List[int], end: List[int], nodes: int, width: float
    ) -> None:
        self._start = start
        self._end = end
        self._nodes = nodes
        self._width = width

    def animate(
        self, canvas: Canvas, time_vec: List[int], pos_vec: List[Tuple[int, int]]
    ) -> None:

        # for _, pos in list(zip(time_vec, pos_vec)):

        with hold_canvas():
            canvas.clear()
            x_coords, y_coords = spring_module.spring(
                [self._start[0], self._start[1]],
                pos_vec,  # list(pos),
                self._nodes,
                self._width,
            )
            canvas.stroke_lines(list(zip(x_coords, y_coords)))

            # time.sleep(0.02)
