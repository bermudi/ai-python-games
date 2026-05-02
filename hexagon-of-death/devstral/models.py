from dataclasses import dataclass
import math
from math_utils import Vec2

@dataclass
class Player:
    pos: Vec2       # Exact position
    dir: Vec2       # Direction vector (normalized)
    plane: Vec2     # Camera plane (perpendicular to dir)

    def rotate(self, rot_speed: float):
        """
        Apply rotation matrix to BOTH self.dir and self.plane
        to ensure FOV remains constant.
        
        [ x ]   [ cos -sin ] [ x ]
        [ y ] = [ sin  cos ] [ y ]
        """
        # Rotate direction vector
        cos_angle = math.cos(rot_speed)
        sin_angle = math.sin(rot_speed)
        
        new_dir_x = self.dir.x * cos_angle - self.dir.y * sin_angle
        new_dir_y = self.dir.x * sin_angle + self.dir.y * cos_angle
        self.dir = Vec2(new_dir_x, new_dir_y)
        
        # Rotate camera plane vector
        new_plane_x = self.plane.x * cos_angle - self.plane.y * sin_angle
        new_plane_y = self.plane.x * sin_angle + self.plane.y * cos_angle
        self.plane = Vec2(new_plane_x, new_plane_y)

@dataclass
class WorldMap:
    data: list[list[int]]  # 2D Grid: 0 = Empty, >0 = Wall Color ID

    def get_cell(self, x: int, y: int) -> int:
        """Get cell value at (x, y), return 0 if out of bounds"""
        if 0 <= x < len(self.data[0]) and 0 <= y < len(self.data):
            return self.data[y][x]
        return 0