import math

# gui
NUM_TIME_UNITS = 20
NUM_DATAPOINTS = 1000
DEFAULT_FRAME = 0

# calculations
START_DEFLECTION = math.pi
START_VELOCITY = 0
MASS = 1
DEFAULT_C = 0.5
DEFAULT_D = 0.5

# drawing still modules
DIRECTIONS = {
    "right": (-1, 1),
    "left": (1, -1),
    "bottom": (-1, 1),
    "top": (1, -1),
}
X_ORIGIN = 20
Y_ORIGIN = 55
Y_AX_TOP = 30
Y_AX_BOTTOM = 30
X_AX_RIGHT = 70
