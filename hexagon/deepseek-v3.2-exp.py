import pygame
import sys
import math
import numpy as np

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bouncing in a Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Physics parameters
FPS = 60
GRAVITY = 0.5
FRICTION = 0.99
BOUNCE_DAMPING = 0.8

# Hexagon parameters
HEX_RADIUS = 300
HEX_CENTER = (WIDTH // 2, HEIGHT // 2)
ROTATION_SPEED = 0.01  # radians per frame

# Ball parameters
BALL_RADIUS = 20
ball_pos = np.array([WIDTH // 2, HEIGHT // 2 - 100], dtype=float)
ball_vel = np.array([2.0, 0.0], dtype=float)

def get_hexagon_vertices(angle):
    """Calculate the vertices of the hexagon at a given rotation angle"""
    vertices = []
    for i in range(6):
        theta = angle + i * (2 * math.pi / 6)
        x = HEX_CENTER[0] + HEX_RADIUS * math.cos(theta)
        y = HEX_CENTER[1] + HEX_RADIUS * math.sin(theta)
        vertices.append((x, y))
    return vertices

def get_hexagon_edges(vertices):
    """Get the edges of the hexagon as line segments"""
    edges = []
    for i in range(6):
        edges.append((vertices[i], vertices[(i + 1) % 6]))
    return edges

def distance_point_to_line(point, line_start, line_end):
    """Calculate the distance from a point to a line segment"""
    line_vec = np.array(line_end) - np.array(line_start)
    point_vec = np.array(point) - np.array(line_start)
    line_len = np.linalg.norm(line_vec)
    line_unitvec = line_vec / line_len
    point_vec_scaled = point_vec / line_len
    t = np.dot(line_unitvec, point_vec_scaled)
    
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
        
    nearest = np.array(line_start) + t * line_vec
    dist = np.linalg.norm(np.array(point) - nearest)
    return dist, nearest

def reflect_velocity(velocity, normal):
    """Reflect velocity vector across a normal vector"""
    normal = normal / np.linalg.norm(normal)  # Normalize
    return velocity - 2 * np.dot(velocity, normal) * normal

# Main game loop
clock = pygame.time.Clock()
rotation_angle = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear screen
    screen.fill(BLACK)
    
    # Update rotation
    rotation_angle += ROTATION_SPEED
    
    # Get hexagon vertices and edges
    hex_vertices = get_hexagon_vertices(rotation_angle)
    hex_edges = get_hexagon_edges(hex_vertices)
    
    # Apply gravity
    ball_vel[1] += GRAVITY
    
    # Apply friction
    ball_vel *= FRICTION
    
    # Update ball position
    ball_pos += ball_vel
    
    # Check for collisions with hexagon edges
    for edge in hex_edges:
        dist, nearest = distance_point_to_line(ball_pos, edge[0], edge[1])
        
        if dist <= BALL_RADIUS:
            # Calculate normal vector (perpendicular to the edge)
            edge_vec = np.array(edge[1]) - np.array(edge[0])
            normal = np.array([-edge_vec[1], edge_vec[0]])
            normal = normal / np.linalg.norm(normal)
            
            # Make sure normal points toward the ball
            if np.dot(normal, ball_pos - nearest) < 0:
                normal = -normal
            
            # Move ball outside the edge
            penetration = BALL_RADIUS - dist
            ball_pos += normal * penetration
            
            # Reflect velocity
            ball_vel = reflect_velocity(ball_vel, normal) * BOUNCE_DAMPING
    
    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, hex_vertices, 2)
    
    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()