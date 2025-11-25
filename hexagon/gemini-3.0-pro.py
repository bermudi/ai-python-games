import pygame
import math

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
CYAN = (50, 255, 255)
RED = (255, 50, 50)

# Physics Constants
GRAVITY = 0.15
FRICTION = 0.999      # Air resistance (1.0 = no resistance)
WALL_FRICTION = 0.8   # Energy lost when hitting a wall (bounciness)
ROTATION_SPEED = 1.0  # Degrees per frame
HEXAGON_RADIUS = 250
BALL_RADIUS = 15

class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 18)

        # Hexagon properties
        self.center = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)
        self.hex_angle = 0
        self.hex_radius = HEXAGON_RADIUS

        # Ball properties
        self.ball_pos = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2 - 100)
        self.ball_vel = pygame.math.Vector2(3, 0) # Initial slight push
    
    def get_hexagon_vertices(self):
        """Calculates the 6 points of the hexagon based on current rotation."""
        vertices = []
        for i in range(6):
            # 60 degrees = pi/3 radians
            angle_rad = math.radians(self.hex_angle + i * 60)
            x = self.center.x + self.hex_radius * math.cos(angle_rad)
            y = self.center.y + self.hex_radius * math.sin(angle_rad)
            vertices.append(pygame.math.Vector2(x, y))
        return vertices

    def closest_point_on_segment(self, point, start, end):
        """Finds the closest point on a line segment to a specific point."""
        line_vec = end - start
        point_vec = point - start
        line_len_sq = line_vec.length_squared()
        
        if line_len_sq == 0: 
            return start

        # Project point onto line (dot product) normalized by length
        t = point_vec.dot(line_vec) / line_len_sq
        
        # Clamp t to segment [0, 1]
        t = max(0, min(1, t))
        
        return start + line_vec * t

    def resolve_collisions(self, vertices):
        """
        Checks collision between ball and all 6 walls.
        Handles position correction and velocity reflection.
        """
        for i in range(6):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % 6] # Wrap around to 0 for the last segment

            # Find closest point on this wall to the ball
            closest = self.closest_point_on_segment(self.ball_pos, p1, p2)
            dist_vec = self.ball_pos - closest
            distance = dist_vec.length()

            # Check collision
            if distance < BALL_RADIUS:
                # 1. Calculate Normal Vector of the wall
                # We need the normal pointing inward. 
                # Simple way: Vector from closest point on wall towards ball center
                if distance == 0:
                    normal = pygame.math.Vector2(0, -1) # Fallback
                else:
                    normal = dist_vec.normalize()

                # 2. Position Correction (push ball out of wall to prevent sinking)
                overlap = BALL_RADIUS - distance
                self.ball_pos += normal * overlap

                # 3. Calculate Wall Velocity at impact point
                # The wall is rotating. V = r * omega (angular velocity)
                # Tangent is perpendicular to the radius vector from center
                r_vec = closest - self.center
                # Perpendicular vector for rotation (clockwise vs counter-clockwise matters)
                # For clockwise rotation logic:
                tangent_vel_dir = pygame.math.Vector2(-r_vec.y, r_vec.x).normalize()
                
                # Convert degrees/frame to radians/frame approx for magnitude
                ang_vel_rad = math.radians(ROTATION_SPEED)
                wall_vel_mag = r_vec.length() * ang_vel_rad
                wall_velocity = tangent_vel_dir * wall_vel_mag

                # 4. Relative Velocity Reflection
                # We reflect the ball's velocity relative to the moving wall
                v_rel = self.ball_vel - wall_velocity
                v_rel_dot_n = v_rel.dot(normal)

                # Only bounce if moving towards the wall
                if v_rel_dot_n < 0:
                    # Reflection formula: V_new = V_old - (1 + elasticity) * (V_old . N) * N
                    v_rel_new = v_rel - (1 + WALL_FRICTION) * v_rel_dot_n * normal
                    self.ball_vel = v_rel_new + wall_velocity

    def update(self):
        # 1. Update Hexagon Rotation
        self.hex_angle += ROTATION_SPEED
        if self.hex_angle >= 360:
            self.hex_angle -= 360

        # 2. Apply Gravity
        self.ball_vel.y += GRAVITY

        # 3. Apply Air Friction
        self.ball_vel *= FRICTION

        # 4. Move Ball
        self.ball_pos += self.ball_vel

        # 5. Handle Collisions
        vertices = self.get_hexagon_vertices()
        
        # We run collision check multiple times (sub-stepping) for stability 
        # when the hexagon spins fast or the ball moves fast.
        self.resolve_collisions(vertices)
        
        # Safety check: If ball escapes (glitch), reset it
        if (self.ball_pos - self.center).length() > self.hex_radius + BALL_RADIUS * 2:
            self.ball_pos = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)
            self.ball_vel = pygame.math.Vector2(0, 0)

        return vertices

    def draw(self, vertices):
        self.screen.fill(BLACK)

        # Draw Hexagon
        # Draw polygon fills the shape, lines draw the border
        pygame.draw.polygon(self.screen, (30, 30, 30), vertices) 
        pygame.draw.lines(self.screen, CYAN, True, vertices, 5)

        # Draw Ball
        pygame.draw.circle(self.screen, RED, (int(self.ball_pos.x), int(self.ball_pos.y)), BALL_RADIUS)

        # Draw UI
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, WHITE)
        info_text = self.font.render("Gravity + Friction + Angular Momentum", True, (150, 150, 150))
        self.screen.blit(fps_text, (10, 10))
        self.screen.blit(info_text, (10, 35))

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    # Reset on spacebar
                    if event.key == pygame.K_SPACE:
                        self.ball_pos = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2 - 50)
                        self.ball_vel = pygame.math.Vector2(2, 0)

            vertices = self.update()
            self.draw(vertices)
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    sim = Simulation()
    sim.run()