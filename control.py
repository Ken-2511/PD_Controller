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
        error = math.atan2(math.sin(qr - q), math.cos(qr - q))  # shortest angle error
        return self.kp * error - self.kd * qd + self.mass * self.gravity * self.length * math.sin(q)
    
@dataclass
class Pendulum_CT_Controller:
    kp: float
    kd: float
    mass: float
    gravity: float
    length: float

    def compute_torque(self, q: float, qd: float, qr: float, qrd: float, qrdd: float) -> float:
        # Compute the control torque using a computed torque control law.
        a = qrdd + self.kp * (qr - q) + self.kd * (qrd - qd)
        return self.mass * self.length * self.length * a + self.mass * self.gravity * self.length * math.sin(q)