"""
Main entry point for the Entropy Hexagon simulation.
Implements the fixed timestep game loop.
"""

import pygame
import sys
import random
from vector_math import Vector2
from models import Ball, Hexagon
from physics import PhysicsEngine
from renderer import Renderer
import config


def create_initial_ball(screen_center: Vector2) -> Ball:
    """Create a ball with random initial velocity."""
    # Random velocity in a range
    vx = random.uniform(-config.INITIAL_VELOCITY_RANGE, config.INITIAL_VELOCITY_RANGE)
    vy = random.uniform(-config.INITIAL_VELOCITY_RANGE, config.INITIAL_VELOCITY_RANGE)

    return Ball(
        position=screen_center.copy(),
        velocity=Vector2(vx, vy)
    )


def main() -> None:
    """Main game loop with fixed timestep physics."""
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Entropy Hexagon - Physics Simulation")
    clock = pygame.time.Clock()

    # Calculate screen center
    screen_center = Vector2(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2)

    # Initialize game objects
    ball = create_initial_ball(screen_center)
    hexagon = Hexagon(center=screen_center)

    # Initialize systems
    physics = PhysicsEngine()
    renderer = Renderer(screen)

    # Fixed timestep variables
    accumulator = 0.0  # Accumulates time for physics updates
    physics_step = config.PHYSICS_STEP

    running = True
    while running:
        # Calculate delta time in seconds
        dt = clock.get_time() / 1000.0  # Convert milliseconds to seconds

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Reset simulation
                    ball = create_initial_ball(screen_center)
                    hexagon.reset()

        # Fixed timestep physics update
        # Accumulate time
        accumulator += dt

        # Process physics updates while we have accumulated enough time
        while accumulator >= physics_step:
            # Update hexagon (rotation and shrinking)
            hexagon.update(physics_step)

            # Update physics
            physics.update(ball, hexagon, physics_step)

            # Remove the processed time from accumulator
            accumulator -= physics_step

        # Clear screen
        screen.fill(config.BACKGROUND_COLOR)

        # Render
        renderer.draw_hexagon(hexagon)
        renderer.draw_ball(ball)
        renderer.draw_instructions()

        # Update display
        pygame.display.flip()

        # Cap framerate (FPS)
        clock.tick(config.FPS)

    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
