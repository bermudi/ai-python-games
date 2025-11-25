import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spinning Hexagon with Bouncing Ball")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Hexagon parameters
hexagon_center = (width // 2, height // 2)
hexagon_radius = 150
num_sides = 6
rotation_angle = 0

# Ball parameters
ball_x = width // 2
ball_y = height // 4
ball_radius = 20
ball_velocity_x = 5
ball_velocity_y = 5
gravity = 0.5
damping = 0.8  # Coefficient of restitution (bounciness)

def calculate_hexagon_vertices(center, radius, angle):
    vertices = []
    for i in range(num_sides):
        angle_rad = math.radians(angle + i * 360 / num_sides)
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] + radius * math.sin(angle_rad)
        vertices.append((int(x), int(y)))
    return vertices

def rotate_point(x, y, angle, center):
    angle_rad = math.radians(angle)
    x -= center[0]
    y -= center[1]
    new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
    new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
    new_x += center[0]
    new_y += center[1]
    return int(new_x), int(new_y)

def distance_point_to_line(point, line_start, line_end):
    # Calculate the distance from a point to a line segment
    x0, y0 = point
    x1, y1 = line_start
    x2, y2 = line_end
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        # Line is a point
        return math.sqrt((x0 - x1)**2 + (y0 - y1)**2)
    t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx**2 + dy**2)
    t = max(0, min(1, t))  # Clamp t to the range [0, 1]
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    return math.sqrt((x0 - closest_x)**2 + (y0 - closest_y)**2), (closest_x, closest_y)

def reflect_vector(incident_x, incident_y, normal_x, normal_y):
    # Reflect a vector (incident_x, incident_y) across a normal vector (normal_x, normal_y)
    dot_product = incident_x * normal_x + incident_y * normal_y
    reflected_x = incident_x - 2 * normal_x * dot_product
    reflected_y = incident_y - 2 * normal_y * dot_product
    return reflected_x, reflected_y

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(black)

    # Update hexagon rotation
    rotation_angle += 1
    rotated_vertices = calculate_hexagon_vertices(hexagon_center, hexagon_radius, rotation_angle)

    # Update ball position
    ball_velocity_y += gravity
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y

    # Collision detection
    for i in range(num_sides):
        line_start = rotated_vertices[i]
        line_end = rotated_vertices[(i + 1) % num_sides]
        distance, closest_point = distance_point_to_line((ball_x, ball_y), line_start, line_end)

        if distance <= ball_radius:
            # Collision occurred
            # Calculate normal vector (vector from closest point on the line to the ball's center)
            normal_x = ball_x - closest_point[0]
            normal_y = ball_y - closest_point[1]
            normal_length = math.sqrt(normal_x**2 + normal_y**2)
            normal_x /= normal_length
            normal_y /= normal_length

            # Reflect the ball's velocity
            ball_velocity_x, ball_velocity_y = reflect_vector(ball_velocity_x, ball_velocity_y, normal_x, normal_y)
            ball_velocity_x *= damping
            ball_velocity_y *= damping

            # Move the ball slightly out of the collision
            ball_x += normal_x * (ball_radius - distance)
            ball_y += normal_y * (ball_radius - distance)


    # Draw hexagon
    pygame.draw.polygon(screen, white, rotated_vertices, 2)

    # Draw ball
    pygame.draw.circle(screen, red, (int(ball_x), int(ball_y)), ball_radius)

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()