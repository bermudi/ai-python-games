import pygame
import math
import sys

"""
Penguin Alpha was an experimental model that appeared in Cascade at the end of November 2025.
"""

class Ball:
    def __init__(self, x, y, radius, mass=1.0):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = radius
        self.mass = mass
        self.restitution = 0.8  # Bounciness coefficient
        
class Hexagon:
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.rotation = 0
        self.angular_velocity = 0.5  # Radians per second
        self.vertices = []
        self.update_vertices()
        
    def update_vertices(self):
        self.vertices = []
        for i in range(6):
            angle = self.rotation + (i * math.pi / 3)
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            self.vertices.append((x, y))
            
    def rotate(self, dt):
        self.rotation += self.angular_velocity * dt
        self.update_vertices()
        
    def get_edges(self):
        edges = []
        for i in range(6):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % 6]
            edges.append((p1, p2))
        return edges

class PhysicsSimulation:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Ball in Spinning Hexagon")
        self.clock = pygame.time.Clock()
        
        # Physics constants
        self.gravity = 500  # Pixels per second squared
        self.air_friction = 0.99  # Velocity damping
        self.rolling_friction = 0.98  # Additional friction when rolling
        
        # Create hexagon and ball
        self.hexagon = Hexagon(width // 2, height // 2, min(width, height) * 0.35)
        self.ball = Ball(width // 2, height // 2 - 50, 15)
        
        # Give ball initial velocity
        self.ball.vx = 150
        self.ball.vy = -100
        
        self.running = True
        self.dt = 0
        
    def point_to_line_distance(self, px, py, x1, y1, x2, y2):
        """Calculate distance from point to line segment"""
        line_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        if line_length == 0:
            return math.sqrt((px - x1)**2 + (py - y1)**2)
        
        t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / line_length**2))
        projection_x = x1 + t * (x2 - x1)
        projection_y = y1 + t * (y2 - y1)
        
        return math.sqrt((px - projection_x)**2 + (py - projection_y)**2)
    
    def get_line_normal(self, x1, y1, x2, y2):
        """Get normal vector to line segment"""
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx**2 + dy**2)
        if length == 0:
            return 0, 1
        # Perpendicular vector pointing inward
        return -dy / length, dx / length
    
    def check_collision(self):
        """Check and handle collision between ball and hexagon edges"""
        edges = self.hexagon.get_edges()
        
        for edge in edges:
            p1, p2 = edge
            x1, y1 = p1
            x2, y2 = p2
            
            # Calculate distance from ball center to edge
            distance = self.point_to_line_distance(self.ball.x, self.ball.y, x1, y1, x2, y2)
            
            if distance < self.ball.radius:
                # Collision detected
                # Get normal vector
                nx, ny = self.get_line_normal(x1, y1, x2, y2)
                
                # Check if normal points toward ball (inward)
                to_ball_x = self.ball.x - (x1 + x2) / 2
                to_ball_y = self.ball.y - (y1 + y2) / 2
                if nx * to_ball_x + ny * to_ball_y < 0:
                    nx, ny = -nx, -ny
                
                # Push ball out of wall
                overlap = self.ball.radius - distance
                self.ball.x += nx * overlap
                self.ball.y += ny * overlap
                
                # Calculate relative velocity (including wall rotation)
                # Wall tangent velocity at collision point
                collision_x = self.ball.x - nx * self.ball.radius
                collision_y = self.ball.y - ny * self.ball.radius
                
                # Distance from hexagon center to collision point
                dist_from_center = math.sqrt((collision_x - self.hexagon.center_x)**2 + 
                                           (collision_y - self.hexagon.center_y)**2)
                
                # Tangential velocity of wall at collision point
                if dist_from_center > 0:
                    wall_vx = -self.hexagon.angular_velocity * (collision_y - self.hexagon.center_y)
                    wall_vy = self.hexagon.angular_velocity * (collision_x - self.hexagon.center_x)
                else:
                    wall_vx = wall_vy = 0
                
                # Relative velocity
                rel_vx = self.ball.vx - wall_vx
                rel_vy = self.ball.vy - wall_vy
                
                # Velocity component along normal
                v_normal = rel_vx * nx + rel_vy * ny
                
                if v_normal < 0:  # Moving toward wall
                    # Apply impulse
                    impulse = -(1 + self.ball.restitution) * v_normal
                    self.ball.vx += impulse * nx
                    self.ball.vy += impulse * ny
                    
                    # Add some of wall's tangential velocity (friction effect)
                    friction_coefficient = 0.1
                    self.ball.vx += wall_vx * friction_coefficient
                    self.ball.vy += wall_vy * friction_coefficient
    
    def update_physics(self, dt):
        """Update ball physics"""
        # Apply gravity
        self.ball.vy += self.gravity * dt
        
        # Apply air friction
        self.ball.vx *= self.air_friction
        self.ball.vy *= self.air_friction
        
        # Update position
        self.ball.x += self.ball.vx * dt
        self.ball.y += self.ball.vy * dt
        
        # Update hexagon rotation
        self.hexagon.rotate(dt)
        
        # Check collisions
        self.check_collision()
    
    def draw(self):
        """Draw the simulation"""
        self.screen.fill((20, 20, 30))  # Dark background
        
        # Draw hexagon
        pygame.draw.polygon(self.screen, (100, 200, 100), self.hexagon.vertices, 3)
        
        # Draw ball
        pygame.draw.circle(self.screen, (255, 100, 100), 
                         (int(self.ball.x), int(self.ball.y)), self.ball.radius)
        
        # Draw center point for reference
        pygame.draw.circle(self.screen, (255, 255, 255), 
                         (int(self.hexagon.center_x), int(self.hexagon.center_y)), 2)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.dt = self.clock.tick(60) / 1000.0  # Convert to seconds
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        # Reset ball with random velocity
                        self.ball.x = self.hexagon.center_x
                        self.ball.y = self.hexagon.center_y - 50
                        self.ball.vx = (pygame.time.get_ticks() % 400) - 200
                        self.ball.vy = (pygame.time.get_ticks() % 200) - 100
            
            self.update_physics(self.dt)
            self.draw()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    sim = PhysicsSimulation()
    sim.run()
