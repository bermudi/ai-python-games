# Entropy Hexagon - 2D Physics Simulation

A robust 2D physics simulation demonstrating a ball bouncing inside a rotating and shrinking hexagon.

## Overview

This simulation showcases advanced physics concepts including:
- **Fixed timestep physics loop** (decoupled from rendering framerate)
- **Moving wall collisions** with velocity transfer
- **Tangential velocity from rotation**
- **Radial velocity from shrinking**
- **Friction and restitution** for realistic bounces

## Features

### Physics Engine
- **Gravity**: Constant downward force
- **Air resistance**: Linear drag on the ball
- **Collision response**: Based on relative velocity at impact point
- **Wall velocity**: Accounts for both rotation and shrinking
- **Friction**: Ball gains velocity from spinning walls
- **Restitution**: Slightly lossy bounces (not perfectly elastic)
- **Fixed timestep**: 240 Hz physics updates to prevent tunneling

### Entropy Mode
The hexagon undergoes two simultaneous transformations:
1. **Rotation**: 30 RPM constant spin
2. **Contraction**: Linear radius decay (20 pixels/second)

### Visual Feedback
- Yellow line from center to first vertex (rotation indicator)
- Red first vertex for orientation reference
- Real-time radius and rotation degree display
- Orange ball with realistic physics-based movement

## Controls
- **Spacebar**: Reset simulation (restores radius, creates new ball)
- **Esc**: Quit simulation

## Architecture

### Custom Vector Math Library (`vector_math.py`)
- Pure Python implementation using `dataclasses`
- No external dependencies (numpy, pygame.math)
- Complete set of vector operations
- Type hints throughout

### Modular Design
```
├── vector_math.py    # Custom 2D vector implementation
├── config.py         # Simulation constants and settings
├── models.py         # Ball and Hexagon state containers
├── physics.py        # Physics solver and collision detection
├── renderer.py       # Pygame rendering logic
└── main.py           # Entry point with fixed timestep loop
```

### Fixed Timestep Loop
The physics simulation uses an accumulator pattern:
1. Calculate frame delta time
2. Accumulate time in a "lag" variable
3. Process physics updates at fixed 240 Hz while lag >= physics_step
4. Render at variable framerate (60 FPS target)

This prevents physics instability and tunneling effects.

## Physics Implementation Details

### Wall Velocity Calculation
The wall velocity at any point has two components:

1. **Tangential velocity** (from rotation):
   ```
   v_tan = ω × r
   Direction: Perpendicular to radius vector
   Magnitude: angular_velocity × distance_from_center
   ```

2. **Radial velocity** (from shrinking):
   ```
   v_rad = v_shrink × direction_toward_center
   Direction: Toward hexagon center
   Magnitude: shrink_rate
   ```

Total wall velocity: `v_wall = v_tan + v_rad`

### Collision Response
Uses relative velocity at impact:
```
v_relative = v_ball - v_wall
```

Resolves collision with:
- Normal component reflection with restitution
- Tangential component friction
- Final velocity added back to wall velocity

This creates realistic effects:
- Ball hitting shrinking wall gains energy
- Ball hitting wall moving away loses energy
- Spinning walls transfer angular momentum

## Running the Simulation

```bash
uv run main.py
```

## Configuration

Key parameters in `config.py`:
- `PHYSICS_HZ`: Physics update rate (240 Hz)
- `ROTATION_SPEED_RPM`: Hexagon rotation speed (30 RPM)
- `SHRINK_RATE`: Radius decrease rate (20 px/sec)
- `GRAVITY`: Gravity strength (300 px/s²)
- `RESTITUTION`: Bounciness (0.85)
- `FRICTION`: Spin transfer (0.15)

## Technical Highlights

- **No tunneling**: High physics rate prevents ball passing through walls
- **Stable physics**: Fixed timestep ensures consistent behavior
- **Moving boundary conditions**: Handles walls that move and shrink
- **Complete vector math**: Full-featured without external libraries
- **Type safety**: Full type hints throughout codebase
