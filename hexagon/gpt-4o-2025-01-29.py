import pygame
import numpy as np
import math

######
# Two-shot: had to fix runtime error.
######

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
CENTER = np.array([WIDTH // 2, HEIGHT // 2])
HEX_RADIUS = 200
BALL_RADIUS = 10
GRAVITY = 0.3
FRICTION = 0.99  # Damping to prevent infinite bouncing
ROTATION_SPEED = 0.02  # Radians per frame

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Define hexagon vertices
def get_hexagon_vertices(center, radius, angle_offset=0):
    vertices = []
    for i in range(6):
        angle = angle_offset + math.pi / 3 * i
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        vertices.append(np.array([x, y]))
    return vertices

# Reflect velocity based on normal
def reflect_velocity(velocity, normal):
    return velocity - 2 * np.dot(velocity, normal) * normal

# Ball properties
ball_pos = np.array([CENTER[0], CENTER[1] - HEX_RADIUS // 2], dtype=float)  # FIXED: Ensure floating-point calculations
ball_vel = np.array([2, 0], dtype=float)  # Ensure velocity is also float

running = True
angle = 0  # Rotation angle

while running:
    screen.fill((0, 0, 0))
    angle += ROTATION_SPEED  # Rotate hexagon

    # Get rotated hexagon vertices
    hexagon_vertices = get_hexagon_vertices(CENTER, HEX_RADIUS, angle)

    # Draw hexagon
    pygame.draw.polygon(screen, (0, 255, 0), hexagon_vertices, 2)

    # Update ball position
    ball_vel[1] += GRAVITY  # Gravity effect
    ball_pos += ball_vel

    # Ball-hexagon collision detection
    for i in range(6):
        p1, p2 = hexagon_vertices[i], hexagon_vertices[(i + 1) % 6]
        edge = p2 - p1
        edge_normal = np.array([-edge[1], edge[0]])  # Perpendicular vector
        edge_normal /= np.linalg.norm(edge_normal)  # Normalize

        # Compute distance from ball to edge
        ball_to_edge = ball_pos - p1
        distance = np.dot(ball_to_edge, edge_normal)

        if abs(distance) < BALL_RADIUS:  # Collision detected
            ball_vel = reflect_velocity(ball_vel, edge_normal) * FRICTION
            ball_pos -= edge_normal * (BALL_RADIUS - abs(distance))  # Prevent sinking

    # Draw ball
    pygame.draw.circle(screen, (255, 0, 0), ball_pos.astype(int), BALL_RADIUS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)  # Frame rate

pygame.quit()