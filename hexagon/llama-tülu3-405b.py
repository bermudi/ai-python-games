import pygame
import math

# Initialize pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spinning Hexagon with Bouncing Ball")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

def draw_hexagon(center, radius, rotation_angle):
    points = []
    for i in range(6):
        angle = math.radians(60 * i + rotation_angle)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(screen, white, points, 2)

# Ball properties
ball_pos = [400, 300]
ball_velocity = [2, 2]
ball_radius = 10
gravity = 0.5

def update_ball_position():
    global ball_pos, ball_velocity
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]
    ball_velocity[1] += gravity  # Apply gravity

def check_wall_collision():
    global ball_pos, ball_velocity, screen_width, screen_height, ball_radius
    if ball_pos[0] - ball_radius <= 0 or ball_pos[0] + ball_radius >= screen_width:
        ball_velocity[0] *= -1
    if ball_pos[1] - ball_radius <= 0 or ball_pos[1] + ball_radius >= screen_height:
        ball_velocity[1] *= -0.8  # Damping factor for energy loss

def check_hexagon_collision(center, radius, rotation_angle):
    global ball_pos, ball_velocity
    points = []
    for i in range(6):
        angle = math.radians(60 * i + rotation_angle)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    
    # Check for collision with each edge of the hexagon
    for i in range(6):
        p1 = points[i]
        p2 = points[(i + 1) % 6]
        # Line equation parameters
        A = p2[1] - p1[1]
        B = p1[0] - p2[0]
        C = p2[0] * p1[1] - p1[0] * p2[1]
        
        # Distance from ball center to the line
        distance = abs(A * ball_pos[0] + B * ball_pos[1] + C) / math.sqrt(A**2 + B**2)
        
        if distance <= ball_radius:
            # Reflect the velocity
            normal_vector = [A, B]
            normal_magnitude = math.sqrt(normal_vector[0]**2 + normal_vector[1]**2)
            normal_vector = [normal_vector[0] / normal_magnitude, normal_vector[1] / normal_magnitude]
            dot_product = ball_velocity[0] * normal_vector[0] + ball_velocity[1] * normal_vector[1]
            ball_velocity[0] -= 2 * dot_product * normal_vector[0]
            ball_velocity[1] -= 2 * dot_product * normal_vector[1]
            break

running = True
rotation_angle = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    # Update rotation angle
    rotation_angle += 1
    if rotation_angle >= 360:
        rotation_angle = 0

    # Draw spinning hexagon
    draw_hexagon((400, 300), 150, rotation_angle)

    # Update ball position
    update_ball_position()

    # Check for collisions with walls and hexagon
    check_wall_collision()
    check_hexagon_collision((400, 300), 150, rotation_angle)

    # Draw the ball
    pygame.draw.circle(screen, red, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
