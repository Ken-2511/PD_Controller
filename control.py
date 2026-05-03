import math
from dataclasses import dataclass

@dataclass
class Pendulum_PD_Controller:
    kp: float
    kd: float
    mass: float
    gravity: float
    length: float

    def compute_torque(self, q: float, qd: float, qr: float) -> float:
        # Compute the control torque using a PD control law.
        error = (qr - q + math.pi) % (2 * math.pi) - math.pi
        return self.kp * error - self.kd * qd + self.mass * self.gravity * self.length * math.sin(q)