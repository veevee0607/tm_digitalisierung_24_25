import time
import math
from ipycanvas import hold_canvas
import numpy as np
import time

from ..modules.shapes import Spring, Rectangle
from ...utils.helper import (
    abs_value,
    map_value,
    draw_line_with_strokes,
    rotate_point,
)
from .anim_superclass import AnimationInstance
from ...calculations.int_solver import IntSolver
from ..modules.shapes import Rectangle, Circle

from ...utils.constants import (
    NUM_TIME_UNITS,
    NUM_DATAPOINTS,
    MASS,
    START_DEFLECTION,
    START_VELOCITY,
    DEFAULT_C,
    DEFAULT_D,
    DEFAULT_FRAME,
    X_ORIGIN,
    Y_ORIGIN,
    Y_AX_TOP,
    Y_AX_BOTTOM,
    X_AX_RIGHT,
)


class Aufgabe4(AnimationInstance):

    def __init__(self):
        super().__init__()
        self.calculator = IntSolver()
        self.c = DEFAULT_C
        self.d = DEFAULT_D
        self.frame = DEFAULT_FRAME
        self.circ = Circle(center=(-1, -1), radius=-1)
        self.rec = Rectangle(width=-1, height=-1)

    def _inital_visual(self):
        """Draw the inital visual for the visual representation of oscillation."""
        # draw inital lines
        # coordinates
        x_1_h = abs_value(self.anim_canvas.height, 30)
        y_1_h = abs_value(self.anim_canvas.height, 20)
        x_2_h = abs_value(self.anim_canvas.height, 40)
        y_2_h = abs_value(self.anim_canvas.height, 20)

        x_1_v = abs_value(self.anim_canvas.height, 10)
        y_1_v = abs_value(self.anim_canvas.height, 50)
        x_2_v = abs_value(self.anim_canvas.height, 10)
        y_2_v = abs_value(self.anim_canvas.height, 60)

        # horizontal
        self.anim_canvas[1].line_width = 2.0
        draw_line_with_strokes(
            canvas=self.anim_canvas[1],
            x_1=x_1_h,
            y_1=y_1_h,
            x_2=x_2_h,
            y_2=y_2_h,
            len_strokes=abs_value(self.anim_canvas.height, 2),
            num_strokes=5,
            alpha=80,
            direction_strokes="top",
        )
        self.anim_canvas[1].line_width = 1.5

        # triangle on horizontal line
        triangle_endpoint_x_h = x_1_h + ((x_2_h - x_1_h) / 2)
        triangle_endpoint_y_h = y_1_h + abs_value(self.anim_canvas.height, 5)
        self.anim_canvas[1].stroke_line(
            x_1_h + abs_value(self.anim_canvas.height, 1),
            y_1_h,
            triangle_endpoint_x_h,
            triangle_endpoint_y_h,
        )
        self.anim_canvas[1].stroke_line(
            x_2_h - abs_value(self.anim_canvas.height, 1),
            y_1_h,
            triangle_endpoint_x_h,
            triangle_endpoint_y_h,
        )

        # vertical line
        self.anim_canvas[1].line_width = 2.0
        draw_line_with_strokes(
            canvas=self.anim_canvas[1],
            x_1=x_1_v,
            y_1=y_1_v,
            x_2=x_2_v,
            y_2=y_2_v,
            len_strokes=abs_value(self.anim_canvas.height, 2),
            num_strokes=5,
            alpha=10,
            direction_strokes="left",
        )

        self.anim_canvas[1].line_width = 1.5

        # triangle on vertical line
        triangle_endpoint_x_v = x_1_v + abs_value(self.anim_canvas.height, 5)
        triangle_endpoint_y_v = y_1_v + ((y_2_v - y_1_v) / 2)
        self.anim_canvas[1].stroke_line(
            x_1_v,
            y_1_v + abs_value(self.anim_canvas.height, 1),
            triangle_endpoint_x_v,
            triangle_endpoint_y_v,
        )
        self.anim_canvas[1].stroke_line(
            x_2_v,
            y_2_v
            - abs_value(
                self.anim_canvas.height,
                1,
            ),
            triangle_endpoint_x_v,
            triangle_endpoint_y_v,
        )

        # make circles
        self.anim_canvas[1].line_width = 2.5
        self.anim_canvas[1].fill_style = "#FFFFFF"

        # horizontal
        self.anim_canvas[1].stroke_circle(
            x=triangle_endpoint_x_h,
            y=triangle_endpoint_y_h,
            radius=int(abs_value(self.anim_canvas.height, 1) / 1.5),
        )
        self.anim_canvas[1].fill_circle(
            x=triangle_endpoint_x_h,
            y=triangle_endpoint_y_h,
            radius=int(abs_value(self.anim_canvas.height, 1) / 1.5),
        )
        self.bearings_point = (triangle_endpoint_x_h, triangle_endpoint_y_h)

        # vertical
        radius_v = int(abs_value(self.anim_canvas.height, 1) / 1.5)
        self.anim_canvas[1].stroke_circle(
            x=triangle_endpoint_x_v,
            y=triangle_endpoint_y_v,
            radius=radius_v,
        )

        # set anker point for rectanlge and circle
        self.radius_v = radius_v
        self.anker_point_rec = (triangle_endpoint_x_v, triangle_endpoint_y_v - radius_v)
        self.rec.width = abs_value(self.anim_canvas.height, 50)
        self.rec.height = self.radius_v * 2
        self.circ.radius = abs_value(self.anim_canvas.height, 10)
        # self.circ.center = (
        #     self.anker_point_rec[0]
        #     + abs_value(self.anim_canvas.height, 50)
        #     + self.circ.radius,
        #     self.anker_point_rec[1] + self.radius_v,
        # )
        self.circ.center = (
            self.rec.width + self.circ.radius,
            self.anker_point_rec[1] + self.radius_v,
        )

        # draw first frame
        self._draw_first_frame()

        # fill circle after rectangle
        self.anim_canvas[1].fill_style = "#FFFFFF"
        self.anim_canvas[1].fill_circle(
            x=triangle_endpoint_x_v,
            y=triangle_endpoint_y_v,
            radius=radius_v,
        )

        # set some class attributes
        self.x_origin = abs_value(self.graph_canvas.height, X_ORIGIN)
        self.y_origin = abs_value(self.graph_canvas.width, Y_ORIGIN)
        self.y_ax_top = abs_value(self.graph_canvas.height, Y_AX_TOP)
        self.y_ax_bottom = abs_value(self.graph_canvas.height, Y_AX_BOTTOM)
        self.x_ax_right = abs_value(self.graph_canvas.height, X_AX_RIGHT)

        # draw coordinate system
        self.draw_coordinate_system()
        self.graph_canvas[0].translate(x=self.x_origin, y=self.y_origin)
        self.graph_canvas[0].fill_style = "blue"

        self.graph_canvas[2].translate(x=self.x_origin, y=self.y_origin)
        self.graph_canvas[2].stroke_style = "blue"
        self.graph_canvas[2].line_width = 1.0

    def _calculate(self):
        """Function to calculate the solution given the current inputs."""
        # clear static graph
        self.graph_canvas[2].clear_rect(
            -self.x_origin,
            -self.y_origin,
            self.graph_canvas.width,
            self.graph_canvas.height,
        )
        # clear animated graph
        self.graph_canvas[0].clear_rect(
            -self.x_origin,
            -self.y_origin,
            self.graph_canvas.width,
            self.graph_canvas.height,
        )
        t = np.linspace(0, NUM_TIME_UNITS, NUM_DATAPOINTS)
        solution = self.calculator.integrate(
            self.calculator.calculate,
            START_DEFLECTION,
            START_VELOCITY,
            t,  # t
            self.c,  # c
            self.d,  # d
            MASS,  # m
        )
        solution = solution[:, 1]
        self.solution = np.array(list(zip(t, solution)))

        # map solution for graph animation
        t_min = t.min(axis=0)
        t_max = t.max(axis=0)
        s_min = min(solution)
        s_max = max(solution)

        self.mapped_solution = [
            (
                map_value(val_t, t_min, t_max, 0, self.x_ax_right),
                map_value(
                    val_s,
                    s_min,
                    s_max,
                    0,
                    self.y_ax_top,  # only half the axis
                ),
            )
            for (val_t, val_s) in self.solution
        ]
        self.offset = self.mapped_solution[0][1]

    def _animate_visual(self):
        """Function to animate the visual representation of oscillation
        and the line graph.
        """
        # draw still graph
        self.graph_canvas[2].begin_path()
        first_point = self.mapped_solution[0]
        # start at first point
        self.graph_canvas[2].move_to(first_point[0], first_point[1])

        for t, s in self.mapped_solution:
            self.graph_canvas[2].line_to(t, s - self.offset)

        self.graph_canvas[2].stroke()

        # make iterators for both solutions
        visual_iter = iter(self.solution)
        graph_iter = iter(self.mapped_solution)

        while self.is_running.is_set():
            try:
                # graph animation
                t_graph, s_graph = next(graph_iter)
                with hold_canvas():
                    self.animate_blob(t_graph, s_graph)

                # visual animation
                _, s_visual = next(visual_iter)
                self.draw_rotating_angle(s_visual)

                # pause
                self.anim_canvas[0].sleep(10)  # 20 milli seconds
                self.graph_canvas[0].sleep(10)

            # end animation when either iterator is exhausted
            except StopIteration:
                self.notify_observers()
                break

    def draw_rotating_angle(self, angle):
        """Function to draw the rectangle and circle at given angle.

        Args:
            angle (int): Current angle.
        """
        # Calculate the coordinates of the four corners
        fixed_x = self.anker_point_rec[0]
        fixed_y = self.anker_point_rec[1] + self.radius_v
        top_left = (
            fixed_x,
            fixed_y - self.rec.height / 2,
        )
        top_right = (
            fixed_x + self.rec.width,
            fixed_y - self.rec.height / 2,
        )
        bottom_left = (
            fixed_x,
            fixed_y + self.rec.height / 2,
        )
        bottom_right = (
            fixed_x + self.rec.width,
            fixed_y + self.rec.height / 2,
        )

        # Rotate the corners around the fixed point
        top_left_rot = rotate_point(*top_left, fixed_x, fixed_y, angle)
        top_right_rot = rotate_point(*top_right, fixed_x, fixed_y, angle)
        bottom_left_rot = rotate_point(*bottom_left, fixed_x, fixed_y, angle)
        bottom_right_rot = rotate_point(*bottom_right, fixed_x, fixed_y, angle)

        self.anim_canvas[0].line_width = 1.5
        with hold_canvas():
            self.anim_canvas[0].clear()
            # draw the rectangle using the rotated points
            self.anim_canvas[0].fill_style = "#bebebe"
            self.anim_canvas[0].fill_polygon(
                [top_left_rot, top_right_rot, bottom_right_rot, bottom_left_rot]
            )
            self.anim_canvas[0].stroke_polygon(
                [top_left_rot, top_right_rot, bottom_right_rot, bottom_left_rot]
            )

            # get center of circle
            circle_center = rotate_point(
                fixed_x + self.rec.width, fixed_y, fixed_x, fixed_y, angle
            )

            # draw circle
            self.anim_canvas[0].fill_circle(
                circle_center[0], circle_center[1], self.circ.radius
            )
            self.anim_canvas[0].stroke_circle(
                circle_center[0], circle_center[1], self.circ.radius
            )

    def draw_coordinate_system(self):
        """Function to draw basic, static coordinate system."""
        self.graph_canvas[1].line_width = 2.0
        # translate
        self.graph_canvas[1].translate(x=self.x_origin, y=self.y_origin)
        # draw x- and y-axis
        self.graph_canvas[1].stroke_line(
            x1=0, y1=-self.y_ax_top, x2=0, y2=self.y_ax_bottom
        )
        self.graph_canvas[1].stroke_line(x1=0, y1=0, x2=self.x_ax_right, y2=0)
        # draw labels
        self.graph_canvas[1].font = "italic 20px 'Cambria Math', serif"
        self.graph_canvas[1].fill_text(
            "t [s]",
            self.x_ax_right - abs_value(self.graph_canvas.width, 5),
            abs_value(self.graph_canvas.width, 5),
        )
        # vertical label
        # save curren state of canvas
        self.graph_canvas[1].save()
        # rotate canvas for verical text
        self.graph_canvas[1].rotate(-math.pi / 2)
        self.graph_canvas[1].fill_text(
            "Auslenkung φ(t) [ ° ]",
            -self.y_ax_top // 2,
            -abs_value(self.graph_canvas.width, 5),
        )
        # restore canvas state
        self.graph_canvas[1].restore()

        # add ticks
        self.graph_canvas[1].line_width = 1.0
        tick_length = abs_value(self.graph_canvas.width, 2)
        num_ticks_x = 10
        # x axis
        x_spacing = self.x_ax_right / num_ticks_x
        for i in range(1, num_ticks_x + 1):
            x = i * x_spacing
            self.graph_canvas[1].stroke_line(
                x1=x, y1=-tick_length / 2, x2=x, y2=tick_length / 2
            )

        # y axis
        num_ticks_y = 8
        y_spacing = (self.y_ax_top + self.y_ax_bottom) / num_ticks_y
        for i in range(1, int(num_ticks_y / 2) + 1):
            y_1 = -i * y_spacing
            y_2 = i * y_spacing
            self.graph_canvas[1].stroke_line(
                x1=-tick_length / 2, y1=y_1, x2=tick_length / 2, y2=y_1
            )
            self.graph_canvas[1].stroke_line(
                x1=-tick_length / 2, y1=y_2, x2=tick_length / 2, y2=y_2
            )

    def animate_blob(self, t, s):
        """Function to animate the blob along the line graph.

        Args:
            t (int): Current x position.
            s (int): Current y position.
        """
        with hold_canvas():
            self.graph_canvas[0].clear_rect(
                -self.x_origin,
                -self.y_origin,
                self.graph_canvas.width,
                self.graph_canvas.height,
            )
            self.graph_canvas[0].fill_circle(
                t, s - self.offset, radius=abs_value(self.graph_canvas.height, 1)
            )
