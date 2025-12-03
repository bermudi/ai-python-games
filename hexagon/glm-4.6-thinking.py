import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (20, 20, 30)
BALL_COLOR = (255, 100, 100)
HEXAGON_COLOR = (100, 200, 255)
GRAVITY = 500  # pixels/s^2
AIR_FRICTION = 0.995  # velocity damping per frame
RESTITUTION = 0.75  # bounce damping (0 = no bounce, 1 = perfect bounce)
BALL_RADIUS = 15
HEXAGON_RADIUS = 200
ROTATION_SPEED = 0.5  # radians per second

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = BALL_RADIUS
        self.trail = []  # Store previous positions for trail effect
        self.max_trail_length = 20
        
    def update(self, dt):
        # Apply gravity
        self.vy += GRAVITY * dt
        
        # Apply air friction (velocity damping)
        self.vx *= AIR_FRICTION
        self.vy *= AIR_FRICTION
        
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
            color = (int(255 * alpha), int(100 * alpha), int(100 * alpha))
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), 
                             int(self.radius * alpha * 0.5))
        
        # Draw ball with gradient effect
        for i in range(3):
            color_intensity = 255 - i * 30
            pygame.draw.circle(screen, (color_intensity, 100, 100), 
                             (int(self.x), int(self.y)), 
                             self.radius - i * 2)
        
        # Draw highlight
        pygame.draw.circle(screen, (255, 200, 200), 
                         (int(self.x - self.radius/3), int(self.y - self.radius/3)), 
                         self.radius//3)

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
            angle = self.rotation + i * math.pi / 3
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            self.vertices.append((x, y))
    
    def update(self, dt):
        self.rotation += ROTATION_SPEED * dt
        self.update_vertices()
    
    def draw(self, screen):
        # Draw filled hexagon with transparency
        hex_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(hex_surface, (*HEXAGON_COLOR, 50), self.vertices)
        screen.blit(hex_surface, (0, 0))
        
        # Draw hexagon outline
        pygame.draw.polygon(screen, HEXAGON_COLOR, self.vertices, 3)
        
        # Draw vertices as small circles
        for vertex in self.vertices:
            pygame.draw.circle(screen, HEXAGON_COLOR, (int(vertex[0]), int(vertex[1])), 5)
    
    def get_edges(self):
        edges = []
        for i in range(6):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % 6]
            edges.append((p1, p2))
        return edges
    
    def get_wall_velocity_at_point(self, x, y):
        """Calculate the tangential velocity of the hexagon wall at a given point"""
        # Vector from center to point
        dx = x - self.center_x
        dy = y - self.center_y
        
        # Tangential velocity = angular_velocity × radius_vector
        # In 2D: vx = -ω * dy, vy = ω * dx
        vx = -ROTATION_SPEED * dy
        vy = ROTATION_SPEED * dx
        
        return vx, vy

def check_collision(ball, hexagon):
    """Check and handle collision between ball and hexagon walls"""
    edges = hexagon.get_edges()
    
    for edge in edges:
        p1, p2 = edge
        
        # Vector from p1 to p2
        edge_vec = np.array([p2[0] - p1[0], p2[1] - p1[1]])
        edge_length = np.linalg.norm(edge_vec)
        
        if edge_length == 0:
            continue
            
        edge_unit = edge_vec / edge_length
        
        # Vector from p1 to ball center
        to_ball = np.array([ball.x - p1[0], ball.y - p1[1]])
        
        # Project ball center onto edge
        projection_length = np.dot(to_ball, edge_unit)
        projection_length = max(0, min(edge_length, projection_length))
        
        # Closest point on edge to ball center
        closest_point = np.array(p1) + projection_length * edge_unit
        
        # Distance from ball center to closest point
        dist_vec = np.array([ball.x, ball.y]) - closest_point
        distance = np.linalg.norm(dist_vec)
        
        # Check if collision occurs
        if distance < ball.radius and distance > 0:
            # Calculate normal vector (pointing away from edge)
            normal = dist_vec / distance
            
            # Push ball out of wall to prevent sticking
            overlap = ball.radius - distance
            ball.x += normal[0] * overlap * 1.01  # Slight extra to ensure separation
            ball.y += normal[1] * overlap * 1.01
            
            # Get wall velocity at collision point
            wall_vx, wall_vy = hexagon.get_wall_velocity_at_point(closest_point[0], closest_point[1])
            
            # Relative velocity of ball with respect to wall
            rel_vx = ball.vx - wall_vx
            rel_vy = ball.vy - wall_vy
            
            # Decompose relative velocity into normal and tangential components
            vel_normal = rel_vx * normal[0] + rel_vy * normal[1]
            
            # Only process if ball is moving towards the wall
            if vel_normal < 0:
                # Calculate tangential component
                tangent = np.array([-normal[1], normal[0]])
                vel_tangent = rel_vx * tangent[0] + rel_vy * tangent[1]
                
                # Apply collision response with restitution
                new_vel_normal = -vel_normal * RESTITUTION
                
                # Add some friction to tangential component
                friction_coefficient = 0.1
                new_vel_tangent = vel_tangent * (1 - friction_coefficient)
                
                # Reconstruct velocity in world coordinates
                ball.vx = new_vel_normal * normal[0] + new_vel_tangent * tangent[0] + wall_vx
                ball.vy = new_vel_normal * normal[1] + new_vel_tangent * tangent[1] + wall_vy
                
                return True
    
    return False

def draw_info(screen, font, ball):
    """Draw information text on screen"""
    speed = math.sqrt(ball.vx**2 + ball.vy**2)
    texts = [
        "Ball Bouncing in Spinning Hexagon",
        f"Speed: {speed:.1f} px/s",
        f"Position: ({ball.x:.0f}, {ball.y:.0f})",
        "Press SPACE to reset | ESC to exit"
    ]
    
    for i, text in enumerate(texts):
        text_surface = font.render(text, True, (200, 200, 200))
        screen.blit(text_surface, (10, 10 + i * 25))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ball Bouncing in Spinning Hexagon - Physics Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    
    # Create objects
    hexagon = Hexagon(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, HEXAGON_RADIUS)
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    
    # Give ball initial random velocity
    ball.vx = 200
    ball.vy = -150
    
    running = True
    dt = 0
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Reset ball position and velocity
                    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
                    ball.vx = 200
                    ball.vy = -150
        
        # Update physics
        dt = clock.tick(FPS) / 1000.0  # Convert to seconds
        dt = min(dt, 0.02)  # Cap dt to prevent instability
        
        ball.update(dt)
        hexagon.update(dt)
        
        # Check collisions multiple times per frame for accuracy
        for _ in range(3):
            check_collision(ball, hexagon)
        
        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        
        # Draw grid for reference
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(screen, (30, 30, 40), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(screen, (30, 30, 40), (0, y), (SCREEN_WIDTH, y), 1)
        
        hexagon.draw(screen)
        ball.draw(screen)
        draw_info(screen, font, ball)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()