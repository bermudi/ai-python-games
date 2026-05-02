"""
Physics engine for the Entropy Hexagon simulation.
Handles collision detection and response with moving walls.
"""

from vector_math import Vector2
from models import Ball, Hexagon
import config


class PhysicsEngine:
    """
    Physics solver that handles:
    - Gravity
    - Air resistance
    - Collision detection with moving walls
    - Collision response with friction and restitution
    """

    def __init__(self):
        self.gravity_force = Vector2(0, config.GRAVITY)

    def update_ball_physics(self, ball: Ball, dt: float) -> None:
        """
        Update ball physics (excluding wall collisions).
        """
        # Apply gravity: F = ma, so a = F/m
        ball.apply_force(self.gravity_force, dt)

        # Apply air resistance (linear drag)
        ball.velocity = ball.velocity * config.AIR_RESISTANCE

    def check_and_resolve_collision(
        self,
        ball: Ball,
        hexagon: Hexagon
    ) -> bool:
        """
        Check for collision between ball and hexagon walls.
        If collision is detected, resolve it using realistic physics.

        Returns True if collision was detected and resolved.
        """
        # Find closest wall to ball
        wall_index, distance, closest_point = hexagon.find_closest_wall(ball.position)

        # If distance <= ball.radius, collision occurred
        if distance <= ball.radius:
            # Calculate wall normal (points outward)
            normal = hexagon.get_wall_normal(wall_index)

            # Get wall velocity at the impact point
            wall_vel = hexagon.get_wall_velocity_at_point(closest_point, wall_index)

            # Calculate relative velocity (ball velocity relative to wall)
            relative_vel = ball.velocity - wall_vel

            # Decompose relative velocity into normal and tangential components
            vel_normal_mag = relative_vel.dot(normal)

            # If ball is moving away from wall, don't process collision
            if vel_normal_mag > 0:
                return False

            # Separate ball from wall (prevent overlap)
            overlap = ball.radius - distance
            separation_vec = normal * overlap
            ball.position = ball.position + separation_vec

            # Reflect the normal component of relative velocity (with restitution)
            # v_new = v - (1 + e) * (v · n) * n
            # But we need to add back the wall velocity
            reflected_relative = relative_vel - normal * (vel_normal_mag * (1 + config.RESTITUTION))

            # Calculate friction in tangential direction
            # Get tangent vector (perpendicular to normal)
            tangent = normal.perpendicular()

            # Decompose into tangential component
            vel_tangent_mag = relative_vel.dot(tangent)

            # Apply friction: reduces tangential component
            # f = friction coefficient * change in normal velocity
            friction_force = abs(vel_normal_mag * config.FRICTION)
            vel_tangent_mag = max(0, abs(vel_tangent_mag) - friction_force) * (1 if vel_tangent_mag >= 0 else -1)

            # Reconstruct final relative velocity
            final_relative_vel = tangent * vel_tangent_mag + reflected_relative.project_onto(normal)

            # Final ball velocity = relative velocity + wall velocity
            ball.velocity = final_relative_vel + wall_vel

            return True

        return False

    def update(
        self,
        ball: Ball,
        hexagon: Hexagon,
        dt: float
    ) -> bool:
        """
        Full physics update step.

        Returns True if collision occurred during this step.
        """
        collision_occurred = False

        # Update ball physics (gravity, drag)
        self.update_ball_physics(ball, dt)

        # Check for and resolve collisions with hexagon
        if self.check_and_resolve_collision(ball, hexagon):
            collision_occurred = True

        # Update ball position
        ball.position = ball.position + (ball.velocity * dt)

        return collision_occurred
