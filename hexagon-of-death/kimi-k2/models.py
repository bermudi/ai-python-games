"""
Model classes for the Entropy Hexagon simulation.
"""

from dataclasses import dataclass, field
from math import cos, sin
from vector_math import Vector2
import config


@dataclass
class Ball:
    """Ball object with position, velocity, and physics properties."""
    position: Vector2
    velocity: Vector2
    radius: float = config.BALL_RADIUS
    mass: float = config.BALL_MASS

    @classmethod
    def create_at_center(cls, screen_center: Vector2) -> 'Ball':
        """Create a new ball at the center of the screen."""
        return cls(
            position=screen_center.copy(),
            velocity=Vector2.zero()
        )

    def apply_force(self, force: Vector2, dt: float) -> None:
        """Apply a force to the ball (F = ma)."""
        acceleration = force / self.mass
        self.velocity = self.velocity + (acceleration * dt)


@dataclass
class Hexagon:
    """
    Hexagon that rotates and shrinks over time.
    Provides methods to get wall geometry and wall velocity at any point.
    """
    center: Vector2
    radius: float = config.INITIAL_RADIUS
    rotation: float = 0.0  # Current rotation in radians
    rotation_speed: float = config.ROTATION_SPEED_RAD_PER_SEC
    shrink_rate: float = config.SHRINK_RATE
    min_radius: float = config.MIN_RADIUS

    @property
    def vertex_count(self) -> int:
        """Number of vertices (always 6 for hexagon)."""
        return 6

    def update(self, dt: float) -> None:
        """
        Update hexagon state (rotation and shrinking).
        """
        # Rotate
        self.rotation += self.rotation_speed * dt

        # Shrink (but not below minimum)
        self.radius = max(self.min_radius, self.radius - self.shrink_rate * dt)

    def reset(self) -> None:
        """Reset to initial state."""
        self.radius = config.INITIAL_RADIUS
        self.rotation = 0.0

    def get_vertices(self) -> list[Vector2]:
        """
        Get the current vertex positions in world coordinates.
        """
        vertices = []
        for i in range(self.vertex_count):
            # Angle for each vertex (60 degrees apart = 2π/6)
            angle = self.rotation + (i * 2 * 3.14159 / self.vertex_count)
            # Vertex position relative to center
            vertex = Vector2(
                cos(angle) * self.radius,
                sin(angle) * self.radius
            )
            # Add center offset
            vertices.append(self.center + vertex)
        return vertices

    def get_wall(self, wall_index: int) -> tuple[Vector2, Vector2]:
        """
        Get the start and end points of a wall segment.
        Returns: (start_point, end_point)
        """
        vertices = self.get_vertices()
        start = vertices[wall_index]
        end = vertices[(wall_index + 1) % self.vertex_count]
        return (start, end)

    def get_wall_normal(self, wall_index: int) -> Vector2:
        """
        Get the outward-facing normal vector for a wall segment.
        The normal is perpendicular to the wall and points outward.
        """
        vertices = self.get_vertices()
        start = vertices[wall_index]
        end = vertices[(wall_index + 1) % self.vertex_count]

        # Wall direction vector
        wall_vec = end - start

        # Get normal by rotating wall vector 90 degrees clockwise
        # This gives a rightward-pointing normal when facing from start to end
        normal = wall_vec.perpendicular().normalized

        # Calculate midpoint of wall
        midpoint = (start + end) / 2

        # Determine if normal points outward (away from center)
        # By checking dot product with vector from center to midpoint
        center_to_mid = midpoint - self.center

        # If dot product is negative, normal points inward, so flip it
        if normal.dot(center_to_mid) > 0:
            normal = -normal

        return normal

    def get_wall_velocity_at_point(
        self,
        impact_point: Vector2,
        wall_index: int
    ) -> Vector2:
        """
        Calculate the velocity of the wall at a specific impact point.

        The wall velocity has TWO components:
        1. Tangential velocity from rotation (v_tan = omega × r)
        2. Radial velocity from shrinking (v_rad = pointing toward center)

        Args:
            impact_point: Point on the wall where collision occurs
            wall_index: Index of the wall segment

        Returns:
            Vector2 representing wall velocity at impact point
        """
        # Vector from center to impact point
        r_vec = impact_point - self.center

        # 1. Tangential velocity from rotation
        # For 2D, tangential velocity is perpendicular to radius vector
        # Magnitude = angular_velocity * radius
        angular_vel = self.rotation_speed
        tangential_speed = angular_vel * r_vec.magnitude

        # Tangential direction is perpendicular to radius
        # Right-hand rule: rotation is counter-clockwise (positive z)
        # So tangential is 90 degrees ahead of radial vector
        tangential_dir = r_vec.perpendicular().normalized
        tangential_vel = tangential_dir * tangential_speed

        # 2. Radial velocity from shrinking
        # Points directly toward center if shrinking
        # Magnitude = shrink_rate
        if self.radius > self.min_radius and self.shrink_rate > 0:
            radial_dir = (self.center - impact_point).normalized
            radial_vel = radial_dir * self.shrink_rate
        else:
            radial_vel = Vector2.zero()

        # Total wall velocity is sum of both components
        return tangential_vel + radial_vel

    def find_closest_wall(self, point: Vector2) -> tuple[int, float, Vector2]:
        """
        Find the closest wall to a given point.

        Returns:
            Tuple of (wall_index, distance_to_wall, closest_point_on_wall)
        """
        min_distance = float('inf')
        closest_wall_index = 0
        closest_point = Vector2.zero()

        for i in range(self.vertex_count):
            start, end = self.get_wall(i)
            wall_vec = end - start

            # Project point onto wall segment
            t = ((point - start).dot(wall_vec)) / wall_vec.magnitude_squared

            # Clamp to segment endpoints
            t = max(0.0, min(1.0, t))

            # Closest point on the wall segment
            wall_point = start + wall_vec * t

            # Distance from point to wall
            distance = point.distance_to(wall_point)

            if distance < min_distance:
                min_distance = distance
                closest_wall_index = i
                closest_point = wall_point

        return closest_wall_index, min_distance, closest_point
