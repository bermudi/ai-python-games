### Test Subject: "Retro Raycasting Engine"

### 1. Architectural Strategy: The "DDA" Rendering Loop

We will implement a 2.5D raycasting engine. The core requirement is to separate the **Map Data** from the **Ray Calculation**. The engine must use the **DDA (Digital Differential Analyzer)** algorithm to traverse the grid.

**The Loop Logic:**
```text
While Running:
  1. Handle Input (Rotate Player, Move Player).
  2. For every vertical pixel column (0 to SCREEN_WIDTH):
       a. Calculate Ray Position and Direction.
       b. Execute DDA Algorithm to find wall impact.
       c. Calculate perpendicular distance (fix fish-eye effect).
       d. Calculate wall height based on distance.
       e. Buffer the vertical line for rendering.
  3. Render all buffered lines to Pygame surface.
```

### 2. Configuration & Constants (`config.py`)

Centralize settings to tune the field of view and resolution.

```python
# Screen
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60

# World
TILE_SIZE = 64
MAP_WIDTH = 24
MAP_HEIGHT = 24

# Player
FOV = 0.66    # Field of View modifier (approx 66 degrees)
MOVE_SPEED = 5.0
ROT_SPEED = 3.0
```

### 3. Core Math Abstractions (`math_utils.py`)

Do **not** use `numpy`. We need a lightweight specific math class to handle floating point positions vs integer grid coordinates.

```python
from dataclasses import dataclass
import math

@dataclass
class Vec2:
    x: float
    y: float

    # Must implement:
    # __add__, __sub__, __mul__ (scalar)
    # rotate(angle_speed) -> returns new Vec2
    # length_sq() -> float (faster than length for comparisons)
```

### 4. Domain Models (`models.py`)

The Player must rely on the **Camera Plane** technique for raycasting, not just a simple angle.

```python
@dataclass
class Player:
    pos: Vec2       # Exact position
    dir: Vec2       # Direction vector (normalized)
    plane: Vec2     # Camera plane (perpendicular to dir)

    def rotate(self, rot_speed: float):
        """
        Must apply rotation matrix to BOTH self.dir and self.plane
        to ensure FOV remains constant.

        [ x ]   [ cos -sin ] [ x ]
        [ y ] = [ sin  cos ] [ y ]
        """
        pass

@dataclass
class WorldMap:
    data: list[list[int]] # 2D Grid: 0 = Empty, >0 = Wall Color ID

    def get_cell(self, x: int, y: int) -> int:
        pass
```

### 5. The Raycaster (`engine.py`)

This is the "Workhorse" test. It must implement the DDA algorithm step-by-step.

**Crucial Math Concept:** We must calculate `side_dist` (distance to next grid line) and `delta_dist` (distance between grid lines) to jump grid squares efficiently.

```python
class Raycaster:
    def cast_rays(self, player: Player, world_map: WorldMap) -> list[dict]:
        results = []
        for x in range(SCREEN_WIDTH):
            # 1. Calculate Ray Direction
            camera_x = 2 * x / SCREEN_WIDTH - 1
            ray_dir = player.dir + (player.plane * camera_x)

            # 2. Setup DDA
            map_x = int(player.pos.x)
            map_y = int(player.pos.y)

            # Calculate delta_dist (avoid divide by zero)
            delta_dist_x = abs(1 / ray_dir.x) if ray_dir.x != 0 else 1e30
            delta_dist_y = abs(1 / ray_dir.y) if ray_dir.y != 0 else 1e30

            # Calculate step and initial side_dist
            # (Logic required: if ray_dir < 0, step = -1, etc.)

            # 3. Perform DDA Step
            hit = 0
            side = 0 # 0 for NS, 1 for EW
            while hit == 0:
                # Jump to next map square, OR in x or y direction
                # Update side_dist
                # Check collision with world_map.get_cell(map_x, map_y)
                pass

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
```

### 6. The Renderer (`view.py`)

Decoupled rendering. It receives the scanlines from the engine and draws them.

```python
import pygame

class PygameRenderer:
    def render_frame(self, scanlines: list[dict]):
        self.screen.fill((50, 50, 50)) # Ceiling/Floor

        for line in scanlines:
            # Calculate Line Height
            # h = SCREEN_HEIGHT / line['dist']

            # Calculate Darker color for 'side == 1' (fake lighting)

            # Draw Vertical Line using pygame.draw.line
            pass
```

### 7. Implementation Roadmap

1.  **Math Setup**: Implement `Vec2` and the `Player.rotate` matrix logic.
2.  **Map**: Create a simple hardcoded integer grid (1s around the borders, some random blocks inside).
3.  **Engine (DDA)**: Implement the steps in Section 5.
    *   *Constraint:* You must handle the `division by zero` edge case in `delta_dist`.
4.  **View**: Connect Pygame. Draw the result.
5.  **Input**: Hook up WASD keys to move the player vector and Left/Right keys to rotate.
