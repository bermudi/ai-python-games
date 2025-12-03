import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60
GRAVITY = 500  # pixels/s^2
FRICTION_COEFFICIENT = 0.98  # Air resistance
WALL_FRICTION = 0.85  # Friction when bouncing off walls
RESTITUTION = 0.75  # Bounciness coefficient
HEXAGON_RADIUS = 250
BALL_RADIUS = 15
HEXAGON_ROTATION_SPEED = 0.5  # radians per second

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
GRAY = (100, 100, 100)

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = radius
        self.mass = 1
        self.trail = []  # Store previous positions for trail effect
        self.max_trail_length = 20
        
    def update(self, dt):
        # Apply gravity
        self.vy += GRAVITY * dt
        
        # Apply air friction
        self.vx *= FRICTION_COEFFICIENT
        self.vy *= FRICTION_COEFFICIENT
        
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
    
    def draw(self, screen):
        # Draw trail
        for i, pos in enumerate(self.trail):
            alpha = i / len(self.trail) if self.trail else 1
            color = (255 * alpha, 50 * alpha, 50 * alpha)
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), 
                             int(self.radius * alpha * 0.5))
        
        # Draw ball with gradient effect
        for i in range(self.radius, 0, -1):
            color_intensity = 255 - (self.radius - i) * 10
            color = (min(255, color_intensity), 50, 50)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), i)
        
        # Draw highlight
        highlight_x = int(self.x - self.radius * 0.3)
        highlight_y = int(self.y - self.radius * 0.3)
        pygame.draw.circle(screen, (255, 150, 150), 
                         (highlight_x, highlight_y), self.radius // 3)

class Hexagon:
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.rotation = 0
        self.vertices = []
        self.update_vertices()
        
    def update_vertices(self):
        self.vertices = []
        for i in range(6):
            angle = self.rotation + (2 * math.pi * i / 6)
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            self.vertices.append((x, y))
    
    def rotate(self, dt):
        self.rotation += HEXAGON_ROTATION_SPEED * dt
        self.update_vertices()
    
    def get_edges(self):
        edges = []
        for i in range(6):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % 6]
            edges.append((p1, p2))
        return edges
    
    def draw(self, screen):
        # Draw filled hexagon with transparency
        pygame.draw.polygon(screen, GRAY, self.vertices, 3)
        
        # Draw vertices
        for vertex in self.vertices:
            pygame.draw.circle(screen, WHITE, (int(vertex[0]), int(vertex[1])), 5)
        
        # Draw center point
        pygame.draw.circle(screen, GREEN, (int(self.center_x), int(self.center_y)), 3)

def point_to_line_distance(px, py, x1, y1, x2, y2):
    """Calculate the shortest distance from a point to a line segment"""
    # Vector from p1 to p2
    dx = x2 - x1
    dy = y2 - y1
    
    # Vector from p1 to point
    dpx = px - x1
    dpy = py - y1
    
    # Calculate parameter t for closest point on line segment
    segment_length_sq = dx * dx + dy * dy
    if segment_length_sq == 0:
        return math.sqrt(dpx * dpx + dpy * dpy), x1, y1
    
    t = max(0, min(1, (dpx * dx + dpy * dy) / segment_length_sq))
    
    # Closest point on segment
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    
    # Distance to closest point
    distance = math.sqrt((px - closest_x) ** 2 + (py - closest_y) ** 2)
    
    return distance, closest_x, closest_y

def check_collision(ball, hexagon):
    """Check and handle collision between ball and hexagon edges"""
    edges = hexagon.get_edges()
    
    for edge in edges:
        p1, p2 = edge
        distance, closest_x, closest_y = point_to_line_distance(
            ball.x, ball.y, p1[0], p1[1], p2[0], p2[1]
        )
        
        if distance < ball.radius:
            # Calculate normal vector (pointing inward)
            edge_dx = p2[0] - p1[0]
            edge_dy = p2[1] - p1[1]
            edge_length = math.sqrt(edge_dx ** 2 + edge_dy ** 2)
            
            if edge_length > 0:
                # Normal vector (perpendicular to edge)
                normal_x = -edge_dy / edge_length
                normal_y = edge_dx / edge_length
                
                # Make sure normal points inward
                to_center_x = hexagon.center_x - ball.x
                to_center_y = hexagon.center_y - ball.y
                
                if normal_x * to_center_x + normal_y * to_center_y < 0:
                    normal_x = -normal_x
                    normal_y = -normal_y
                
                # Push ball out of wall
                overlap = ball.radius - distance
                ball.x += normal_x * overlap
                ball.y += normal_y * overlap
                
                # Calculate relative velocity (including wall rotation)
                # Wall velocity at collision point
                wall_vx = -HEXAGON_ROTATION_SPEED * (closest_y - hexagon.center_y)
                wall_vy = HEXAGON_ROTATION_SPEED * (closest_x - hexagon.center_x)
                
                rel_vx = ball.vx - wall_vx
                rel_vy = ball.vy - wall_vy
                
                # Velocity component along normal
                v_normal = rel_vx * normal_x + rel_vy * normal_y
                
                if v_normal < 0:  # Moving towards wall
                    # Calculate reflection
                    ball.vx -= (1 + RESTITUTION) * v_normal * normal_x
                    ball.vy -= (1 + RESTITUTION) * v_normal * normal_y
                    
                    # Apply wall friction to tangential component
                    tangent_x = edge_dx / edge_length
                    tangent_y = edge_dy / edge_length
                    v_tangent = rel_vx * tangent_x + rel_vy * tangent_y
                    
                    ball.vx -= v_tangent * (1 - WALL_FRICTION) * tangent_x
                    ball.vy -= v_tangent * (1 - WALL_FRICTION) * tangent_y
                    
                    # Add some of the wall's velocity (momentum transfer)
                    ball.vx += wall_vx * 0.1
                    ball.vy += wall_vy * 0.1

def draw_info(screen, ball, hexagon):
    """Draw information text on screen"""
    font = pygame.font.Font(None, 24)
    
    # Calculate speed
    speed = math.sqrt(ball.vx ** 2 + ball.vy ** 2)
    
    texts = [
        f"Speed: {speed:.1f} px/s",
        f"Position: ({int(ball.x)}, {int(ball.y)})",
        f"Hexagon Rotation: {math.degrees(hexagon.rotation) % 360:.1f}°",
        "Press SPACE to reset ball position",
        "Press R to randomize ball velocity"
    ]
    
    for i, text in enumerate(texts):
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (10, 10 + i * 25))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ball Bouncing in Spinning Hexagon")
    clock = pygame.time.Clock()
    
    # Create objects
    hexagon = Hexagon(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, HEXAGON_RADIUS)
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, BALL_RADIUS)
    
    # Give initial velocity
    ball.vx = 200
    ball.vy = -100
    
    running = True
    dt = 0
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Reset ball position
                    ball.x = SCREEN_WIDTH // 2
                    ball.y = SCREEN_HEIGHT // 2 - 100
                    ball.vx = 200
                    ball.vy = -100
                    ball.trail = []
                elif event.key == pygame.K_r:
                    # Randomize velocity
                    ball.vx = np.random.uniform(-300, 300)
                    ball.vy = np.random.uniform(-300, 300)
        
        # Update physics
        dt = clock.tick(FPS) / 1000.0  # Convert to seconds
        
        # Update hexagon rotation
        hexagon.rotate(dt)
        
        # Update ball physics
        ball.update(dt)
        
        # Check collisions
        check_collision(ball, hexagon)
        
        # Draw everything
        screen.fill(BLACK)
        
        # Draw grid for reference
        for i in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(screen, (20, 20, 20), (i, 0), (i, SCREEN_HEIGHT), 1)
        for i in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(screen, (20, 20, 20), (0, i), (SCREEN_WIDTH, i), 1)
        
        hexagon.draw(screen)
        ball.draw(screen)
        draw_info(screen, ball, hexagon)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()