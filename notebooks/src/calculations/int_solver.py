from typing import List, Tuple
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import math


class IntSolver:
    def __init__(self) -> None:
        return None

    def calculate(
        self, x: Tuple[float, float], t: List[float], c: float, d: float, m: float
    ) -> Tuple[float, float]:
        x_1, x_2 = x[0], x[1]

        x_dot = (x_2, -d / m * x_2 - c / m * x_1)
        return x_dot

    def integrate(self, func, start_deflection: float, start_velocity: float, t, *args):
        y_0 = (start_deflection, start_velocity)
        # variabel
        x = odeint(func=func, y0=y_0, t=t, args=args)

        return x


# def main():
#     solver = IntSolver()

#     t = np.linspace(0, 100, 1000)
#     solution = solver.integrate(
#         solver.calculate,
#         math.pi / 12,
#         0,
#         t,
#         0.5,  # c
#         0.2,  # d
#         1,  # m
#     )

#     print(f"{solution=}")

#     # Example data
#     x = solution[:, 0]  # first column
#     y = solution[:, -1:]  # second column
#     print(f"{x=}")
#     print(f"{y=}")

#     # Plotting
#     plt.plot(t, x)  # Label for the legend
#     plt.xlabel("t")  # Label for the x-axis
#     plt.ylabel("x")  # Label for the y-axis
#     plt.title("Plot of t vs x")  # Title for the plot
#     plt.legend()  # Show legend

#     plt.grid(True)  # Optional: Show grid
#     plt.show()


# main()
