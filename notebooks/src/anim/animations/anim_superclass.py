from abc import abstractmethod
from typing import Tuple, List
import time
from threading import Thread
import threading
from ipywidgets import IntProgress
from IPython.display import display


class AnimationInstance:
    def __init__(self) -> None:
        self.canvas = None
        self.calculator = None
        self.is_running = threading.Event()
        self.is_calculating = threading.Event()
        self._observer = None

    def start(self):
        """Function to start animation thread if "start"
        button is pressed.
        """

        # start new thread for calculation
        self.calc_thread = Thread(target=self._calculate)
        self.calc_thread.start()
        self.calc_thread.join()

        # start new thread for animation
        if not self.is_calculating.is_set():
            self.is_running.set()
            self.anim_thread = Thread(target=self._animate_visual, daemon=True).start()

    def stop(self):
        """Function to stop animation thread if "stop"
        button is pressed.
        """
        print("here")
        if self.is_running.is_set():
            # stop animation
            self.is_running.clear()
            if self.anim_thread:
                self.anim_thread.join()

    def register_observer(self, observer):
        """_summary_

        Args:
            observer (_type_): _description_
        """
        self._observer = observer

    def unregister_observer(self):
        """_summary_"""
        self._observer = None

    def notify_observers(self):
        """_summary_"""
        self._observer.update()

    @abstractmethod
    def _animate_visual(self):
        pass
        """Function to animate the visualization.
        """

    @abstractmethod
    def _calculate(self):
        pass
        """Function to calculate solution.
        """

    @abstractmethod
    def _draw_first_frame(self):
        pass
        """Function to draw the first frame of animation before
            "start" button is pressed.

        Args:
            canvas (Canvas): Canvas to be drawn on.
        """

    @abstractmethod
    def _inital_visual(self):
        pass
        """Function that draws the still modules of the animation
            before any button is pressed.
        """
