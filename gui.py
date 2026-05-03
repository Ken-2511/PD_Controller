import math
import pygame


class PendulumPainter:
    """Draw-only pendulum view.

    Angle convention:
    - 0 radians points vertically downward.
    - Positive radians rotate counterclockwise around +z, out of the page.
    """

    def __init__(
        self,
        center: tuple[int, int],
        swing_radius_mm: int,
        px_per_mm: int = 1,
    ) -> None:
        self.center = pygame.Vector2(center)
        self.length_px = swing_radius_mm * px_per_mm
        self.angle_rad = 0.0
        self.reference_angle_rad = 0.0

        self.background_color = (248, 249, 251)
        self.guide_color = (214, 220, 228)
        self.reference_color = (65, 125, 230)
        self.rod_color = (35, 43, 54)
        self.bob_color = (231, 91, 77)
        self.pivot_color = (28, 36, 48)
        self.text_color = (61, 69, 82)

    def set_angle(self, angle_rad: float) -> None:
        self.angle_rad = angle_rad % (2 * math.pi)

    def set_reference_angle(self, angle_rad: float) -> None:
        self.reference_angle_rad = angle_rad % (2 * math.pi)

    def position_from_angle(self, angle_rad: float) -> pygame.Vector2:
        # Pygame's screen y-axis points downward, so this maps from math xy
        # coordinates with +z out of the page into screen coordinates.
        offset = pygame.Vector2(
            math.sin(angle_rad) * self.length_px,
            math.cos(angle_rad) * self.length_px,
        )
        return self.center + offset

    def bob_position(self) -> pygame.Vector2:
        return self.position_from_angle(self.angle_rad)

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

        reference = self.position_from_angle(self.reference_angle_rad)
        reference_xy = (round(reference.x), round(reference.y))
        pygame.draw.line(surface, self.reference_color, center_xy, reference_xy, width=3)
        pygame.draw.circle(surface, self.reference_color, reference_xy, 12, width=3)

        bob = self.bob_position()
        bob_xy = (round(bob.x), round(bob.y))
        pygame.draw.line(surface, self.rod_color, center_xy, bob_xy, width=6)
        pygame.draw.circle(surface, self.bob_color, bob_xy, 26)
        pygame.draw.circle(surface, (142, 47, 40), bob_xy, 26, width=3)
        pygame.draw.circle(surface, self.pivot_color, center_xy, 10)

        angle_deg = math.degrees(self.angle_rad)
        label = font.render(
            f"angle: {self.angle_rad:5.2f} rad / {angle_deg:6.1f} deg",
            True,
            self.text_color,
        )
        surface.blit(label, (24, 24))

        reference_deg = math.degrees(self.reference_angle_rad)
        reference_label = font.render(
            f"ref:   {self.reference_angle_rad:5.2f} rad / {reference_deg:6.1f} deg",
            True,
            self.reference_color,
        )
        surface.blit(reference_label, (24, 52))


def main() -> None:
    canvas_size = 800
    pendulum_radius_mm = 300
    px_per_mm = 1
    fps = 60

    pygame.init()
    pygame.display.set_caption("Pendulum Painter")

    screen = pygame.display.set_mode((canvas_size, canvas_size))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)

    pendulum = PendulumPainter(
        center=(canvas_size // 2, canvas_size // 2),
        swing_radius_mm=pendulum_radius_mm,
        px_per_mm=px_per_mm,
    )
    angular_speed_rad_per_sec = math.radians(45.0)
    pendulum.set_reference_angle(math.radians(90.0))
    angle = 0.0

    running = True
    while running:
        dt = clock.tick(fps) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        angle += angular_speed_rad_per_sec * dt
        pendulum.set_angle(angle)
        pendulum.draw(screen, font)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
