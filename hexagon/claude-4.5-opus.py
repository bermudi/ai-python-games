import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bouncing in Spinning Hexagon")
clock = pygame.time.Clock()

# Colors
BLACK = (10, 10, 25)
WHITE = (255, 255, 255)
RED = (255, 75, 75)
BLUE = (80, 140, 255)
CYAN = (100, 255, 255)

# Hexagon settings
CENTER = [WIDTH // 2, HEIGHT // 2]
HEX_RADIUS = 270
hex_angle = 0.0
hex_angular_velocity = 1.5  # radians per second

# Ball settings
ball_pos = [float(WIDTH // 2), float(HEIGHT // 2)]
ball_vel = [250.0, -150.0]
BALL_RADIUS = 16
GRAVITY = 980.0
RESTITUTION = 0.78  # bounciness (energy loss on bounce)
FRICTION = 0.992    # tangential friction

# Trail effect
trail = []
MAX_TRAIL = 40


def get_hexagon_vertices(center, radius, angle):
    """Get the vertices of a hexagon rotated by angle."""
    vertices = []
    for i in range(6):
        vertex_angle = angle + i * math.pi / 3
        x = center[0] + radius * math.cos(vertex_angle)
        y = center[1] + radius * math.sin(vertex_angle)
        vertices.append([x, y])
    return vertices


def point_to_segment_distance(point, seg_start, seg_end):
    """Calculate shortest distance from point to line segment and closest point."""
    px, py = point
    x1, y1 = seg_start
    x2, y2 = seg_end
    
    dx, dy = x2 - x1, y2 - y1
    length_sq = dx * dx + dy * dy
    
    if length_sq == 0:
        dist = math.hypot(px - x1, py - y1)
        return dist, [x1, y1]
    
    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / length_sq))
    closest = [x1 + t * dx, y1 + t * dy]
    dist = math.hypot(px - closest[0], py - closest[1])
    
    return dist, closest


def get_inward_normal(seg_start, seg_end, center):
    """Get the inward-pointing unit normal of an edge."""
    dx = seg_end[0] - seg_start[0]
    dy = seg_end[1] - seg_start[1]
    length = math.hypot(dx, dy)
    
    if length == 0:
        return [0, 0]
    
    # Two perpendicular unit vectors
    n1 = [-dy / length, dx / length]
    n2 = [dy / length, -dx / length]
    
    # Edge midpoint
    mid = [(seg_start[0] + seg_end[0]) / 2, (seg_start[1] + seg_end[1]) / 2]
    
    # Choose the one pointing toward center
    to_center = [center[0] - mid[0], center[1] - mid[1]]
    
    if n1[0] * to_center[0] + n1[1] * to_center[1] > 0:
        return n1
    return n2


def get_wall_velocity(point, center, omega):
    """Velocity of a point on the rotating hexagon: v = ω × r"""
    rx = point[0] - center[0]
    ry = point[1] - center[1]
    return [-omega * ry, omega * rx]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def handle_collision(ball_pos, ball_vel, vertices, omega):
    """Detect and resolve collisions with hexagon walls."""
    for i in range(6):
        seg_start = vertices[i]
        seg_end = vertices[(i + 1) % 6]
        
        dist, closest = point_to_segment_distance(ball_pos, seg_start, seg_end)
        
        if dist < BALL_RADIUS:
            # Get inward normal
            normal = get_inward_normal(seg_start, seg_end, CENTER)
            
            # Wall velocity at contact point (due to rotation)
            wall_vel = get_wall_velocity(closest, CENTER, omega)
            
            # Ball velocity relative to wall
            rel_vel = [ball_vel[0] - wall_vel[0], ball_vel[1] - wall_vel[1]]
            
            # Component of relative velocity toward wall
            vel_normal = dot(rel_vel, normal)
            
            # Only bounce if moving toward the wall
            if vel_normal < 0:
                # Tangent vector
                tangent = [-normal[1], normal[0]]
                vel_tangent = dot(rel_vel, tangent)
                
                # Reflect normal component (with restitution loss)
                new_vel_normal = -vel_normal * RESTITUTION
                
                # Apply friction to tangent component
                new_vel_tangent = vel_tangent * FRICTION
                
                # Reconstruct relative velocity
                new_rel_vel = [
                    new_vel_normal * normal[0] + new_vel_tangent * tangent[0],
                    new_vel_normal * normal[1] + new_vel_tangent * tangent[1]
                ]
                
                # Convert back to world velocity
                ball_vel[0] = new_rel_vel[0] + wall_vel[0]
                ball_vel[1] = new_rel_vel[1] + wall_vel[1]
                
                # Push ball out of wall
                penetration = BALL_RADIUS - dist + 1.0
                ball_pos[0] += normal[0] * penetration
                ball_pos[1] += normal[1] * penetration
    
    return ball_pos, ball_vel


def draw_hexagon(surface, vertices, color, width):
    """Draw hexagon with glow effect."""
    # Glow layers
    for w in range(width + 6, width, -2):
        alpha = 50 - (w - width) * 8
        glow_color = (color[0] // 4, color[1] // 4, color[2] // 4)
        int_verts = [(int(v[0]), int(v[1])) for v in vertices]
        pygame.draw.polygon(surface, glow_color, int_verts, w)
    
    # Main hexagon
    int_verts = [(int(v[0]), int(v[1])) for v in vertices]
    pygame.draw.polygon(surface, color, int_verts, width)
    
    # Vertices
    for v in int_verts:
        pygame.draw.circle(surface, CYAN, v, 7)
        pygame.draw.circle(surface, WHITE, v, 4)


def draw_ball(surface, pos, radius):
    """Draw ball with 3D shading effect."""
    x, y = int(pos[0]), int(pos[1])
    
    # Shadow
    pygame.draw.circle(surface, (30, 15, 15), (x + 5, y + 5), radius)
    
    # Main ball
    pygame.draw.circle(surface, RED, (x, y), radius)
    
    # Highlight
    pygame.draw.circle(surface, (255, 200, 200), (x - 5, y - 5), radius // 3)


def draw_trail(surface, trail):
    """Draw motion trail."""
    for i, (tx, ty) in enumerate(trail):
        progress = i / len(trail)
        alpha = int(180 * progress)
        r = max(2, int(BALL_RADIUS * progress * 0.6))
        color = (min(255, 80 + alpha), 30, 30)
        pygame.draw.circle(surface, color, (int(tx), int(ty)), r)


def main():
    global hex_angle, hex_angular_velocity, ball_pos, ball_vel, trail
    
    running = True
    font = pygame.font.Font(None, 26)
    
    while running:
        dt = clock.tick(60) / 1000.0
        dt = min(dt, 0.033)  # Cap delta time
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Reset ball
                    ball_pos = [float(WIDTH // 2), float(HEIGHT // 2)]
                    ball_vel = [250.0, -150.0]
                    trail.clear()
                elif event.key == pygame.K_r:
                    # Reverse rotation
                    hex_angular_velocity *= -1
        
        # Adjust rotation speed with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            hex_angular_velocity += 2.0 * dt
        if keys[pygame.K_LEFT]:
            hex_angular_velocity -= 2.0 * dt
        hex_angular_velocity = max(-6.0, min(6.0, hex_angular_velocity))
        
        # Update hexagon rotation
        hex_angle += hex_angular_velocity * dt
        
        # Physics substeps for stability
        substeps = 4
        sub_dt = dt / substeps
        
        for _ in range(substeps):
            # Apply gravity
            ball_vel[1] += GRAVITY * sub_dt
            
            # Update position
            ball_pos[0] += ball_vel[0] * sub_dt
            ball_pos[1] += ball_vel[1] * sub_dt
            
            # Get hexagon and handle collisions
            vertices = get_hexagon_vertices(CENTER, HEX_RADIUS, hex_angle)
            ball_pos, ball_vel = handle_collision(
                ball_pos, ball_vel, vertices, hex_angular_velocity
            )
        
        # Update trail
        trail.append((ball_pos[0], ball_pos[1]))
        if len(trail) > MAX_TRAIL:
            trail.pop(0)
        
        # ===== RENDERING =====
        screen.fill(BLACK)
        
        # Draw trail
        if trail:
            draw_trail(screen, trail)
        
        # Draw hexagon
        vertices = get_hexagon_vertices(CENTER, HEX_RADIUS, hex_angle)
        draw_hexagon(screen, vertices, BLUE, 4)
        
        # Draw ball
        draw_ball(screen, ball_pos, BALL_RADIUS)
        
        # Draw UI
        speed = math.hypot(ball_vel[0], ball_vel[1])
        info_lines = [
            f"Rotation: {hex_angular_velocity:+.2f} rad/s",
            f"Ball Speed: {speed:.0f} px/s",
            "",
            "LEFT/RIGHT: Adjust rotation",
            "R: Reverse rotation",
            "SPACE: Reset ball"
        ]
        
        for i, line in enumerate(info_lines):
            color = CYAN if i < 2 else (150, 150, 150)
            text = font.render(line, True, color)
            screen.blit(text, (12, 12 + i * 22))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()