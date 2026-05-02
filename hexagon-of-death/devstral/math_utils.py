from dataclasses import dataclass
import math

@dataclass
class Vec2:
    x: float
    y: float

    def __add__(self, other):
        """Vector addition"""
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        return Vec2(self.x + other, self.y + other)

    def __sub__(self, other):
        """Vector subtraction"""
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        return Vec2(self.x - other, self.y - other)

    def __mul__(self, scalar):
        """Scalar multiplication"""
        return Vec2(self.x * scalar, self.y * scalar)

    def rotate(self, angle_speed: float):
        """Rotate vector by angle_speed (in radians)"""
        cos_angle = math.cos(angle_speed)
        sin_angle = math.sin(angle_speed)
        
        new_x = self.x * cos_angle - self.y * sin_angle
        new_y = self.x * sin_angle + self.y * cos_angle
        
        return Vec2(new_x, new_y)

    def length_sq(self) -> float:
        """Return squared length (faster for comparisons)"""
        return self.x * self.x + self.y * self.y

    def length(self) -> float:
        """Return actual length"""
        return math.sqrt(self.length_sq())

    def normalize(self):
        """Return normalized vector"""
        length = self.length()
        if length > 0:
            return Vec2(self.x / length, self.y / length)
        return Vec2(self.x, self.y)