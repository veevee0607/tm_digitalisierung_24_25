from typing import Any
from ipycanvas import MultiCanvas
import ipywidgets.widgets as widgets
from ipywidgets import AppLayout, GridspecLayout, Button, Layout

from ..uebung_1.einmassenschwinger import Einmassenschwinger


"""Module containing functions to build an interactive ui for displaying
    and manipulating animations.
"""

IS_RUNNING: Any = False
EINMASENSCHWINGER_INSTANCE: Any = None


def make_interactive_ui():
    """Function to build interactive ui for displaying
    and manipulating animations.
    """
    # make elements for slider
    slider_title = widgets.HTML(
        '<strong style="font-family: Arial, sans-serif;">Variables</strong>'
    )

    slider_d = widgets.IntSlider(
        value=7,
        min=0,
        max=10,
        step=1,
        description="d",
        # continuous_update=True,
        orientation="horizontal",
        readout=True,
        readout_format="d",
        layout=widgets.Layout(left="-30%", top="-70%", width="120%", display="flex"),
    )

    slider_c = widgets.IntSlider(
        value=7,
        min=0,
        max=10,
        step=1,
        description="c",
        # continuous_update=True,
        orientation="horizontal",
        readout=True,
        readout_format="d",
        layout=widgets.Layout(left="-30%", bottom="120%", width="120%", display="flex"),
    )

    # define observe functions
    slider_d.observe(on_value_change_d, names="value")
    slider_c.observe(on_value_change_c, names="value")

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
            height="25%",
            width="15%",
            bottom="65%",
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
        ),
    )
    anim_button.description = "▶"

    # left multi canvas for visual animation
    mult_canvas_vis = MultiCanvas(
        n_canvases=4,
        width=600,
        height=300,
        layout=widgets.Layout(
            width="100%", height="100%"  # , border="2px solid purple", padding="1px"
        ),
    )
    global EINMASENSCHWINGER_INSTANCE
    EINMASENSCHWINGER_INSTANCE = Einmassenschwinger(mult_canvas_vis)
    anim_button.on_click(lambda b: animation_button_click(mult_canvas_vis, b))
    # anim_button.style.button_color = 'lightgreen'

    # make grid for animation interaction
    anim_inter_grid = GridspecLayout(
        2,
        1,
    )
    anim_inter_grid[0, 0] = animation_title
    anim_inter_grid[1, 0] = anim_button

    # right multi canvas for plot animation
    mult_canvas_plot = MultiCanvas(
        layout=widgets.Layout(
            width="100%", height="100%", border="2px solid green", padding="1px"
        )
    )

    # make grid for canvases
    canvas_grid = GridspecLayout(1, 2)
    canvas_grid[0, 0] = mult_canvas_vis
    canvas_grid[0, 1] = mult_canvas_plot

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
    return app_layout


def animation_button_click(mult_canvas_vis, b: widgets.Button):
    """Function controlling the behaviour of the
        "start"/"stop" button.

    Args:
        b (widgets.Button): "start"/"stop" button.
    """
    global IS_RUNNING, EINMASENSCHWINGER_INSTANCE
    if IS_RUNNING:
        IS_RUNNING = False
        b.description = "▶"
        EINMASENSCHWINGER_INSTANCE.stop()
    else:
        IS_RUNNING = True
        b.description = "❚❚"
        EINMASENSCHWINGER_INSTANCE.start()


def on_value_change_d(change):
    """_summary_

    Args:
        change (_type_): _description_
    """
    new_value = change["new"]
    global EINMASENSCHWINGER_INSTANCE
    EINMASENSCHWINGER_INSTANCE.d = new_value


def on_value_change_c(change):
    """_summary_

    Args:
        change (_type_): _description_
    """
    new_value = change["new"]
    global EINMASENSCHWINGER_INSTANCE
    EINMASENSCHWINGER_INSTANCE.c = new_value
