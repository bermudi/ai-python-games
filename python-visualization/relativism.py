import matplotlib
matplotlib.use('Qt5Agg')  # You can also try 'Qt5Agg' or other backends
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def relativistic_addition(u: float, v: float, c: float = 1.0) -> float:
    return (u + v) / (1 + (u * v) / (c**2))

# Setup
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
c = 1.0  # Speed of light in our units
v_rel = 0.9  # Each ship moves at 0.9c relative to the previous

# Calculate velocities
v_B_classical = v_rel  # Ship B relative to A
v_C_classical = v_B_classical + v_rel  # Ship C relative to A (classical)

v_B_relativistic = v_rel  # Ship B relative to A  
v_C_relativistic = relativistic_addition(v_B_relativistic, v_rel, c)  # Ship C relative to A (relativistic)

print(f"Classical: Ship C moves at {v_C_classical:.3f}c relative to Ship A")
print(f"Relativistic: Ship C moves at {v_C_relativistic:.6f}c relative to Ship A")

# Animation parameters
t_max = 10
dt = 0.1
t_values = np.arange(0, t_max, dt)

# Initialize ship positions
ship_A_pos = [0, 0]  # Ships A always at origin
ship_B_classical = []
ship_C_classical = []
ship_B_relativistic = []
ship_C_relativistic = []

def animate(frame):
    t = frame * dt
    
    # Clear axes
    ax1.clear()
    ax2.clear()
    
    # Calculate positions at time t
    # Ship A always at origin (0)
    pos_A = 0
    
    # Classical scenario
    pos_B_classical = v_B_classical * t
    pos_C_classical = v_C_classical * t
    
    # Relativistic scenario  
    pos_B_relativistic = v_B_relativistic * t
    pos_C_relativistic = v_C_relativistic * t
    
    # Plot classical scenario
    ax1.scatter([pos_A], [0], s=200, c='blue', marker='s', label='Ship A (stationary)')
    ax1.scatter([pos_B_classical], [0], s=200, c='green', marker='^', label=f'Ship B ({v_B_classical:.1f}c)')
    ax1.scatter([pos_C_classical], [0], s=200, c='red', marker='o', label=f'Ship C ({v_C_classical:.1f}c)')
    
    ax1.set_xlim(-1, 15)
    ax1.set_ylim(-0.5, 0.5)
    ax1.set_title(f'Classical Physics: Ship C at {v_C_classical:.1f}c (Faster than light!)', fontsize=14, color='red')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylabel('Classical')
    
    # Add speed of light reference line
    light_pos = c * t
    ax1.axvline(x=light_pos, color='gold', linestyle='--', linewidth=3, alpha=0.7, label='Light beam')
    
    # Plot relativistic scenario
    ax2.scatter([pos_A], [0], s=200, c='blue', marker='s', label='Ship A (stationary)')
    ax2.scatter([pos_B_relativistic], [0], s=200, c='green', marker='^', label=f'Ship B ({v_B_relativistic:.1f}c)')
    ax2.scatter([pos_C_relativistic], [0], s=200, c='red', marker='o', label=f'Ship C ({v_C_relativistic:.3f}c)')
    
    ax2.set_xlim(-1, 15)
    ax2.set_ylim(-0.5, 0.5)
    ax2.set_title(f'Relativistic Physics: Ship C at {v_C_relativistic:.3f}c (Under light speed)', fontsize=14, color='green')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlabel('Position (light-seconds)')
    ax2.set_ylabel('Relativistic')
    
    # Add speed of light reference line
    ax2.axvline(x=light_pos, color='gold', linestyle='--', linewidth=3, alpha=0.7, label='Light beam')
    
    # Add time display
    fig.suptitle(f'Time: {t:.1f} seconds\nShip B moves {v_rel:.1f}c relative to A, Ship C moves {v_rel:.1f}c relative to B', fontsize=12)

# Create and run animation
anim = animation.FuncAnimation(fig, animate, frames=len(t_values), interval=100, repeat=True)
plt.tight_layout()
plt.show()

# Static comparison for easier viewing