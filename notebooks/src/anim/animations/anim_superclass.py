from abc import abstractmethod
from typing import Tuple, List
import time
from threading import Thread
import threading
from ipywidgets import IntProgress
from IPython.display import display


class AnimationInstance:
    def __init__(self) -> None:
        self.frame = None
        self.canvas = None
        self.calculator = None
        self.is_running = threading.Event()
        self.is_calculating = False
        self.anim_thread = None
        self.calc_thread = None
        self.progress_bar_thread = None
        self._observer = None

    def toggle_animation(self, _):
        if self.is_running.is_set():
            # Stop animation
            self.is_running.clear()
            if self.thread:
                self.thread.join()
            self.button.description = "Play"
        else:
            # Start animation
            self.is_running.set()
            self.thread = threading.Thread(target=self.animation_loop, daemon=True)
            self.thread.start()
            self.button.description = "Stop"

    def start(self):
        """Function to start animation thread if "start"
        button is pressed.
        """
        # # make stop event for progress bar thread
        # self.stop_event = threading.Event()
        # # make progress bar while calculating
        # if not self.is_calculating:
        #     self.is_calculating = True
        #     # start new thread for calculation
        #     self.calc_thread = Thread(target=self._calculate)
        #     self.calc_thread.start()
        #     # start new thread for animation
        #     # have them run simultaniously
        #     self.progress_bar_thread = Thread(
        #         target=self.anim_progress_bar, args=(self.stop_event)
        #     )
        #     self.progress_bar_thread.start()

        #     # start thread to monitor threads
        #     self.monitor_thread = threading.Thread(target=self.monitor_calc_threads)
        #     self.monitor_thread.start()

        # calculate solution
        self._calculate()

        self.is_running.set()
        self.anim_thread = Thread(target=self._animate, daemon=True).start()
        # if self.anim_thread.join():
        #     self.anim_finished = True

    def stop(self):
        """Function to stop animation thread if "stop"
        button is pressed.
        """
        if self.is_running.is_set():
            # stop animation
            self.is_running.clear()
            if self.anim_thread:
                self.anim_thread.join()

    # def monitor_calc_threads(self):
    #     """Function to monitor calculation thread and joing anim
    #     thread when calculation is done.
    #     """
    #     # wait for calculation to finish
    #     self.calc_thread.join()
    #     # set stop event for anim thread
    #     self.stop_event.set()
    #     # stop animation of progress bar
    #     self.progress_bar_thread.join()

    # def anim_progress_bar(self):
    #     max_count = 100

    #     f = IntProgress(min=0, max=max_count)  # instantiate the bar
    #     display(f)  # display the bar

    #     count = 0
    #     while count <= max_count:
    #         f.value += 1  # signal to increment the progress bar
    #         time.sleep(0.1)
    #         count += 1
    #     return None

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
    def _animate(self):
        pass
        """Function to animate all moving parts.
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
