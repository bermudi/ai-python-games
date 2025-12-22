import math

import pygame

# --- Configuration Constants ---
WIDTH, HEIGHT = 800, 800
FPS = 60

# Colors
COLOR_BG = (15, 15, 20)
COLOR_HEXAGON = (200, 200, 200)
COLOR_BALL = (255, 80, 80)
COLOR_ACCENT = (0, 255, 255)

# Physics Constants
GRAVITY = 0.25  # Downward acceleration per frame
FRICTION_AIR = 0.999  # Air resistance (1.0 = none, <1.0 = drag)
FRICTION_WALL = 0.99  # Tangential friction on bounce
RESTITUTION = 0.85  # Bounciness (1.0 = perfectly elastic, <1.0 = energy loss)
HEX_RADIUS = 300
HEX_ROTATION_SPEED = 0.015  # Radians per frame
BALL_RADIUS = 15
INITIAL_SPEED = 5.0


class Vector:
    """A simple 2D Vector class to handle physics math without numpy."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        m = self.magnitude()
        if m == 0:
            return Vector(0, 0)
        return Vector(self.x / m, self.y / m)

    def rotate(self, angle):
        """Rotate vector by angle (radians)."""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector(self.x * cos_a - self.y * sin_a, self.x * sin_a + self.y * cos_a)

    def to_tuple(self):
        return (int(self.x), int(self.y))


class Ball:
    def __init__(self, x, y):
        self.pos = Vector(x, y)
        self.vel = Vector(INITIAL_SPEED, 0)
        self.radius = BALL_RADIUS
        self.color = COLOR_BALL

    def update(self):
        # Apply Gravity
        self.vel.y += GRAVITY

        # Apply Air Friction
        self.vel = self.vel * FRICTION_AIR

        # Update Position
        self.pos = self.pos + self.vel

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos.to_tuple(), self.radius)
        # Draw a slight shine/highlight
        pygame.draw.circle(
            surface,
            (255, 150, 150),
            (int(self.pos.x - self.radius * 0.3), int(self.pos.y - self.radius * 0.3)),
            int(self.radius / 3),
        )


class Hexagon:
    def __init__(self, center_x, center_y, radius):
        self.center = Vector(center_x, center_y)
        self.radius = radius
        self.angle = 0.0
        self.angular_velocity = HEX_ROTATION_SPEED
        self.vertices = []

    def update(self):
        self.angle += self.angular_velocity
        self.update_vertices()

    def update_vertices(self):
        self.vertices = []
        for i in range(6):
            # Calculate vertex position based on current rotation angle
            theta = self.angle + i * (math.pi / 3)
            x = self.center.x + self.radius * math.cos(theta)
            y = self.center.y + self.radius * math.sin(theta)
            self.vertices.append(Vector(x, y))

    def draw(self, surface):
        points = [v.to_tuple() for v in self.vertices]
        pygame.draw.polygon(surface, COLOR_HEXAGON, points, 5)

        # Draw center pivot
        pygame.draw.circle(surface, COLOR_ACCENT, self.center.to_tuple(), 4)

    def get_walls(self):
        """Returns a list of tuples (p1, p2) representing the walls."""
        walls = []
        for i in range(6):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % 6]
            walls.append((p1, p2))
        return walls


def closest_point_on_segment(seg_a, seg_b, point):
    """Finds the closest point on line segment AB to Point P."""
    seg_v = seg_b - seg_a
    if seg_v.magnitude() == 0:
        return seg_a

    pt_v = point - seg_a
    seg_len_sq = seg_v.magnitude() ** 2

    # Project point onto line (parameter t)
    t = pt_v.dot(seg_v) / seg_len_sq

    # Clamp t to segment [0, 1]
    t = max(0, min(1, t))

    return seg_a + seg_v * t


def resolve_collision(ball, hexagon):
    walls = hexagon.get_walls()

    collided = False

    for p1, p2 in walls:
        # 1. Geometry check: Find closest point on wall
        closest = closest_point_on_segment(p1, p2, ball.pos)
        dist_vec = ball.pos - closest
        dist = dist_vec.magnitude()

        # Check if ball is touching the wall
        if dist < ball.radius:
            collided = True

            # 2. Calculate Wall Normal
            # Normal vector of the wall.
            # For a hexagon defined counter-clockwise, the inward normal points "left" of the vector p2->p1
            wall_vec = p2 - p1
            normal = Vector(-wall_vec.y, wall_vec.x).normalize()

            # Ensure normal points towards the center of the hexagon (inward)
            to_center = hexagon.center - closest
            if normal.dot(to_center) < 0:
                normal = normal * -1

            # 3. Positional Correction (prevent sinking)
            # Push the ball out of the wall so it doesn't get stuck
            overlap = ball.radius - dist
            if dist == 0:
                # Fallback if centers exactly overlap
                correction = normal * ball.radius
            else:
                correction = dist_vec.normalize() * overlap

            ball.pos = ball.pos + correction

            # 4. Velocity Calculation with Rotating Wall
            # We need the velocity of the wall AT THE POINT OF IMPACT
            # V_wall = angular_velocity * radius_vector (cross product in 2D)
            r_vec = closest - hexagon.center
            # Tangent velocity vector of the wall at impact point
            # (-y, x) rotates 90 degrees counter-clockwise
            wall_vel = Vector(-r_vec.y, r_vec.x) * hexagon.angular_velocity

            # 5. Relative Velocity
            # Transform ball velocity into the wall's reference frame
            rel_vel = ball.vel - wall_vel

            # 6. Reflection
            # V_new = V_old - 2(V_old . Normal) * Normal
            # We separate it into Normal and Tangential components
            vel_along_normal = rel_vel.dot(normal)

            # Only bounce if moving towards the wall
            if vel_along_normal < 0:
                # Elastic bounce with restitution (bounciness)
                j = -(1 + RESTITUTION) * vel_along_normal
                impulse = normal * j

                # Apply friction to tangential component
                # Tangent vector
                tangent = Vector(-normal.y, normal.x)
                vel_along_tangent = rel_vel.dot(tangent)

                # Apply wall friction to the tangential part
                friction_impulse = tangent * (-vel_along_tangent * (1 - FRICTION_WALL))

                # Update relative velocity
                rel_vel = rel_vel + impulse + friction_impulse

                # 7. Convert back to World Frame
                ball.vel = rel_vel + wall_vel

    return collided


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")
    clock = pygame.time.Clock()

    # Initialize Objects
    hexagon = Hexagon(WIDTH // 2, HEIGHT // 2, HEX_RADIUS)
    ball = Ball(WIDTH // 2, HEIGHT // 2 - 100)

    running = True
    paused = False

    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    # Reset ball
                    ball.pos = Vector(WIDTH // 2, HEIGHT // 2 - 100)
                    ball.vel = Vector(INITIAL_SPEED, 0)
                elif event.key == pygame.K_UP:
                    hexagon.angular_velocity += 0.005
                elif event.key == pygame.K_DOWN:
                    hexagon.angular_velocity -= 0.005

        # 2. Physics Update
        if not paused:
            # We can sub-step physics for better stability if needed,
            # but 60 FPS is usually fine for this simple sim.
            ball.update()
            hexagon.update()

            # Check collision multiple times per frame if speed is high (optional)
            # Here we do it once
            resolve_collision(ball, hexagon)

        # 3. Drawing
        screen.fill(COLOR_BG)

        # Draw Hexagon
        hexagon.draw(screen)

        # Draw Ball
        ball.draw(screen)

        # UI Info
        font = pygame.font.SysFont("monospace", 16)
        info_text = [
            f"Rotation Speed: {hexagon.angular_velocity:.3f} rad/frame",
            f"Ball Velocity: {ball.vel.magnitude():.2f}",
            "Controls: Space (Pause), R (Reset), Up/Down (Spin Speed)",
        ]

        for i, line in enumerate(info_text):
            text_surf = font.render(line, True, (150, 150, 150))
            screen.blit(text_surf, (10, 10 + i * 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
