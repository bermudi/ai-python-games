import pygame
import math
import sys

# --- 1. Initialization and Constants ---

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Hexagon parameters
HEX_CENTER = (WIDTH // 2, HEIGHT // 2)
HEX_RADIUS = 150
HEX_ROTATION_SPEED = 0.02  # Radians per frame

# Ball parameters
BALL_RADIUS = 15
ball_pos = [WIDTH // 2, HEIGHT // 2 - 100]  # Initial position (list for mutability)
ball_velocity = [0, 0]  # Initial velocity
GRAVITY = 0.2
FRICTION = 0.99  # Air resistance (velocity reduction per frame)
BOUNCE_DAMPING = 0.8  # Energy loss on collision


# --- 2. Helper Functions ---

def calculate_hexagon_vertices(center, radius, rotation):
    """Calculates the vertices of the hexagon."""
    vertices = []
    for i in range(6):
        angle = math.radians(i * 60) + rotation  # Convert to radians, add rotation
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        vertices.append((x, y))
    return vertices

def point_in_polygon(point, vertices):
    """Checks if a point is inside a polygon (using ray casting)."""
    x, y = point
    n = len(vertices)
    inside = False

    p1x, p1y = vertices[0]
    for i in range(n + 1):
        p2x, p2y = vertices[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def distance(p1, p2):
    """Calculates the distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def closest_point_on_line(ball, p1, p2):
    """Finds the closest point on a line segment to the ball."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    if dx == 0 and dy == 0:  # It's a point, not a line segment
        return p1

    t = ((ball[0] - p1[0]) * dx + (ball[1] - p1[1]) * dy) / (dx**2 + dy**2)
    t = max(0, min(1, t))  # Clamp t to [0, 1] for line *segment*

    closest_x = p1[0] + t * dx
    closest_y = p1[1] + t * dy
    return closest_x, closest_y

def reflect_vector(v, n):
    """Reflects a vector 'v' across a normal 'n'."""
    dot_product = v[0] * n[0] + v[1] * n[1]
    reflected_v = [v[0] - 2 * dot_product * n[0],
                   v[1] - 2 * dot_product * n[1]]
    return reflected_v


# --- 3. Main Game Loop ---

def run_game():
    global ball_pos, ball_velocity, HEX_ROTATION_SPEED
    
    rotation = 0  # Initial rotation of the hexagon
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                     running = False

        # --- Update ---

        # 1. Apply Gravity and Friction
        ball_velocity[1] += GRAVITY
        ball_velocity[0] *= FRICTION
        ball_velocity[1] *= FRICTION

        # 2. Update Ball Position
        ball_pos[0] += ball_velocity[0]
        ball_pos[1] += ball_velocity[1]

        # 3. Calculate Hexagon Vertices
        vertices = calculate_hexagon_vertices(HEX_CENTER, HEX_RADIUS, rotation)

        # 4. Collision Detection and Response
        for i in range(6):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % 6]  # Wrap around to the first vertex

            closest_point = closest_point_on_line(ball_pos, p1, p2)
            dist = distance(ball_pos, closest_point)

            if dist < BALL_RADIUS:
                # Calculate normal vector (perpendicular to the edge)
                normal_x = ball_pos[0] - closest_point[0]
                normal_y = ball_pos[1] - closest_point[1]
                normal_magnitude = math.sqrt(normal_x**2 + normal_y**2)

                #Prevent division by zero.
                if normal_magnitude > 0:
                    normal_x /= normal_magnitude
                    normal_y /= normal_magnitude

                    # Reflect the ball's velocity
                    ball_velocity = reflect_vector(ball_velocity, [normal_x, normal_y])
                    ball_velocity[0] *= BOUNCE_DAMPING
                    ball_velocity[1] *= BOUNCE_DAMPING

                    # Move ball out of collision
                    overlap = BALL_RADIUS - dist
                    if normal_magnitude > 0:
                        ball_pos[0] += normal_x * overlap
                        ball_pos[1] += normal_y * overlap

        # 5. Rotate Hexagon
        rotation += HEX_ROTATION_SPEED

        # --- Draw ---

        screen.fill(BLACK)  # Clear screen

        # Draw Hexagon
        pygame.draw.polygon(screen, WHITE, vertices, 2)

        # Draw Ball
        pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

        pygame.display.flip()  # Update the display
        clock.tick(60) #60 frames per second.

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()