from typing import Tuple, List, Any
from ipycanvas import Canvas
from abc import abstractmethod


class Shape:
    def __init__(
        self,
        center: Tuple[int, int],
        width: int | Any = None,
        height: int | Any = None,
        upper_left_corner: Tuple[int, int] | Any = None,
        radius: int | Any = None,
        A: Tuple[int, int] | Any = None,
        B: Tuple[int, int] | Any = None,
        C: Tuple[int, int] | Any = None,
    ) -> None:
        self._center = center

        # shape can only be one of rectangle, triangle or circle
        if width is not None and height is not None and upper_left_corner is not None:
            self._width = width
            self._height = height
            self._upper_left_corner = upper_left_corner
        elif radius is not None:
            self._radius = radius
        elif A is not None and B is not None and C is not None:
            self._A = A
            self._B = B
            self._C = C

    @abstractmethod
    def animate(
        self,
        canvas: Canvas,
        time_vec: List[int],
        pos_vec: Any,
    ) -> None:
        pass

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, new_center: int):
        self._center = new_center

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, new_width: int):
        self._width = new_width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new_height: int):
        self._height = new_height

    @property
    def upper_left_corner(self):
        return self._upper_left_corner

    @upper_left_corner.setter
    def height(self, new_corner: int):
        self._upper_left_corner = new_corner

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, new_radius: int):
        self._radius = new_radius

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, new_A: int):
        self._A = new_A

    @property
    def B(self):
        return self._B

    @B.setter
    def B(self, new_B: int):
        self._B = new_B

    @property
    def C(self):
        return self._C

    @C.setter
    def C(self, new_C: int):
        self._C = new_C
