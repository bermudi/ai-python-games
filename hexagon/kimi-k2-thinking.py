import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
FPS = 60
BACKGROUND_COLOR = (10, 10, 20)

# Hexagon properties
HEXAGON_RADIUS = 300
HEXAGON_CENTER = (WIDTH // 2, HEIGHT // 2)
ROTATION_SPEED = 0.01  # radians per frame

# Ball properties
BALL_RADIUS = 15
BALL_COLOR = (255, 50, 50)
GRAVITY = 0.3
FRICTION = 0.99
BOUNCE_DAMPING = 0.8

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2 - 100
        self.vx = 3
        self.vy = 0
        self.radius = BALL_RADIUS
        self.trail = []
        self.max_trail_length = 50
    
    def update(self):
        # Apply gravity
        self.vy += GRAVITY
        
        # Apply friction
        self.vx *= FRICTION
        self.vy *= FRICTION
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
    
    def bounce(self, normal_x, normal_y):
        # Calculate dot product
        dot_product = self.vx * normal_x + self.vy * normal_y
        
        # Reflect velocity
        self.vx -= 2 * dot_product * normal_x
        self.vy -= 2 * dot_product * normal_y
        
        # Apply bounce damping
        self.vx *= BOUNCE_DAMPING
        self.vy *= BOUNCE_DAMPING
    
    def draw(self, screen):
        # Draw trail
        if len(self.trail) > 1:
            for i in range(len(self.trail) - 1):
                alpha = int(255 * (i / len(self.trail)))
                color = (255, 50, 50, alpha)
                pygame.draw.line(screen, color, self.trail[i], self.trail[i+1], 2)
        
        # Draw ball
        pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), self.radius)

class Hexagon:
    def __init__(self):
        self.rotation = 0
        self.vertices = []
        self.edges = []
    
    def update(self):
        self.rotation += ROTATION_SPEED
        self.calculate_vertices()
        self.calculate_edges()
    
    def calculate_vertices(self):
        self.vertices = []
        for i in range(6):
            angle = self.rotation + i * math.pi / 3
            x = HEXAGON_CENTER[0] + HEXAGON_RADIUS * math.cos(angle)
            y = HEXAGON_CENTER[1] + HEXAGON_RADIUS * math.sin(angle)
            self.vertices.append((x, y))
    
    def calculate_edges(self):
        self.edges = []
        for i in range(6):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % 6]
            self.edges.append(((x1, y1), (x2, y2)))
    
    def check_collision(self, ball):
        for i, edge in enumerate(self.edges):
            x1, y1 = edge[0]
            x2, y2 = edge[1]
            
            # Find the closest point on the edge to the ball
            edge_dx = x2 - x1
            edge_dy = y2 - y1
            edge_length = math.sqrt(edge_dx**2 + edge_dy**2)
            
            # Normalize edge vector
            if edge_length > 0:
                edge_dx /= edge_length
                edge_dy /= edge_length
            
            # Vector from edge start to ball
            ball_dx = ball.x - x1
            ball_dy = ball.y - y1
            
            # Project ball onto edge
            projection = ball_dx * edge_dx + ball_dy * edge_dy
            
            # Clamp projection to edge segment
            projection = max(0, min(edge_length, projection))
            
            # Find closest point on edge
            closest_x = x1 + projection * edge_dx
            closest_y = y1 + projection * edge_dy
            
            # Check distance to ball
            distance = math.sqrt((ball.x - closest_x)**2 + (ball.y - closest_y)**2)
            
            if distance < ball.radius:
                # Calculate normal vector (perpendicular to edge)
                normal_x = -edge_dy
                normal_y = edge_dx
                
                # Ensure normal points outward
                center_dx = ball.x - HEXAGON_CENTER[0]
                center_dy = ball.y - HEXAGON_CENTER[1]
                if normal_x * center_dx + normal_y * center_dy > 0:
                    normal_x = -normal_x
                    normal_y = -normal_y
                
                # Move ball outside the wall
                overlap = ball.radius - distance
                ball.x += normal_x * overlap
                ball.y += normal_y * overlap
                
                # Bounce
                ball.bounce(normal_x, normal_y)
                
                return True
        
        return False
    
    def draw(self, screen):
        # Draw hexagon
        pygame.draw.polygon(screen, (100, 100, 150), self.vertices, 3)
        
        # Draw vertices
        for vertex in self.vertices:
            pygame.draw.circle(screen, (150, 150, 200), (int(vertex[0]), int(vertex[1])), 5)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ball in Spinning Hexagon")
    clock = pygame.time.Clock()
    
    ball = Ball()
    hexagon = Hexagon()
    
    font = pygame.font.Font(None, 36)
    
    # Add initial velocity
    ball.vx = 5
    ball.vy = 2
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Reset ball position
                    ball.x = WIDTH // 2
                    ball.y = HEIGHT // 2 - 100
                    ball.vx = 5
                    ball.vy = 2
                    ball.trail = []
        
        # Update
        ball.update()
        hexagon.update()
        hexagon.check_collision(ball)
        
        # Draw
        screen.fill(BACKGROUND_COLOR)
        
        # Draw center point
        pygame.draw.circle(screen, (200, 200, 200), HEXAGON_CENTER, 3)
        
        hexagon.draw(screen)
        ball.draw(screen)
        
        # Draw UI text
        text = font.render("Press SPACE to reset", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        speed_text = font.render(f"Speed: {math.sqrt(ball.vx**2 + ball.vy**2):.2f}", True, (255, 255, 255))
        screen.blit(speed_text, (10, 50))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()