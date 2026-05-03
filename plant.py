import math
from dataclasses import dataclass

@dataclass
class Pendulum:
    # static
    mass: float
    length: float
    gravity: float
    # dynamic
    q: float
    qd: float
