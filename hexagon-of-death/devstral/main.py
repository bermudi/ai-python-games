import pygame
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, MOVE_SPEED, ROT_SPEED, MAP_WIDTH, MAP_HEIGHT
from math_utils import Vec2
from models import Player, WorldMap
from engine import Raycaster
from view import PygameRenderer

def create_test_map():
    """Create a simple test map with borders and some internal walls"""
    # Create empty map
    map_data = [[0 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    
    # Add borders
    for i in range(MAP_WIDTH):
        map_data[0][i] = 1  # Top border
        map_data[MAP_HEIGHT-1][i] = 1  # Bottom border
    
    for i in range(MAP_HEIGHT):
        map_data[i][0] = 1  # Left border
        map_data[i][MAP_WIDTH-1] = 1  # Right border
    
    # Add some internal walls
    for i in range(5, 10):
        map_data[5][i] = 2
        map_data[10][i] = 3
    
    for i in range(8, 15):
        map_data[i][8] = 4
    
    # Add a central block
    for i in range(15, 20):
        for j in range(15, 20):
            if i == 15 or i == 19 or j == 15 or j == 19:
                map_data[i][j] = 5
    
    return WorldMap(map_data)

def main():
    # Initialize components
    renderer = PygameRenderer()
    raycaster = Raycaster()
    world_map = create_test_map()
    
    # Create player starting in the middle, facing right
    player = Player(
        pos=Vec2(12.0, 12.0),
        dir=Vec2(1.0, 0.0),
        plane=Vec2(0.0, 0.66)  # FOV = 0.66
    )
    
    # Main game loop
    running = True
    while running:
        # Handle events
        running = renderer.handle_events()
        
        # Handle input
        keys = pygame.key.get_pressed()
        
        # Rotation
        if keys[pygame.K_LEFT]:
            player.rotate(math.radians(-ROT_SPEED))
        if keys[pygame.K_RIGHT]:
            player.rotate(math.radians(ROT_SPEED))
        
        # Movement
        move_speed = MOVE_SPEED / FPS  # Frame-rate independent movement
        if keys[pygame.K_w]:
            # Move forward
            new_pos = player.pos + player.dir * move_speed
            if world_map.get_cell(int(new_pos.x), int(new_pos.y)) == 0:
                player.pos = new_pos
        if keys[pygame.K_s]:
            # Move backward
            new_pos = player.pos - player.dir * move_speed
            if world_map.get_cell(int(new_pos.x), int(new_pos.y)) == 0:
                player.pos = new_pos
        if keys[pygame.K_a]:
            # Strafe left
            strafe_dir = Vec2(-player.dir.y, player.dir.x)  # Perpendicular to direction
            new_pos = player.pos + strafe_dir * move_speed
            if world_map.get_cell(int(new_pos.x), int(new_pos.y)) == 0:
                player.pos = new_pos
        if keys[pygame.K_d]:
            # Strafe right
            strafe_dir = Vec2(player.dir.y, -player.dir.x)  # Perpendicular to direction
            new_pos = player.pos + strafe_dir * move_speed
            if world_map.get_cell(int(new_pos.x), int(new_pos.y)) == 0:
                player.pos = new_pos
        
        # Cast rays and render
        scanlines = raycaster.cast_rays(player, world_map)
        renderer.render_frame(scanlines)
        renderer.update_display()
    
    pygame.quit()

if __name__ == "__main__":
    main()