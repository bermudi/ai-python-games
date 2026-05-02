"""
Configuration constants for the Entropy Hexagon simulation.
"""

# Window settings
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 800
FPS: int = 60
BACKGROUND_COLOR: tuple[int, int, int] = (30, 30, 40)

# Physics settings
PHYSICS_HZ: int = 240  # Physics updates per second (fixed timestep)
PHYSICS_STEP: float = 1.0 / PHYSICS_HZ  # Fixed timestep in seconds

# Hexagon settings
INITIAL_RADIUS: float = 250.0
HEXAGON_COLOR: tuple[int, int, int] = (100, 200, 255)
ROTATION_SPEED_RPM: float = 30.0  # Rotations per minute
ROTATION_SPEED_RPS: float = ROTATION_SPEED_RPM / 60.0  # Rotations per second
ROTATION_SPEED_RAD_PER_SEC: float = ROTATION_SPEED_RPS * 2 * 3.14159  # Radians per second

# Shrinking rate (linear decay per second)
SHRINK_RATE: float = 20.0  # pixels per second
MIN_RADIUS: float = 80.0  # Minimum radius (stops shrinking here)

# Ball settings
BALL_RADIUS: float = 10.0
BALL_COLOR: tuple[int, int, int] = (255, 200, 100)
BALL_MASS: float = 1.0

# Physics parameters
GRAVITY: float = 300.0  # pixels per second squared
AIR_RESISTANCE: float = 0.98  # Velocity multiplier per physics step
RESTITUTION: float = 0.85  # Bounciness (0 = no bounce, 1 = perfect bounce)
FRICTION: float = 0.15  # Friction coefficient (0 = no friction, 1 = full friction)

# Initial ball velocity
INITIAL_VELOCITY_RANGE: float = 50.0  # Random initial velocity range
