"""
Custom 2D Vector implementation using dataclasses.
No numpy or pygame.math dependencies.
"""

from dataclasses import dataclass
from math import sqrt, atan2, cos, sin


@dataclass
class Vector2:
    """2D Vector class with common vector operations."""
    x: float
    y: float

    # Constructors
    @classmethod
    def zero(cls) -> 'Vector2':
        """Create a zero vector."""
        return cls(0.0, 0.0)

    @classmethod
    def from_angle(cls, angle_rad: float, magnitude: float = 1.0) -> 'Vector2':
        """Create a vector from an angle and magnitude."""
        return cls(cos(angle_rad) * magnitude, sin(angle_rad) * magnitude)

    def copy(self) -> 'Vector2':
        """Create a copy of this vector."""
        return Vector2(self.x, self.y)

    # Basic operations
    def __add__(self, other: 'Vector2') -> 'Vector2':
        """Add two vectors."""
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2') -> 'Vector2':
        """Subtract two vectors."""
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vector2':
        """Multiply vector by scalar."""
        return Vector2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> 'Vector2':
        """Multiply scalar by vector (commutative)."""
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> 'Vector2':
        """Divide vector by scalar."""
        return Vector2(self.x / scalar, self.y / scalar)

    def __neg__(self) -> 'Vector2':
        """Negate vector."""
        return Vector2(-self.x, -self.y)

    # Properties
    @property
    def magnitude(self) -> float:
        """Get vector magnitude (length)."""
        return sqrt(self.x * self.x + self.y * self.y)

    @property
    def magnitude_squared(self) -> float:
        """Get squared magnitude (faster for comparisons)."""
        return self.x * self.x + self.y * self.y

    @property
    def angle(self) -> float:
        """Get vector angle in radians."""
        return atan2(self.y, self.x)

    @property
    def normalized(self) -> 'Vector2':
        """Get normalized vector (unit vector)."""
        mag = self.magnitude
        if mag == 0:
            return Vector2.zero()
        return Vector2(self.x / mag, self.y / mag)

    # Vector operations
    def dot(self, other: 'Vector2') -> float:
        """Dot product of two vectors."""
        return self.x * other.x + self.y * other.y

    def cross(self, other: 'Vector2') -> float:
        """Cross product (scalar result for 2D vectors)."""
        return self.x * other.y - self.y * other.x

    def distance_to(self, other: 'Vector2') -> float:
        """Distance to another vector."""
        dx = self.x - other.x
        dy = self.y - other.y
        return sqrt(dx * dx + dy * dy)

    def lerp(self, other: 'Vector2', t: float) -> 'Vector2':
        """Linear interpolation between two vectors."""
        return self + (other - self) * t

    def project_onto(self, other: 'Vector2') -> 'Vector2':
        """Project this vector onto another vector."""
        other_mag_sq = other.magnitude_squared
        if other_mag_sq == 0:
            return Vector2.zero()
        return other * (self.dot(other) / other_mag_sq)

    def rotate(self, angle_rad: float) -> 'Vector2':
        """Rotate vector by an angle (radians)."""
        cos_a = cos(angle_rad)
        sin_a = sin(angle_rad)
        return Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )

    def perpendicular(self) -> 'Vector2':
        """Get perpendicular vector (rotated 90 degrees clockwise)."""
        return Vector2(self.y, -self.x)

    # Utility
    def to_tuple(self) -> tuple[float, float]:
        """Convert to tuple."""
        return (self.x, self.y)

    def to_int_tuple(self) -> tuple[int, int]:
        """Convert to integer tuple (for drawing)."""
        return (int(self.x), int(self.y))
