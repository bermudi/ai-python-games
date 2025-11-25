import pygame
import sys
import math
import numpy as np

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)
HEXAGON_COLOR = (100, 100, 255)
BALL_COLOR = (255, 100, 100)
HEXAGON_RADIUS = 300
BALL_RADIUS = 20
GRAVITY = 0.5
FRICTION = 0.98
RESTITUTION = 0.8  # Bounciness
ROTATION_SPEED = 0.01  # Radians per frame

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bouncing in a Spinning Hexagon")
clock = pygame.time.Clock()

# Hexagon vertices (initial position)
def get_hexagon_vertices(center, radius, rotation):
    vertices = []
    for i in range(6):
        angle = rotation + i * (2 * math.pi / 6)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        vertices.append((x, y))
    return vertices

# Calculate the normal vector for a line segment
def get_normal(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    length = math.sqrt(dx*dx + dy*dy)
    if length == 0:
        return (0, 0)
    # Normal vector (perpendicular to the line, pointing inward)
    return (-dy/length, dx/length)

# Ball class
class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 0
        self.vy = 0
    
    def update(self):
        # Apply gravity
        self.vy += GRAVITY
        
        # Apply friction
        self.vx *= FRICTION
        self.vy *= FRICTION
        
        # Update position
        self.x += self.vx
        self.y += self.vy
    
    def draw(self):
        pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), self.radius)
        # Draw a small dot to show rotation
        pygame.draw.circle(screen, (255, 255, 255), 
                          (int(self.x + self.radius/2 * math.cos(self.vx*5)), 
                           int(self.y + self.radius/2 * math.sin(self.vy*5))), 
                          self.radius//4)

# Create the ball
ball = Ball(WIDTH // 2, HEIGHT // 2 - 100, BALL_RADIUS)

# Main game loop
rotation = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # Add some initial velocity with arrow keys
            elif event.key == pygame.K_LEFT:
                ball.vx = -10
            elif event.key == pygame.K_RIGHT:
                ball.vx = 10
            elif event.key == pygame.K_UP:
                ball.vy = -10
            elif event.key == pygame.K_DOWN:
                ball.vy = 10
    
    # Update rotation
    rotation += ROTATION_SPEED
    
    # Get hexagon vertices
    center = (WIDTH // 2, HEIGHT // 2)
    hexagon_vertices = get_hexagon_vertices(center, HEXAGON_RADIUS, rotation)
    
    # Update ball position
    ball.update()
    
    # Check for collisions with hexagon walls
    for i in range(6):
        p1 = hexagon_vertices[i]
        p2 = hexagon_vertices[(i + 1) % 6]
        
        # Calculate the normal vector for this wall
        normal = get_normal(p1, p2)
        
        # Calculate the distance from the ball to the line segment
        # Using vector projection
        line_vec = (p2[0] - p1[0], p2[1] - p1[1])
        line_len = math.sqrt(line_vec[0]**2 + line_vec[1]**2)
        line_unit_vec = (line_vec[0] / line_len, line_vec[1] / line_len)
        
        ball_to_p1 = (ball.x - p1[0], ball.y - p1[1])
        projection_length = ball_to_p1[0] * line_unit_vec[0] + ball_to_p1[1] * line_unit_vec[1]
        
        # Clamp the projection to the line segment
        projection_length = max(0, min(line_len, projection_length))
        
        # Find the closest point on the line segment to the ball
        closest_point = (
            p1[0] + projection_length * line_unit_vec[0],
            p1[1] + projection_length * line_unit_vec[1]
        )
        
        # Calculate the distance from the ball to the closest point
        dist_x = ball.x - closest_point[0]
        dist_y = ball.y - closest_point[1]
        distance = math.sqrt(dist_x**2 + dist_y**2)
        
        # Check if the ball is colliding with this wall
        if distance < ball.radius:
            # Move the ball outside the wall
            overlap = ball.radius - distance
            ball.x += overlap * normal[0]
            ball.y += overlap * normal[1]
            
            # Calculate the relative velocity of the wall at the collision point
            # The wall is rotating, so points have tangential velocity
            wall_velocity = (
                -ROTATION_SPEED * (closest_point[1] - center[1]),
                ROTATION_SPEED * (closest_point[0] - center[0])
            )
            
            # Calculate the ball's velocity relative to the wall
            relative_vx = ball.vx - wall_velocity[0]
            relative_vy = ball.vy - wall_velocity[1]
            
            # Calculate the dot product of the relative velocity and the normal
            dot_product = relative_vx * normal[0] + relative_vy * normal[1]
            
            # If the ball is moving toward the wall, bounce it
            if dot_product < 0:
                # Calculate the reflection
                ball.vx = wall_velocity[0] + RESTITUTION * (relative_vx - 2 * dot_product * normal[0])
                ball.vy = wall_velocity[1] + RESTITUTION * (relative_vy - 2 * dot_product * normal[1])
    
    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    
    # Draw hexagon
    pygame.draw.polygon(screen, HEXAGON_COLOR, hexagon_vertices, 2)
    
    # Draw ball
    ball.draw()
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()