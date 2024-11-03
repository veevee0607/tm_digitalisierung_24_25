import time
from threading import Thread
from ipycanvas import Canvas, hold_canvas
import numpy as np
import time

from ..external_utilities.spring import spring_module
from ..animation_modules.shapes import Spring
from ..animation_modules.shapes import Rectangle
from ..animation_modules import still_modules
from ..animation_modules.still_modules import draw_still_frame
from ..utils.helper import abs_value, map_value, animate_text

"""Module containing the Einmassenschwinger Class and all functions
    to animate that oscillation.
"""

# canvas settings
FONT_SIZE = 4
MAX_WIDTH = 4


class Einmassenschwinger:
    def __init__(self, canvas: Canvas):
        """Initiate all still components for Einmassenschwinger
            animation.

        Args:
            canvas (Canvas): Canvas to be drawn on.
        """
        self.d = None
        self.c = None

        # make frame for animation
        # this is first to attain the global variable MID_POINT
        draw_still_frame(
            canvas=canvas[0],
            padding_width=10,
            padding_height=10,
            width=80,
            height=80,
            width_num_strokes=30,
            height_num_strokes=17,
            alpha_height=10,
            alpha_width=10,
        )

        # cosmetic line where spring is attached
        mid_point = still_modules.MID_POINT
        line_endpoint = (mid_point[0] + abs_value(canvas.width, 2), mid_point[1])
        self.line_endpoint = line_endpoint
        canvas[0].stroke_line(
            mid_point[0], mid_point[1], line_endpoint[0], line_endpoint[1]
        )

        self.canvas = canvas
        self.is_running = False
        self.thread = None
        self.spring_obj = Spring(
            start=still_modules.MID_POINT,
            end=(
                still_modules.MID_POINT[0] + abs_value(canvas.width, 20),
                still_modules.MID_POINT[1],
            ),
            nodes=25,
            width=abs_value(canvas.height, 10),
        )
        self.spring_obj._start = line_endpoint

        self.mass_obj = Rectangle(
            width=abs_value(canvas.width, 20),
            height=abs_value(canvas.height, 20),
        )

        # get dummy solution
        pos_vec = self.calc_dummy_solution()
        self.pos_vec = pos_vec

        # set style for canvases
        canvas[0].stroke_style = "black"
        canvas[0].line_width = 0.65
        global FONT_SIZE
        canvas[0].font = f"{abs_value(canvas.width, FONT_SIZE)}px euklid"

        canvas[1].fill_style = "#bebebe"
        canvas[1].font = f"{abs_value(canvas.width, FONT_SIZE)}px euklid"

        # add text (static)
        global MAX_WIDTH
        canvas[0].fill_text(
            text="c",
            x=mid_point[0] + abs_value(canvas.height, 5),
            y=mid_point[1] - abs_value(canvas.height, 10),
            max_width=abs_value(canvas.width, MAX_WIDTH),
        )

        # draw arrow
        center = (mid_point[0] + abs_value(canvas.width, 20), mid_point[1])
        still_modules.draw_arrow(
            canvas=canvas[0],
            x1=center[0] + abs_value(canvas.width, 10),
            y1=center[1] - abs_value(canvas.height, 20),
            x2=center[0] + abs_value(canvas.width, 20),
            y2=center[1] - abs_value(canvas.height, 20),
            base_length=abs_value(canvas.height, 5),
            num_base_strokes=3,
            alpha=10,
            stroke_len=10,
            spacing_padding=3,
            arrow_length=abs_value(canvas.height, 4),
            arrow_angle=20,
            description="x",
            description_font_size=FONT_SIZE,
            description_max_width=MAX_WIDTH,
            description_padding_x=3,
            description_padding_y=3,
        )

        # draw first frame
        self.draw_first_frame(canvas)

    def start(self):
        """Function to start animation thread if "start"
        button is pressed. See interactive_ui for
        more details on the button interaction.
        """
        if not self.is_running:
            self.is_running = True
            # start the animation in a separate thread
            self.thread = Thread(target=self._animate)
            self.thread.start()

    def stop(self):
        """Function to stop animation thread if "stop"
        button is pressed. See interactive_ui for
        more details on the button interaction.
        """
        # set the flag to stop animation
        self.is_running = False
        if self.thread:
            self.thread.join()  # wait for the thread to finish

    def _animate(self):
        """Function to animate all moving parts within
        Einmassenschwinger system.
        """
        # run animation
        self.canvas[1].line_width = 0.65
        self.canvas[2].line_width = 0.65

        # get range of x values
        x_min = min([p[0] for p in self.pos_vec[10:]])
        x_max = max([p[0] for p in self.pos_vec[10:]])

        mapped_pos_vec = [
            (
                map_value(
                    val_x,
                    x_min,
                    x_max,
                    self.line_endpoint[0],
                    abs_value(self.canvas.width, 50),
                ),
                val_y,
            )
            for (val_x, val_y) in self.pos_vec[10:]
        ]

        global FONT_SIZE
        global MAX_WIDTH
        while self.is_running:
            print(f"{self.c=}")
            print(f"{self.d=}")
            for pos in mapped_pos_vec:

                with hold_canvas():
                    self.spring_obj.draw(
                        canvas=self.canvas[1],
                        pos=pos,
                    )
                with hold_canvas():
                    self.mass_obj.draw(
                        canvas=self.canvas[2],
                        pos=pos,
                    )
                    animate_text(
                        canvas=self.canvas[3],
                        pos=pos,
                        text="m",
                        font_size=FONT_SIZE,
                        max_width=MAX_WIDTH,
                        fill_style="black",
                        x_padding=10,
                        y_padding=1,
                    )

                time.sleep(0.01)
            mapped_pos_vec.reverse()

    def draw_first_frame(self, canvas: Canvas):
        """Function to draw the first frame of animation before
            "start" button is pressed.

        Args:
            canvas (Canvas): Canvas to be drawn on.
        """
        first_frame_pos = self.pos_vec[10]
        with hold_canvas():
            # spring
            self.spring_obj.draw(canvas[1], first_frame_pos)

            # mass obj
            canvas[1].fill_rect(
                x=first_frame_pos[0] + abs_value(canvas.width, 2),
                y=first_frame_pos[1] - self.mass_obj.height / 2,
                width=self.mass_obj.width,
                height=self.mass_obj.height,
            )
            canvas[1].stroke_rect(
                x=first_frame_pos[0] + abs_value(canvas.width, 2),
                y=first_frame_pos[1] - self.mass_obj.height / 2,
                width=self.mass_obj.width,
                height=self.mass_obj.height,
            )

            # animate text
            global MAX_WIDTH
            global FONT_SIZE
            animate_text(
                canvas=self.canvas[3],
                pos=first_frame_pos,
                text="m",
                font_size=FONT_SIZE,
                max_width=MAX_WIDTH,
                fill_style="black",
                x_padding=10,
                y_padding=1,
            )

    def calc_dummy_solution(self):
        """Calculate dummy solution for animation."""
        x = np.linspace(0, 1 * np.pi, 200)
        y = list(np.sin(0.2 * x) * 100 + 1.1)
        pos_vec = [(self.line_endpoint[0] + 10, self.line_endpoint[1])]
        for val in y:
            pos_vec.append(
                (self.line_endpoint[0] + 10 + int(val), self.line_endpoint[1])
            )
        return pos_vec
