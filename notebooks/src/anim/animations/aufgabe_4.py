import time
import math
import asyncio
from threading import Thread
from ipycanvas import Canvas, hold_canvas
import numpy as np
import time

from ..modules.shapes import Spring, Rectangle
from ..modules import still_modules
from ...utils.helper import (
    abs_value,
    map_value,
    animate_text,
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

    def _calculate(self):
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
        self.solution = solution

    def _inital_visual(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        # draw inital lines
        # coordinates
        x_1_h = abs_value(self.canvas.height, 30)
        y_1_h = abs_value(self.canvas.height, 20)
        x_2_h = abs_value(self.canvas.height, 40)
        y_2_h = abs_value(self.canvas.height, 20)

        x_1_v = abs_value(self.canvas.height, 10)
        y_1_v = abs_value(self.canvas.height, 50)
        x_2_v = abs_value(self.canvas.height, 10)
        y_2_v = abs_value(self.canvas.height, 60)

        # horizontal
        self.canvas[1].line_width = 2.0
        draw_line_with_strokes(
            canvas=self.canvas[1],
            x_1=x_1_h,
            y_1=y_1_h,
            x_2=x_2_h,
            y_2=y_2_h,
            len_strokes=abs_value(self.canvas.height, 2),
            num_strokes=5,
            alpha=80,
            direction_strokes="top",
        )
        self.canvas[1].line_width = 1.5

        # triangle on horizontal line
        triangle_endpoint_x_h = x_1_h + ((x_2_h - x_1_h) / 2)
        triangle_endpoint_y_h = y_1_h + abs_value(self.canvas.height, 5)
        self.canvas[1].stroke_line(
            x_1_h + abs_value(self.canvas.height, 1),
            y_1_h,
            triangle_endpoint_x_h,
            triangle_endpoint_y_h,
        )
        self.canvas[1].stroke_line(
            x_2_h - abs_value(self.canvas.height, 1),
            y_1_h,
            triangle_endpoint_x_h,
            triangle_endpoint_y_h,
        )

        # vertical line
        self.canvas[1].line_width = 2.0
        draw_line_with_strokes(
            canvas=self.canvas[1],
            x_1=x_1_v,
            y_1=y_1_v,
            x_2=x_2_v,
            y_2=y_2_v,
            len_strokes=abs_value(self.canvas.height, 2),
            num_strokes=5,
            alpha=10,
            direction_strokes="left",
        )

        self.canvas[1].line_width = 1.5

        # triangle on vertical line
        triangle_endpoint_x_v = x_1_v + abs_value(self.canvas.height, 5)
        triangle_endpoint_y_v = y_1_v + ((y_2_v - y_1_v) / 2)
        self.canvas[1].stroke_line(
            x_1_v,
            y_1_v + abs_value(self.canvas.height, 1),
            triangle_endpoint_x_v,
            triangle_endpoint_y_v,
        )
        self.canvas[1].stroke_line(
            x_2_v,
            y_2_v
            - abs_value(
                self.canvas.height,
                1,
            ),
            triangle_endpoint_x_v,
            triangle_endpoint_y_v,
        )

        # make circles
        self.canvas[1].line_width = 2.5
        self.canvas[1].fill_style = "#FFFFFF"

        # horizontal
        self.canvas[1].stroke_circle(
            x=triangle_endpoint_x_h,
            y=triangle_endpoint_y_h,
            radius=int(abs_value(self.canvas.height, 1) / 1.5),
        )
        self.canvas[1].fill_circle(
            x=triangle_endpoint_x_h,
            y=triangle_endpoint_y_h,
            radius=int(abs_value(self.canvas.height, 1) / 1.5),
        )
        self.bearings_point = (triangle_endpoint_x_h, triangle_endpoint_y_h)

        # vertical
        radius_v = int(abs_value(self.canvas.height, 1) / 1.5)
        self.canvas[1].stroke_circle(
            x=triangle_endpoint_x_v,
            y=triangle_endpoint_y_v,
            radius=radius_v,
        )

        # set anker point for rectanlge and circle
        self.radius_v = radius_v
        self.anker_point_rec = (triangle_endpoint_x_v, triangle_endpoint_y_v - radius_v)
        self.rec.width = abs_value(self.canvas.height, 50)
        self.rec.height = self.radius_v * 2
        self.circ.radius = abs_value(self.canvas.height, 10)
        # self.circ.center = (
        #     self.anker_point_rec[0]
        #     + abs_value(self.canvas.height, 50)
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
        self.canvas[1].fill_style = "#FFFFFF"
        self.canvas[1].fill_circle(
            x=triangle_endpoint_x_v,
            y=triangle_endpoint_y_v,
            radius=radius_v,
        )

    def _animate(self):
        for s in self.solution:
            if self.is_running.is_set():
                angle = s[1]
                self.draw_rotating_angle(angle)
                # self.draw_feder_daempfer(angle)
                time.sleep(0.02)
            else:
                break
        # notify the button when animation finishes
        self.notify_observers()

    def draw_feder_daempfer(self, angle):
        alpha = np.arctan2(
            np.cos(angle) - self.bearings_point[0],
            np.sin(angle) - self.bearings_point[1],
        )

        # obere Transformationmatrix
        K_o = np.array(
            [
                [np.sin(alpha), -np.cos(alpha), 1 - 0.355 * np.sin(alpha)],
                [np.cos(alpha), np.sin(alpha), 1.3 - 0.355 * np.cos(alpha)],
                [0, 0, 1],
            ]
        )

        # Ortsvektor des KOS-Ursprungs 2 in globalen Koordinaten
        # koordinatenursprung in den unteren Gabelpunkt legen
        r_O2_1 = np.array(
            [1 - 0.355 * np.sin(alpha), 1.3 - 0.355 * np.cos(alpha), 1]
        )  # mitte der oberen oder unteren Gabel

        # oberer Gabelungspunkt
        r_P1_2 = np.array([-0.35, 0, 1])

        # linker Gabelungspunkt
        r_P2_2 = np.array([0, 0.2, 1])

        # rechter Gabelungspunkt
        r_P3_2 = np.array([0, -0.2, 1])

        # untere Transformationsmatrix
        K_u = np.array(
            [
                [
                    np.sin(alpha),
                    -np.cos(alpha),
                    np.cos(angle) + 0.1 * np.sin(alpha),
                ],
                [np.cos(alpha), np.sin(alpha), np.sin(angle) + 0.1 * np.cos(alpha)],
                [0, 0, 1],
            ]
        )

        # Ortvektor des KOS-Ursprungs 3 in globalen Koordinaten
        r_O3_1 = np.array(
            [
                np.cos(angle) + 0.1 * np.sin(alpha),
                np.sin(angle) + 0.1 * np.cos(alpha),
                1,
            ]
        )

        # unterer Gabelungspunkt
        r_P4_3 = np.array([-0.1, 0, 1])  # _3 = bzgl Koordinatensystem 3

        # linker Gabelungspunkt
        r_P5_3 = np.array([0, 0.2, 1])

        # rechter Gabelungspunkt
        r_P6_3 = np.array([0, -0.2, 1])

        # Punkte in globalen Koordinaten
        r_P1_1 = np.matmul(K_o, r_P1_2)  # _1 = globale Koordinaten
        r_P2_1 = np.matmul(K_o, r_P2_2)
        r_P3_1 = np.matmul(K_o, r_P3_2)
        r_P4_1 = np.matmul(K_u, r_P4_3)
        r_P5_1 = np.matmul(K_u, r_P5_3)
        r_P6_1 = np.matmul(K_u, r_P6_3)

        # print(f"{r_P4_1=}")
        with hold_canvas():
            self.canvas[2].translate(self.bearings_point[0], self.bearings_point[1])
            # self.canvas[0].fill_circle(
            #     self.bearings_point[0], self.bearings_point[1], 5
            # )
            self.canvas[2].clear()
            self.canvas[2].stroke_line(
                r_P4_1[0] * 100 + 200,
                r_O3_1[0] * 100 + 50,
                r_P4_1[1] * 100 + 200,
                r_O3_1[1] * 100 + 50,
            )
            self.canvas[2].stroke_line(
                r_P5_1[0] * 100 + 200,
                r_P6_1[0] * 100 + 50,
                r_P5_1[1] * 100 + 200,
                r_P6_1[1] * 100 + 50,
            )
            self.canvas[2].stroke_line(
                r_O2_1[0] * 100 + 200,
                r_P1_1[0] * 100 + 50,
                r_O2_1[1] * 100 + 200,
                r_P1_1[1] * 100 + 50,
            )
            self.canvas[2].stroke_line(
                r_P2_1[0] * 100 + 200,
                r_P3_1[0] * 100 + 50,
                r_P2_1[1] * 100 + 200,
                r_P3_1[1] * 100 + 50,
            )

    def draw_rotating_angle(self, angle):
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

        self.canvas[0].line_width = 1.5
        with hold_canvas():
            self.canvas[0].clear()
            # draw the rectangle using the rotated points
            self.canvas[0].fill_style = "#bebebe"
            self.canvas[0].fill_polygon(
                [top_left_rot, top_right_rot, bottom_right_rot, bottom_left_rot]
            )
            self.canvas[0].stroke_polygon(
                [top_left_rot, top_right_rot, bottom_right_rot, bottom_left_rot]
            )

            # get center of circle
            circle_center = rotate_point(
                fixed_x + self.rec.width, fixed_y, fixed_x, fixed_y, angle
            )

            # draw circle
            self.canvas[0].fill_circle(
                circle_center[0], circle_center[1], self.circ.radius
            )
            self.canvas[0].stroke_circle(
                circle_center[0], circle_center[1], self.circ.radius
            )

    def _draw_first_frame(self):
        # self.canvas[0].fill_style = "#bebebe"
        # self.canvas[0].line_width = 1

        # # draw rec
        # self.canvas[0].fill_rect(
        #     self.anker_point_rec[0],
        #     self.anker_point_rec[1],
        #     self.rec.width,
        #     self.rec.height,
        # )
        # self.canvas[0].stroke_rect(
        #     self.anker_point_rec[0],
        #     self.anker_point_rec[1],
        #     self.rec.width,
        #     self.rec.height,
        # )

        # # self.anker_point_circ = (
        # #     self.anker_point_rec[0] + abs_value(self.canvas.height, 50),
        # #     self.anker_point_rec[1] + self.radius_v,
        # # )

        # # draw circle
        # self.canvas[0].fill_circle(
        #     self.circ.center[0],
        #     self.circ.center[1],
        #     self.circ.radius,
        # )
        # self.canvas[0].stroke_circle(
        #     self.circ.center[0],
        #     self.circ.center[1],
        #     self.circ.radius,
        # )

        return None
