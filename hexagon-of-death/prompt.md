Here is the refined prompt. I have stripped away the code snippets, removed the explicit math formulas, and added a specific **"Complication"** that raises the difficulty significantly.

This prompt tests whether the LLM can translate *concepts* into code without having the implementation dictated to it.

***

# Technical Specification: The "Entropy" Hexagon Simulation

**Objective:** Write a robust 2D physics simulation in Python using `pygame`. The simulation involves a ball bouncing inside a generic polygon (initially a Hexagon) that is **rotating** and **continuously shrinking**.

### 1. Core Constraints & Architecture
*   **No Third-Party Math Libraries:** You must not use `numpy` or `pygame.math`. You must implement a custom 2D Vector class (`vector_math.py`) using Python's `dataclasses`.
*   **The Simulation Loop:** You must implement a **Fixed Timestep** physics loop that is decoupled from the rendering framerate.
    *   *Reasoning:* The rendering might happen at 60 FPS, but physics must solve at a higher resolution (e.g., 120-240Hz) to prevent "tunneling" (the ball passing through walls at high speeds).
    *   *Pattern:* Use an accumulator approach (calculate `dt`, add to `lag`, step physics while `lag >= physics_step`).
*   **Code Structure:** The solution must be modular.
    *   `config.py`: Constants.
    *   `vector_math.py`: The math library.
    *   `models.py`: State containers (Ball, Hexagon).
    *   `physics.py`: The solver logic.
    *   `renderer.py`: The Pygame view logic.
    *   `main.py`: The entry point and loop.

### 2. The Complication: "Entropy" Mode
The simulation involves two dynamic forces acting on the environment simultaneously:
1.  **Rotation:** The Hexagon spins at a constant rate (e.g., 30 RPM).
2.  **Contraction (The Complication):** The Hexagon's radius slowly decreases over time (linear decay).
    *   *Physics Implication:* The walls are not just moving tangentially (spin); they are also moving radially inward. The ball must react to the wall closing in on it.

### 3. Physics Requirements (The "Test")
The physics solver is the critical component. It must support:
*   **Gravity:** Constant downward force.
*   **Air Resistance:** Linear drag on the ball.
*   **Realistic Wall Interaction:**
    *   You must calculate collisions based on the **Relative Velocity** at the exact point of impact.
    *   The velocity of the wall at the impact point is the sum of its **Tangential Velocity** (from rotation) and its **Radial Velocity** (from shrinking).
    *   **Friction:** When the ball hits the spinning wall, it should gain some tangential velocity (spin transfer).
    *   **Restitution:** The bounce should be slightly lossy (not 100% elastic).

### 4. Implementation Details
*   **Visuals:**
    *   Draw the Hexagon walls.
    *   Draw the Ball.
    *   Draw a visual indicator of the Hexagon's current rotation (e.g., different colored vertices or a line from center to one vertex) so the spin is visible.
*   **Controls:**
    *   Spacebar: Reset the simulation (restore radius, move ball to center).
    *   Esc: Quit.
*   **Type Hinting:** All functions and methods must use standard Python type hints.

### 5. Evaluation Criteria
*   **Stability:** Does the ball tunnel through the wall when the hexagon gets very small? (The fixed timestep loop should prevent this).
*   **Physics Accuracy:** When the ball hits a wall moving *towards* it (shrinking), does it bounce off with *increased* energy? When it hits a wall moving *away* (if spinning fast), does it lose energy?
*   **Code Quality:** Is the vector math library complete and readable?

---

**Instruction:** Generate the complete project structure and code files based on this specification.