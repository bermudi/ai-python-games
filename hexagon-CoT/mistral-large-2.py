import pygame
import math

######
# Two-shot: had to fix runtime error.
######


# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spinning Hexagon with Bouncing Ball")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Hexagon properties
hex_radius = 100
hex_vertices_count = 6
hex_angle = 0

def calculate_hex_vertices(radius, angle):
    vertices = []
    for i in range(hex_vertices_count):
        x = screen_width // 2 + radius * math.cos(angle + 2 * math.pi * i / hex_vertices_count)
        y = screen_height // 2 + radius * math.sin(angle + 2 * math.pi * i / hex_vertices_count)
        vertices.append((x, y))
    return vertices

hex_vertices_coords = calculate_hex_vertices(hex_radius, hex_angle)

# Ball properties
ball_radius = 10
ball_pos = [screen_width // 2, screen_height // 2]
ball_vel = [0, 0]
gravity = 0.5
bounce_factor = 0.8

def update_ball_position(ball_pos, ball_vel):
    ball_vel[1] += gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    return ball_pos, ball_vel

def check_collision(ball_pos, ball_vel, hex_vertices_coords):
    for i in range(hex_vertices_count):
        p1 = hex_vertices_coords[i]
        p2 = hex_vertices_coords[(i + 1) % hex_vertices_count]
        if intersects(ball_pos, ball_radius, p1, p2):
            ball_vel[0] *= -bounce_factor
            ball_vel[1] *= -bounce_factor
    return ball_vel

def intersects(ball_pos, ball_radius, p1, p2):
    # Simplified collision detection for the sake of example
    # Calculate the distance from the ball to the line segment
    line_length = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    if line_length == 0:
        return False

    t = ((ball_pos[0] - p1[0]) * (p2[0] - p1[0]) + (ball_pos[1] - p1[1]) * (p2[1] - p1[1])) / line_length**2
    t = max(0, min(1, t))

    nearest_x = p1[0] + t * (p2[0] - p1[0])
    nearest_y = p1[1] + t * (p2[1] - p1[1])

    distance = math.sqrt((ball_pos[0] - nearest_x)**2 + (ball_pos[1] - nearest_y)**2)

    return distance <= ball_radius

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon rotation
    hex_angle += 0.01
    hex_vertices_coords = calculate_hex_vertices(hex_radius, hex_angle)

    # Update ball position and collision
    ball_pos, ball_vel = update_ball_position(ball_pos, ball_vel)
    ball_vel = check_collision(ball_pos, ball_vel, hex_vertices_coords)

    # Draw everything
    screen.fill(black)
    pygame.draw.polygon(screen, white, hex_vertices_coords, 2)
    pygame.draw.circle(screen, white, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()