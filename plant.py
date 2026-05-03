import math
from dataclasses import dataclass

@dataclass
class Pendulum:
    # static
    mass: float     # kg
    length: float   # m
    gravity: float  # m/s^2
    # dynamic
    q: float        # rad
    qd: float       # rad/s

    def equ_of_motion(self, tau: float) -> float:
        # tau is in N*m; return qdd in rad/s^2.
        return - (self.gravity / self.length) * math.sin(self.q) + tau / (self.mass * self.length * self.length)
    
