# Bouncing ball inside a spinning hexagon with gravity and friction
# Requires: pip install pygame

import math
import sys

import pygame

# ---------------------------
# Config
# ---------------------------
SCREEN_W, SCREEN_H = 900, 700
FPS = 120

HEX_RADIUS = 240.0  # Hexagon circumradius (center to vertex)
HEX_OMEGA = 1.1  # Hexagon angular speed (rad/s), positive = CCW
HEX_LINE_WIDTH = 6

BALL_RADIUS = 18.0
BALL_COLOR = (250, 230, 80)
BG_COLOR = (16, 18, 24)
HEX_COLOR = (90, 180, 255)
HEX_INSIDE_FILL = (30, 40, 55)

GRAVITY = 1300.0  # px/s^2 downward
AIR_DRAG = 0.02  # per second, linear damping
RESTITUTION = 0.72  # normal bounce [0..1]
FRICTION_MU = 0.25  # Coulomb friction coefficient

# ---------------------------
# Math utilities
# ---------------------------


def clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x


def vec_len(x, y):
    return math.hypot(x, y)


def normalize(x, y):
    l = math.hypot(x, y)
    if l == 0:
        return 0.0, 0.0
    return x / l, y / l


# ---------------------------
# Simulation
# ---------------------------


class Ball:
    def __init__(self, pos, radius):
        self.pos = list(pos)  # [x, y]
        self.vel = [220.0, 0.0]
        self.r = radius
        self.mass = (
            1.0  # can be proportional to area; 1 simplifies friction computation
        )


class SpinningHex:
    def __init__(self, center, radius, omega=0.0):
        self.center = list(center)
        self.r = radius
        self.omega = omega
        self.theta = 0.0

        # Precompute base vertices for a regular hexagon on the unit circle
        self.base_vertices = [
            (math.cos(math.radians(60 * i)), math.sin(math.radians(60 * i)))
            for i in range(6)
        ]

    def update(self, dt):
        self.theta += self.omega * dt

    def get_world_vertices(self):
        c = self.center
        ct = math.cos(self.theta)
        st = math.sin(self.theta)
        verts = []
        for ux, uy in self.base_vertices:
            x = c[0] + self.r * (ux * ct - uy * st)
            y = c[1] + self.r * (ux * st + uy * ct)
            verts.append((x, y))
        return verts


# ---------------------------
# Physics: circle vs rotating segment
# ---------------------------


def resolve_ball_vs_rotating_segment(
    ball, p1, p2, wall_velocity_at_contact, restitution, mu
):
    """
    Resolve collision and friction between a moving circle (ball) and a rotating line segment.
    - p1, p2: segment endpoints (world coordinates)
    - wall_velocity_at_contact: [vx, vy] velocity of the wall at the contact point
    - restitution: coefficient of restitution [0..1]
    - mu: friction coefficient
    """
    # Tangent and outward normal (points from wall into interior)
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    seg_len = math.hypot(dx, dy)
    if seg_len < 1e-9:
        return False

    tx = dx / seg_len
    ty = dy / seg_len
    nx = ty  # perpendicular to tangent
    ny = -tx

    # Signed distance from ball center to the infinite line (positive if center is inside the half-plane of the normal)
    # Using point p1 to define the line
    cx = ball.pos[0] - p1[0]
    cy = ball.pos[1] - p1[1]
    s = cx * nx + cy * ny

    # Projection along the segment
    t = cx * tx + cy * ty

    if t < 0.0 or t > seg_len:
        return False  # Contact not within segment span

    penetration = ball.r - s
    if penetration <= 0.0:
        return False

    # Positional correction (push ball inside)
    ball.pos[0] += nx * penetration
    ball.pos[1] += ny * penetration

    # Relative velocity at contact
    v_rel_x = ball.vel[0] - wall_velocity_at_contact[0]
    v_rel_y = ball.vel[1] - wall_velocity_at_contact[1]
    v_n = v_rel_x * nx + v_rel_y * ny

    # Only apply bounce if moving into the wall
    if v_n < 0.0:
        jn = -(1.0 + restitution) * v_n * ball.mass

        # Normal impulse
        ball.vel[0] += (jn * nx) / ball.mass
        ball.vel[1] += (jn * ny) / ball.mass

        # Friction impulse (Coulomb)
        # Recompute relative velocity after normal impulse
        v_rel_x = ball.vel[0] - wall_velocity_at_contact[0]
        v_rel_y = ball.vel[1] - wall_velocity_at_contact[1]
        v_t = v_rel_x * tx + v_rel_y * ty
        jt_max = mu * jn
        jt = -v_t * ball.mass
        jt = clamp(jt, -jt_max, jt_max)

        ball.vel[0] += (jt * tx) / ball.mass
        ball.vel[1] += (jt * ty) / ball.mass

    return True


# ---------------------------
# Rendering helpers
# ---------------------------


def draw_hex(surface, verts, color, width):
    pygame.draw.polygon(surface, color, [(int(x), int(y)) for x, y in verts], width)


def draw_ball(surface, ball, color):
    pygame.draw.circle(
        surface, color, (int(ball.pos[0]), int(ball.pos[1])), int(ball.r)
    )


# ---------------------------
# Main
# ---------------------------


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Ball in a Spinning Hexagon")
    clock = pygame.time.Clock()

    center = (SCREEN_W * 0.5, SCREEN_H * 0.55)
    hexa = SpinningHex(center, HEX_RADIUS, HEX_OMEGA)
    ball = Ball((center[0] + 20.0, center[1] - HEX_RADIUS * 0.4), BALL_RADIUS)

    font = pygame.font.SysFont(None, 22)

    running = True
    paused = False
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    # Reset ball
                    ball.pos = [center[0] + 0.0, center[1] - HEX_RADIUS * 0.4]
                    ball.vel = [220.0, 0.0]
                elif event.key == pygame.K_LEFT:
                    hexa.omega -= 0.2
                elif event.key == pygame.K_RIGHT:
                    hexa.omega += 0.2
                elif event.key == pygame.K_UP:
                    # Nudge ball upward
                    ball.vel[1] -= 200.0
                elif event.key == pygame.K_DOWN:
                    # Nudge ball downward
                    ball.vel[1] += 200.0

        if not paused:
            # Integrate forces
            # Gravity
            ball.vel[1] += GRAVITY * dt
            # Air drag (simple linear damping)
            drag = max(0.0, 1.0 - AIR_DRAG * dt)
            ball.vel[0] *= drag
            ball.vel[1] *= drag

            # Integrate position (semi-implicit Euler)
            ball.pos[0] += ball.vel[0] * dt
            ball.pos[1] += ball.vel[1] * dt

            # Update hex
            hexa.update(dt)

            # Resolve collisions with all 6 edges, iterate a few times to handle corners
            verts = hexa.get_world_vertices()
            # Repeat a few times to handle near-vertex deep penetrations
            for _ in range(3):
                collided_any = False
                for i in range(6):
                    p1 = verts[i]
                    p2 = verts[(i + 1) % 6]
                    # Wall velocity at the segment midpoint (assuming rigid body rotation about hex center)
                    # v_wall = omega x r -> [-omega*ry, omega*rx]
                    mx = 0.5 * (p1[0] + p2[0])
                    my = 0.5 * (p1[1] + p2[1])
                    rx = mx - hexa.center[0]
                    ry = my - hexa.center[1]
                    vwx = -hexa.omega * ry
                    vwy = hexa.omega * rx

                    if resolve_ball_vs_rotating_segment(
                        ball, p1, p2, (vwx, vwy), RESTITUTION, FRICTION_MU
                    ):
                        collided_any = True
                if not collided_any:
                    break

        # Drawing
        screen.fill(BG_COLOR)

        # Fill interior softly
        verts = hexa.get_world_vertices()
        pygame.draw.polygon(
            screen, HEX_INSIDE_FILL, [(int(x), int(y)) for x, y in verts]
        )

        # Draw hexagon outline
        draw_hex(screen, verts, HEX_COLOR, HEX_LINE_WIDTH)

        # Draw ball
        draw_ball(screen, ball, BALL_COLOR)

        # HUD
        hud_lines = [
            f"omega: {hexa.omega:+.2f} rad/s  |  mu: {FRICTION_MU:.2f}  e: {RESTITUTION:.2f}",
            "Controls: SPACE pause, R reset, arrows: change omega, Up/Down nudge ball",
        ]
        y = 10
        for line in hud_lines:
            surf = font.render(line, True, (220, 220, 230))
            screen.blit(surf, (10, y))
            y += 20

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
