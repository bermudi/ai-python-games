from math_utils import Vec2
from models import Player, WorldMap
from config import SCREEN_WIDTH, SCREEN_HEIGHT
import math

class Raycaster:
    def cast_rays(self, player: Player, world_map: WorldMap) -> list[dict]:
        results = []
        
        for x in range(SCREEN_WIDTH):
            # 1. Calculate Ray Direction
            camera_x = 2 * x / SCREEN_WIDTH - 1  # x-coordinate in camera space
            ray_dir = player.dir + (player.plane * camera_x)

            # 2. Setup DDA
            map_x = int(player.pos.x)
            map_y = int(player.pos.y)

            # Calculate delta_dist (distance between grid lines)
            # Avoid division by zero
            delta_dist_x = abs(1 / ray_dir.x) if ray_dir.x != 0 else 1e30
            delta_dist_y = abs(1 / ray_dir.y) if ray_dir.y != 0 else 1e30

            # Calculate step direction and initial side_dist
            step_x = 1 if ray_dir.x >= 0 else -1
            step_y = 1 if ray_dir.y >= 0 else -1

            # Calculate initial side distance
            if ray_dir.x < 0:
                side_dist_x = (player.pos.x - map_x) * delta_dist_x
            else:
                side_dist_x = (map_x + 1.0 - player.pos.x) * delta_dist_x

            if ray_dir.y < 0:
                side_dist_y = (player.pos.y - map_y) * delta_dist_y
            else:
                side_dist_y = (map_y + 1.0 - player.pos.y) * delta_dist_y

            # 3. Perform DDA Step
            hit = 0
            side = 0  # 0 for NS, 1 for EW
            
            while hit == 0:
                # Jump to next map square, either in x or y direction
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    side = 0
                else:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    side = 1

                # Check if ray has hit a wall
                if world_map.get_cell(map_x, map_y) > 0:
                    hit = 1

            # 4. Calculate Fisheye-corrected distance
            if side == 0:
                perp_wall_dist = (side_dist_x - delta_dist_x)
            else:
                perp_wall_dist = (side_dist_y - delta_dist_y)

            results.append({
                "x": x,
                "dist": perp_wall_dist,
                "side": side,
                "color_id": world_map.get_cell(map_x, map_y)
            })
        
        return results