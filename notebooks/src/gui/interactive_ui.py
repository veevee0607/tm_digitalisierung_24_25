from typing import Any
from ipycanvas import MultiCanvas
import ipywidgets.widgets as widgets
from ipywidgets import AppLayout, GridspecLayout, Button, Layout
from ..utils.constants import DEFAULT_C, DEFAULT_D


"""Module containing functions to build an interactive ui for displaying
    and manipulating animations.
"""

IS_RUNNING: Any = False
ANIMATION_INSTANCE: Any = None


class GUI:
    def __init__(self, animation_instance: Any):
        """Function to build interactive ui for displaying
        and manipulating animations.
        """
        # register the GUI as observer for animation
        animation_instance.register_observer(self)

        # make elements for slider
        slider_title = widgets.HTML(
            '<strong style="font-family: Arial, sans-serif;">Variables</strong>'
        )

        slider_d = widgets.FloatSlider(
            value=DEFAULT_D,
            min=0.0,
            max=5.0,
            step=0.1,
            description="d",
            # continuous_update=True,
            orientation="horizontal",
            readout=True,
            readout_format=".1f",
            layout=widgets.Layout(
                left="-30%", top="-70%", width="110%", display="flex"
            ),
        )

        slider_c = widgets.FloatSlider(
            value=DEFAULT_C,
            min=0.0,
            max=1.0,
            step=0.1,
            description="c",
            # continuous_update=True,
            orientation="horizontal",
            readout=True,
            readout_format=".1f",
            layout=widgets.Layout(
                left="-30%", bottom="120%", width="110%", display="flex"
            ),
        )

        slider_frame = widgets.IntSlider(
            value=0,
            min=0,
            max=500,
            step=1,
            description="frame",
            # continuous_update=True,
            orientation="horizontal",
            readout=True,
            readout_format="d",
            layout=widgets.Layout(
                left="-20%", bottom="60%", width="110%", display="flex"
            ),
        )

        # define observe functions
        slider_d.observe(self.on_value_change_d, names="value")
        slider_c.observe(self.on_value_change_c, names="value")
        slider_frame.observe(self.on_value_change_frame, names="value")

        # make grid for slider
        slider_grid = GridspecLayout(3, 1)
        slider_grid[0, 0] = slider_title
        slider_grid[1, 0] = slider_d
        slider_grid[2, 0] = slider_c

        # heading for animation widget
        animation_title = widgets.HTML(
            '<strong style="font-family: Arial, sans-serif;">Animation</strong>'
        )
        anim_button = Button(
            button_style="",
            layout=Layout(
                height="27%",
                width="13%",
                bottom="110%",
                left="5%",
                display="flex",
                # border='1px solid black'),
            ),
            style=dict(
                font_size="90%",
                # font_style='italic',
                font_weight="bold",
                # font_variant="small-caps",
                text_color="#5a6368",
                # text_decoration='underline'
                bottom="5%",
                right="5%",
                display="flex",
            ),
        )
        self.anim_button = anim_button
        anim_button.description = "▶"

        # left multi canvas for visual animation
        mult_canvas_anim = MultiCanvas(
            n_canvases=4,
            width=600,
            height=600,
            layout=widgets.Layout(
                width="100%",
                height="100%",  # border="2px solid green", padding="1px"
            ),
        )

        # right multi canvas for graph
        mult_canvas_graph = MultiCanvas(
            n_canvases=4,
            width=600,
            height=600,
            layout=widgets.Layout(
                width="100%",
                height="100%",  # border="2px solid purple", padding="1px"
            ),
        )
        global ANIMATION_INSTANCE
        ANIMATION_INSTANCE = animation_instance
        ANIMATION_INSTANCE.anim_canvas = mult_canvas_anim
        ANIMATION_INSTANCE.graph_canvas = mult_canvas_graph
        ANIMATION_INSTANCE._inital_visual()
        anim_button.on_click(lambda b: self.animation_button_click(mult_canvas_anim, b))
        # anim_button.style.button_color = 'lightgreen'

        # make grid for animation interaction
        anim_inter_grid = GridspecLayout(
            3,
            1,
        )
        anim_inter_grid[0, 0] = animation_title
        anim_inter_grid[1, 0] = slider_frame
        anim_inter_grid[2, 0] = anim_button

        # right multi canvas for plot animation
        # mult_canvas_plot = MultiCanvas(
        #     layout=widgets.Layout(
        #         width="100%", height="100%", border="2px solid green", padding="1px"
        #     )
        # )

        # make grid for canvases
        canvas_grid = GridspecLayout(1, 2)
        canvas_grid[0, 0] = mult_canvas_anim
        canvas_grid[0, 1] = mult_canvas_graph

        # make grid for interacitve part
        interactive_grid = GridspecLayout(2, 1)
        interactive_grid[0, 0] = slider_grid
        interactive_grid[1, 0] = anim_inter_grid

        app_layout = AppLayout(
            header=None,
            left_sidebar=interactive_grid,
            center=canvas_grid,
            right_sidebar=None,
            footer=None,
            pane_widths=["15%", "85%", "0%"],
            pane_heights=["100%", "100%", "100%"],
        )

        self.app_layout = app_layout

    def animation_button_click(self, mult_canvas_vis, b: widgets.Button):
        """Function controlling the behaviour of the
            "start"/"stop" button.

        Args:
            b (widgets.Button): "start"/"stop" button.
        """
        global IS_RUNNING, ANIMATION_INSTANCE
        if IS_RUNNING:
            print("here gui")
            IS_RUNNING = False
            b.description = "▶"
            ANIMATION_INSTANCE.stop()
        else:
            IS_RUNNING = True
            b.description = "❚❚"
            ANIMATION_INSTANCE.start()

    def update(self):
        """_summary_"""
        self.anim_button.description = "▶"

    def on_value_change_d(self, change):
        """_summary_

        Args:
            change (_type_): _description_
        """
        new_value = change["new"]
        global ANIMATION_INSTANCE
        ANIMATION_INSTANCE.d = new_value

    def on_value_change_c(self, change):
        """_summary_

        Args:
            change (_type_): _description_
        """
        new_value = change["new"]
        global ANIMATION_INSTANCE
        ANIMATION_INSTANCE.c = new_value

    def on_value_change_frame(self, change):
        """_summary_

        Args:
            change (_type_): _description_
        """
        new_value = change["new"]
        global ANIMATION_INSTANCE
        ANIMATION_INSTANCE.frame = new_value
