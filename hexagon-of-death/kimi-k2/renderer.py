"""
Renderer for the Entropy Hexagon simulation using Pygame.
"""

import pygame
from vector_math import Vector2
from models import Ball, Hexagon
import config


class Renderer:
    """
    Handles all drawing operations for the simulation.
    """

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def draw_hexagon(self, hexagon: Hexagon) -> None:
        """Draw the hexagon walls."""
        # Get vertices
        vertices = hexagon.get_vertices()

        # Draw walls as lines connecting vertices
        for i in range(hexagon.vertex_count):
            start = vertices[i].to_int_tuple()
            end = vertices[(i + 1) % hexagon.vertex_count].to_int_tuple()

            pygame.draw.line(
                self.screen,
                config.HEXAGON_COLOR,
                start,
                end,
                3
            )

        # Draw rotation indicator: a line from center to first vertex
        # First vertex is drawn with a different color to show rotation
        first_vertex = vertices[0]
        pygame.draw.line(
            self.screen,
            (255, 255, 0),  # Yellow indicator line
            hexagon.center.to_int_tuple(),
            first_vertex.to_int_tuple(),
            4
        )

        # Draw first vertex with special color
        pygame.draw.circle(
            self.screen,
            (255, 100, 100),  # Red first vertex
            first_vertex.to_int_tuple(),
            8
        )

        # Draw radius info
        self._draw_info(hexagon)

    def _draw_info(self, hexagon: Hexagon) -> None:
        """Draw radius and rotation info."""
        # Calculate radius in screen coords
        radius_text = self.font.render(
            f"Radius: {hexagon.radius:.1f}px",
            True,
            (200, 200, 200)
        )
        rotation_deg = (hexagon.rotation * 180 / 3.14159) % 360
        rotation_text = self.font.render(
            f"Rotation: {rotation_deg:.1f}°",
            True,
            (200, 200, 200)
        )

        # Position text at top-left
        self.screen.blit(radius_text, (10, 10))
        self.screen.blit(rotation_text, (10, 45))

    def draw_ball(self, ball: Ball) -> None:
        """Draw the ball."""
        pygame.draw.circle(
            self.screen,
            config.BALL_COLOR,
            ball.position.to_int_tuple(),
            int(ball.radius)
        )

        # Optional: Draw velocity vector (for debugging/visual feedback)
        # Uncomment to see ball velocity
        # velocity_end = ball.position + ball.velocity * 0.1
        # pygame.draw.line(
        #     self.screen,
        #     (255, 0, 0),
        #     ball.position.to_int_tuple(),
        #     velocity_end.to_int_tuple(),
        #     2
        # )

    def draw_instructions(self) -> None:
        """Draw control instructions."""
        instructions = [
            "SPACE: Reset",
            "ESC: Quit"
        ]

        y_offset = config.SCREEN_HEIGHT - 80
        for instruction in instructions:
            text = self.font.render(instruction, True, (150, 150, 150))
            self.screen.blit(text, (10, y_offset))
            y_offset += 30
