import pygame
import math
import time

# --- Initialization ---
pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

GRAVITY = 0.5  # Adjust as needed
FRICTION = 0.999  # Adjust as needed. Closer to 1 means less friction.
RESTITUTION = 0.7  # Coefficient of restitution (bounciness)
HEXAGON_SIZE = 150 # Side Length
BALL_RADIUS = 15
ROTATION_SPEED = 0.01  # Radians per frame
FPS = 60


# --- Helper Functions ---

def rotate_point(point, angle, center=(0, 0)):
    """Rotates a point around a center point."""
    x, y = point
    cx, cy = center
    x -= cx
    y -= cy
    rotated_x = x * math.cos(angle) - y * math.sin(angle)
    rotated_y = x * math.sin(angle) + y * math.cos(angle)
    return rotated_x + cx, rotated_y + cy

def distance(p1, p2):
    """Calculates the distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def closest_point_on_line(ball_pos, p1, p2):
    """Finds the closest point on a line segment to a given point."""
    x1, y1 = p1
    x2, y2 = p2
    x0, y0 = ball_pos

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:  # It's a point, not a line segment
        return p1

    t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))  # Clamp t to be between 0 and 1 (within the segment)

    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    return closest_x, closest_y

def reflect_vector(vector, normal):
    """Reflects a vector across a normal vector."""
    vx, vy = vector
    nx, ny = normal
    dot_product = vx * nx + vy * ny
    reflected_x = vx - 2 * dot_product * nx
    reflected_y = vy - 2 * dot_product * ny
    return reflected_x, reflected_y

def normalize_vector(vector):
    """Normalizes a vector (makes it unit length)."""
    vx, vy = vector
    magnitude = math.sqrt(vx**2 + vy**2)
    if magnitude == 0:  # Avoid division by zero
       return 0, 0
    return vx / magnitude, vy / magnitude

# --- Hexagon Class ---

class Hexagon:
    def __init__(self, size, center):
        self.size = size
        self.center = center
        self.angle = 0
        self.vertices = self._calculate_vertices()

    def _calculate_vertices(self):
        """Calculates the vertices of the hexagon."""
        vertices = []
        for i in range(6):
            angle = math.radians(60 * i)
            x = self.center[0] + self.size * math.cos(angle)
            y = self.center[1] + self.size * math.sin(angle)
            vertices.append((x, y))
        return vertices

    def rotate(self, angle):
        """Rotates the hexagon."""
        self.angle += angle
        self.vertices = [rotate_point(v, self.angle, self.center) for v in self._calculate_vertices()]

    def draw(self, screen):
        """Draws the hexagon."""
        pygame.draw.polygon(screen, BLUE, self.vertices, 2)

# --- Ball Class ---

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = radius

    def update(self, dt):
        """Updates the ball's position and velocity."""
        self.vy += GRAVITY * dt
        self.vx *= FRICTION
        self.vy *= FRICTION
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, screen):
        """Draws the ball."""
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

    def check_collision(self, hexagon):
        """Checks for collisions with the hexagon's edges."""
        for i in range(6):
            p1 = hexagon.vertices[i]
            p2 = hexagon.vertices[(i + 1) % 6]  # Wrap around to the first vertex

            closest_point = closest_point_on_line((self.x, self.y), p1, p2)
            dist = distance((self.x, self.y), closest_point)

            if dist < self.radius:
                # Collision detected!
                self.handle_collision(p1, p2, closest_point, dist)
                return  # Only handle one collision per frame

    def handle_collision(self, p1, p2, closest_point, dist):
        # Calculate the normal vector
        normal_x = self.x - closest_point[0]
        normal_y = self.y - closest_point[1]
        normal_x, normal_y = normalize_vector((normal_x, normal_y))

        # Reflect the velocity vector
        self.vx, self.vy = reflect_vector((self.vx, self.vy), (normal_x, normal_y))

        # Apply restitution
        self.vx *= RESTITUTION
        self.vy *= RESTITUTION

        # Penetration resolution (move the ball out of the wall)
        overlap = self.radius - dist
        self.x += normal_x * overlap
        self.y += normal_y * overlap

# --- Game Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")
clock = pygame.time.Clock()

hexagon = Hexagon(HEXAGON_SIZE, (WIDTH // 2, HEIGHT // 2))
ball = Ball(WIDTH // 2, HEIGHT // 4, BALL_RADIUS)

# --- Main Game Loop ---
running = True
while running:
    dt = clock.tick(FPS) / 1000  # Delta time in seconds

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update ---
    hexagon.rotate(ROTATION_SPEED)
    ball.update(dt)
    ball.check_collision(hexagon)


    # --- Draw ---
    screen.fill(WHITE)
    hexagon.draw(screen)
    ball.draw(screen)
    pygame.display.flip()

pygame.quit()