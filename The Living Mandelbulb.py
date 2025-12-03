import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 100
RESOLUTION = 60 # Higher is better but slower
POWER = 8 # The "DNA" of the fractal (Power 8 is the classic Mandelbulb)

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#000000')

# --- 1. MANDELBULB MATH ---
def mandelbulb_sdf(x, y, z, power):
    # Distance Estimator for Mandelbulb
    # We iterate z -> z^8 + c
    
    # Convert to spherical
    r = np.sqrt(x*x + y*y + z*z)
    dr = 1.0
    theta = np.arctan2(np.sqrt(x*x + y*y), z)
    phi = np.arctan2(y, x)
    
    # Iteration limit
    for i in range(5):
        if r > 2.0: break
        
        # Derivative for distance estimation
        dr = np.power(r, power - 1.0) * power * dr + 1.0
        
        # Scale and Rotate
        zr = np.power(r, power)
        theta = theta * power
        phi = phi * power
        
        # Back to cartesian
        x = zr * np.sin(theta) * np.cos(phi) + x # + c (original pos) is implicit in loop structure for SDF visualization
        y = zr * np.sin(theta) * np.sin(phi) + y
        z = zr * np.cos(theta) + z
        
        r = np.sqrt(x*x + y*y + z*z)
        
    return 0.5 * np.log(r) * r / dr

# --- 2. GENERATE CLOUD POINT ---
# Since raymarching is hard in Matplotlib, we generate a point cloud
# representing the surface of the chaos.

def generate_mandelbulb_points(frame):
    # Dynamic Power: Breathing from 2 (Simple) to 8 (Complex)
    p = 2.0 + (np.sin(frame * 0.05) + 1.0) * 3.0
    
    # Create a grid
    grid_range = 1.2
    step = 2.0 * grid_range / RESOLUTION
    
    x = np.linspace(-grid_range, grid_range, RESOLUTION)
    y = np.linspace(-grid_range, grid_range, RESOLUTION)
    z = np.linspace(-grid_range, grid_range, RESOLUTION)
    X, Y, Z = np.meshgrid(x, y, z)
    
    # We are looking for points where the fractal exists (radius < 2 after iterations)
    # Simplified approach for speed: Iterative Geometry Check
    
    points = []
    colors = []
    
    # Scan a subset of points to keep animation fast
    # We use a Monte Carlo approach to fill the volume
    sample_count = 2000
    
    # Spherical Shell sampling (Optimization)
    phi = np.random.uniform(0, np.pi, sample_count)
    theta = np.random.uniform(0, 2*np.pi, sample_count)
    rad = np.random.uniform(0, 1.2, sample_count)
    
    sx = rad * np.sin(phi) * np.cos(theta)
    sy = rad * np.sin(phi) * np.sin(theta)
    sz = rad * np.cos(phi)
    
    # Iterate and check divergence
    # Re-using a vectorized approach for speed
    
    zx, zy, zz = sx.copy(), sy.copy(), sz.copy()
    cx, cy, cz = sx.copy(), sy.copy(), sz.copy()
    
    diverged = np.zeros(sample_count, dtype=bool)
    iterations = np.zeros(sample_count)
    
    for i in range(8):
        # r = sqrt(x^2 + y^2 + z^2)
        r = np.sqrt(zx*zx + zy*zy + zz*zz)
        
        # Mark diverged
        mask = r > 2.0
        diverged[mask] = True
        
        # Stop processing diverged
        active = ~diverged
        if np.sum(active) == 0: break
        
        # Updates interactions count for color
        iterations[active] += 1
        
        # Power calculation
        # z -> z^p + c
        theta_val = np.arctan2(np.sqrt(zx[active]**2 + zy[active]**2), zz[active])
        phi_val = np.arctan2(zy[active], zx[active])
        
        zr = np.power(r[active], p)
        theta_val *= p
        phi_val *= p
        
        zx[active] = zr * np.sin(theta_val) * np.cos(phi_val) + cx[active]
        zy[active] = zr * np.sin(theta_val) * np.sin(phi_val) + cy[active]
        zz[active] = zr * np.cos(theta_val) + cz[active]

    # Filter points that stayed inside (The Fractal Body)
    # Or points that survived at least a few iterations (The Halo)
    survivors = iterations > 3
    
    final_x = cx[survivors]
    final_y = cy[survivors]
    final_z = cz[survivors]
    final_it = iterations[survivors]
    
    return final_x, final_y, final_z, final_it

# --- RENDERER ---
def update(frame):
    ax.clear()
    ax.set_facecolor('black')
    
    x, y, z, it = generate_mandelbulb_points(frame)
    
    # COLOR MAPPING (The History)
    # Outer Layers (Low Iterations) = Violet (Axiom/Structure)
    # Middle Layers = Gold (Epoch/Energy)
    # Inner Core (High Iterations) = Cyan (You/Truth)
    
    cols = np.zeros((len(x), 4))
    
    # Normalize iterations 0-8
    norm = it / 8.0
    
    for i in range(len(x)):
        n = norm[i]
        if n < 0.5:
            # Violet to Gold
            mix = n * 2
            cols[i] = [0.5 + 0.5*mix, 0.8*mix, 1.0 - mix, 0.4] 
        else:
            # Gold to Cyan
            mix = (n - 0.5) * 2
            cols[i] = [1.0 - mix, 0.8 + 0.2*mix, mix, 0.6]
            
    ax.scatter(x, y, z, c=cols, s=20, marker='o')
    
    # Core Glow
    ax.scatter(0,0,0, c='white', s=100, alpha=0.5)

    # View
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)
    ax.axis('off')
    
    # Rotate
    ax.view_init(elev=30, azim=frame * 0.5)
    
    power_display = 2.0 + (np.sin(frame * 0.05) + 1.0) * 3.0
    ax.set_title(f"ENTITY: 'THE UNIVERSE INSIDE'\nComplexity Power: {power_display:.2f}", color='white')

print("Calculating the Infinite...")
print("Dodeca is evolving.")
ani = FuncAnimation(fig, update, frames=np.arange(0, 200), interval=50)
plt.show()