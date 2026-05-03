import math

import pygame


CANVAS_SIZE = 800
PENDULUM_DIAMETER_MM = 600
PX_PER_MM = 1
FPS = 60


class PendulumPainter:
    """Draw-only pendulum view.

    Angle convention:
    - 0 degrees points vertically downward.
    - Positive degrees rotate counterclockwise.
    """

    def __init__(
        self,
        center: tuple[int, int],
        swing_diameter_mm: int = PENDULUM_DIAMETER_MM,
        px_per_mm: int = PX_PER_MM,
    ) -> None:
        self.center = pygame.Vector2(center)
        self.length_px = swing_diameter_mm * px_per_mm / 2
        self.angle_deg = 0.0

        self.background_color = (248, 249, 251)
        self.guide_color = (214, 220, 228)
        self.rod_color = (35, 43, 54)
        self.bob_color = (231, 91, 77)
        self.pivot_color = (28, 36, 48)
        self.text_color = (61, 69, 82)

    def set_angle(self, angle_deg: float) -> None:
        self.angle_deg = angle_deg % 360

    def bob_position(self) -> pygame.Vector2:
        angle_rad = math.radians(self.angle_deg)
        offset = pygame.Vector2(
            -math.sin(angle_rad) * self.length_px,
            math.cos(angle_rad) * self.length_px,
        )
        return self.center + offset

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        surface.fill(self.background_color)

        center_xy = (round(self.center.x), round(self.center.y))
        length_px = round(self.length_px)

        pygame.draw.circle(
            surface,
            self.guide_color,
            center_xy,
            length_px,
            width=1,
        )
        pygame.draw.line(
            surface,
            (230, 234, 240),
            (center_xy[0], center_xy[1] - length_px),
            (center_xy[0], center_xy[1] + length_px),
            width=1,
        )
        pygame.draw.line(
            surface,
            (230, 234, 240),
            (center_xy[0] - length_px, center_xy[1]),
            (center_xy[0] + length_px, center_xy[1]),
            width=1,
        )

        bob = self.bob_position()
        bob_xy = (round(bob.x), round(bob.y))
        pygame.draw.line(surface, self.rod_color, center_xy, bob_xy, width=6)
        pygame.draw.circle(surface, self.bob_color, bob_xy, 26)
        pygame.draw.circle(surface, (142, 47, 40), bob_xy, 26, width=3)
        pygame.draw.circle(surface, self.pivot_color, center_xy, 10)

        label = font.render(f"angle: {self.angle_deg:6.1f} deg", True, self.text_color)
        surface.blit(label, (24, 24))


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Pendulum Painter")

    screen = pygame.display.set_mode((CANVAS_SIZE, CANVAS_SIZE))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)

    pendulum = PendulumPainter(center=(CANVAS_SIZE // 2, CANVAS_SIZE // 2))
    angular_speed_deg_per_sec = 45.0
    angle = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        angle += angular_speed_deg_per_sec * dt
        pendulum.set_angle(angle)
        pendulum.draw(screen, font)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
