import time
from typing import Tuple, List, Any
from ipycanvas import Canvas, hold_canvas

from .modules import Shape


class Circle(Shape):
    def __init__(
        self,
        center: Tuple[int, int],
        radius: int | Any = None,
    ) -> None:
        super().__init__(center=center, radius=radius)

    def animate(
        self, canvas: Canvas, time_vec: List[int], pos_vec: List[Tuple[int, int]]
    ) -> None:
        # loop through time vector to animate circle
        for _, pos in zip(time_vec, pos_vec):
            with hold_canvas():
                canvas.clear()
                canvas.stroke_circle(x=pos[0], y=pos[0], radius=self.radius)
                time.sleep(0.02)


class Rectangle(Shape):
    def __init__(
        self,
        center: Tuple[int, int],
        width: int | Any = None,
        height: int | Any = None,
        upper_left_corner: Tuple[int] | Any = None,
    ) -> None:
        super().__init__(center, width, height, upper_left_corner)

    def animate(
        self, canvas: Canvas, time_vec: List[int], pos_vec: List[Tuple[int, int]]
    ) -> None:

        self.height = 100
        # loop through time vector to animate circle
        # for _, pos in zip(time_vec, pos_vec):
        canvas.fill_style = "grey"
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
                x=pos_vec[0] - 5 + self.width / 2,
                y=pos_vec[1] - self.height / 2 + self.height / 2,
            )

            # time.sleep(0.02)


class Triangle(Shape):
    def __init__(
        self,
        center: Tuple[int, int],
        A: Tuple[int] | Any = None,
        B: Tuple[int] | Any = None,
        C: Tuple[int] | Any = None,
    ) -> None:
        super().__init__(center=center, A=A, B=B, C=C)

    def animate(
        self, canvas: Canvas, time_vec: List[int], pos_vec: List[List[Tuple[int, int]]]
    ) -> None:
        # loop through time vector to animate circle
        for _, pos in zip(time_vec, pos_vec):
            with hold_canvas():
                canvas.clear()
                canvas.stroke_polygon(pos)
                time.sleep(0.02)
