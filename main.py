from gui import PendulumPainter
from plant import Pendulum
import pygame
import math

def equ_of_motion(pen: Pendulum) -> float:
    # qdd = - (pen.gravity / pen.length) * math.sin(pen.q)
    return - (pen.gravity / pen.length) * math.sin(pen.q)

if __name__ == '__main__':
    canvas_size = 800
    pendulum_radius_mm = 300
    px_per_mm = 1
    render_hz = 60
    sim_hz = 3000
    steps_per_frame = sim_hz // render_hz

    pygame.init()
    pygame.display.set_caption("Pendulum Simulation")
    screen = pygame.display.set_mode((canvas_size, canvas_size))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)

    pen = Pendulum(
        mass=1.0,
        length=pendulum_radius_mm,
        gravity=9810,
        q=math.pi / 2,
        qd=0.0,
    )
    painter = PendulumPainter(
        center=(canvas_size // 2, canvas_size // 2),
        swing_radius_mm=pendulum_radius_mm,
        px_per_mm=px_per_mm,
    )

    running = True
    painter.set_reference_angle(math.pi / 2)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for _ in range(steps_per_frame):
            qdd = equ_of_motion(pen)
            pen.qd += qdd / sim_hz
            pen.q += pen.qd / sim_hz

        painter.set_angle(pen.q)

        painter.draw(screen, font)
        pygame.display.flip()

        clock.tick(render_hz)
    
    pygame.quit()