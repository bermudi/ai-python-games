import pygame
import math
from pygame.math import Vector2

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAVITY = Vector2(0, 0.2)  # Downward acceleration
RESTITUTION = 0.8  # Energy loss on collision
ROTATION_SPEED = 0.5  # Degrees per frame

# --- Helper Functions ---

def rotate_point(point, angle, center=(0, 0)):
    """Rotates a point around a center point."""
    angle_rad = math.radians(angle)
    x, y = point
    cx, cy = center
    rotated_x = (x - cx) * math.cos(angle_rad) - (y - cy) * math.sin(angle_rad) + cx
    rotated_y = (x - cx) * math.sin(angle_rad) + (y - cy) * math.cos(angle_rad) + cy
    return Vector2(rotated_x, rotated_y)

def point_to_line_distance(point, line_start, line_end):
    """Calculates the distance from a point to a line segment."""
    line_vec = line_end - line_start
    point_vec = point - line_start
    line_len_squared = line_vec.length_squared()

    if line_len_squared == 0:  # Line segment is a point
        return point_vec.length()

    t = max(0, min(1, point_vec.dot(line_vec) / line_len_squared))
    closest_point = line_start + t * line_vec
    return (point - closest_point).length()

def reflect_vector(vector, normal):
    """Reflects a vector across a normal."""
    return vector - 2 * vector.dot(normal) * normal

# --- Hexagon Class ---
class Hexagon:
    def __init__(self, radius, center):
        self.radius = radius
        self.center = Vector2(center)
        self.angle = 0
        self.vertices = self.calculate_vertices()

    def calculate_vertices(self):
        """Calculates the initial vertices of the hexagon."""
        vertices = []
        for i in range(6):
            angle_rad = math.radians(60 * i)
            x = self.center.x + self.radius * math.cos(angle_rad)
            y = self.center.y + self.radius * math.sin(angle_rad)
            vertices.append(Vector2(x, y))
        return vertices

    def rotate(self, angle):
        """Rotates the hexagon by a given angle."""
        self.angle += angle
        for i in range(len(self.vertices)):
            self.vertices[i] = rotate_point(self.vertices[i], angle, self.center)

    def draw(self, screen):
        """Draws the hexagon on the screen."""
        pygame.draw.polygon(screen, WHITE, self.vertices, 2)

# --- Ball Class ---
class Ball:
    def __init__(self, position, radius, velocity=Vector2(0, 0)):
        self.position = Vector2(position)
        self.radius = radius
        self.velocity = Vector2(velocity)

    def update(self, hexagon):
        """Updates the ball's position and velocity."""
        self.velocity += GRAVITY
        self.position += self.velocity

        # Collision detection and response with hexagon edges
        for i in range(6):
            v1 = hexagon.vertices[i]
            v2 = hexagon.vertices[(i + 1) % 6]  # Wrap around to the first vertex
            distance = point_to_line_distance(self.position, v1, v2)

            if distance < self.radius:
                # Calculate normal vector of the edge
                normal = (v2 - v1).normalize().rotate(90)
                # Ensure normal points outward
                if (self.position - hexagon.center).dot(normal) < 0:
                  normal = -normal

                # Reflect velocity
                self.velocity = reflect_vector(self.velocity, normal) * RESTITUTION
                
                # Move ball out of collision
                overlap = self.radius - distance
                self.position += normal * overlap

    def draw(self, screen):
        """Draws the ball on the screen."""
        pygame.draw.circle(screen, RED, (int(self.position.x), int(self.position.y)), self.radius)

# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")
clock = pygame.time.Clock()

# Create hexagon and ball
hexagon = Hexagon(150, (WIDTH // 2, HEIGHT // 2))
ball = Ball((WIDTH // 2, HEIGHT // 2 - 50), 15, Vector2(3,-3))

# --- Main Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game elements
    ball.update(hexagon)
    hexagon.rotate(ROTATION_SPEED)

    # Draw everything
    screen.fill(BLACK)
    hexagon.draw(screen)
    ball.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()