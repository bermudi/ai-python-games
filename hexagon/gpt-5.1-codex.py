import math
import sys
from typing import List

import pygame

WIDTH, HEIGHT = 800, 800
CENTER = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
HEX_RADIUS = 280
BALL_RADIUS = 16
GRAVITY = 900.0  # px / s^2
ROTATION_SPEED = math.radians(24)  # rad / s
RESTITUTION = 0.88
SURFACE_FRICTION = 0.82
AIR_DRAG = 0.12  # proportional velocity damping per second
BACKGROUND = (14, 16, 20)
HEX_COLOR = (50, 200, 255)
BALL_COLOR = (255, 120, 80)
TRAIL_COLOR = (60, 80, 120)


def compute_hex_points(angle: float) -> List[pygame.Vector2]:
    points: List[pygame.Vector2] = []
    for i in range(6):
        theta = angle + i * math.tau / 6
        points.append(
            pygame.Vector2(
                CENTER.x + HEX_RADIUS * math.cos(theta),
                CENTER.y + HEX_RADIUS * math.sin(theta),
            )
        )
    return points


def resolve_collisions(ball_pos: pygame.Vector2, ball_vel: pygame.Vector2, points: List[pygame.Vector2]) -> None:
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        edge = p2 - p1
        normal = pygame.Vector2(-edge.y, edge.x)
        length = normal.length()
        if length == 0:
            continue
        normal /= length  # inward normal for CCW polygon
        distance = (ball_pos - p1).dot(normal)
        if distance < BALL_RADIUS:
            penetration = BALL_RADIUS - distance
            ball_pos += normal * penetration
            normal_velocity = ball_vel.dot(normal)
            if normal_velocity < 0:
                tangent_velocity = ball_vel - normal * normal_velocity
                tangent_velocity *= SURFACE_FRICTION
                ball_vel.update(tangent_velocity - normal * normal_velocity * RESTITUTION)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")
    clock = pygame.time.Clock()

    ball_pos = CENTER + pygame.Vector2(0, -100)
    ball_vel = pygame.Vector2(220, 0)
    angle = 0.0
    trail: List[pygame.Vector2] = []

    running = True
    while running:
        dt = clock.tick(120) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        angle += ROTATION_SPEED * dt
        hex_points = compute_hex_points(angle)

        ball_vel.y += GRAVITY * dt
        damping = max(0.0, 1.0 - AIR_DRAG * dt)
        ball_vel *= damping

        ball_pos += ball_vel * dt
        resolve_collisions(ball_pos, ball_vel, hex_points)

        trail.append(ball_pos.copy())
        if len(trail) > 60:
            trail.pop(0)

        screen.fill(BACKGROUND)
        if len(trail) > 1:
            pygame.draw.lines(
                screen,
                TRAIL_COLOR,
                False,
                [point.xy for point in trail],
                2,
            )
        pygame.draw.polygon(screen, HEX_COLOR, [point.xy for point in hex_points], width=3)
        pygame.draw.circle(screen, BALL_COLOR, ball_pos, BALL_RADIUS)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
