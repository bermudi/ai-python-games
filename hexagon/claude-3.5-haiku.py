import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spinning Hexagon with Bouncing Ball")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Hexagon properties
hexagon_radius = 200
hexagon_center = (WIDTH // 2, HEIGHT // 2)
hexagon_angle = 0
hexagon_rotation_speed = 0.01

# Ball properties
ball_radius = 20
ball_position = [hexagon_center[0], hexagon_center[1] - hexagon_radius + ball_radius]
ball_velocity = [2, 2]
gravity = 0.1

# Function to calculate hexagon vertices
def calculate_hexagon_vertices(center, radius, angle):
    vertices = []
    for i in range(6):
        x = center[0] + radius * math.cos(math.radians(60 * i) + angle)
        y = center[1] + radius * math.sin(math.radians(60 * i) + angle)
        vertices.append((x, y))
    return vertices

# Function to check if a point is inside a polygon
def point_inside_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon rotation
    hexagon_angle += hexagon_rotation_speed
    hexagon_vertices = calculate_hexagon_vertices(hexagon_center, hexagon_radius, hexagon_angle)

    # Update ball position and velocity
    ball_velocity[1] += gravity
    ball_position[0] += ball_velocity[0]
    ball_position[1] += ball_velocity[1]

    # Check for collisions with hexagon edges
    if not point_inside_polygon(ball_position, hexagon_vertices):
        # Simple reflection: reverse velocity
        ball_velocity[0] = -ball_velocity[0]
        ball_velocity[1] = -ball_velocity[1]

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.polygon(screen, BLACK, hexagon_vertices, 2)
    pygame.draw.circle(screen, RED, (int(ball_position[0]), int(ball_position[1])), ball_radius)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()