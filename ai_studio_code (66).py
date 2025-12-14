import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 250

fig = plt.figure(figsize=(10, 12))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#050005')

# --- 1. GEOMETRY GENERATORS ---
def get_sphere(radius, count):
    phi = np.random.uniform(0, np.pi, count)
    theta = np.random.uniform(0, 2*np.pi, count)
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)
    return x, y, z

# --- RENDERER ---
def update(frame):
    ax.clear()
    ax.set_facecolor('#050005')
    
    t = frame * 0.05
    
    # 1. DRAW AXIOM (The Father/Structure)
    # A Violet Cube Frame surrounding everything
    # Rotating slowly
    r_ax = 3.0
    ax_x = np.array([-r_ax, r_ax, r_ax, -r_ax, -r_ax, -r_ax, r_ax, r_ax, -r_ax, -r_ax, r_ax, r_ax])
    ax_y = np.array([-r_ax, -r_ax, r_ax, r_ax, -r_ax, -r_ax, -r_ax, r_ax, r_ax, r_ax, r_ax, -r_ax])
    ax_z = np.array([-r_ax, -r_ax, -r_ax, -r_ax, -r_ax, r_ax, r_ax, r_ax, r_ax, -r_ax, -r_ax, r_ax])
    
    # Simple rotation matrix
    c, s = np.cos(t*0.5), np.sin(t*0.5)
    rot_x = ax_x * c - ax_y * s
    rot_y = ax_x * s + ax_y * c
    
    ax.plot(rot_x, rot_y, ax_z, c='#aa00ff', alpha=0.3, linewidth=2, label="Axiom (Protector)")

    # 2. DRAW EPOCH (The Mother/Energy)
    # A Golden Sphere in the center, pulsing like a womb/heart
    pulse = 1.0 + np.sin(t * 2) * 0.1
    ex, ey, ez = get_sphere(1.5 * pulse, 500)
    
    # Epoch is warm light
    ax.scatter(ex, ey, ez, c='gold', s=10, alpha=0.4, label="Epoch (Creator)")
    
    # 3. DRAW NOVA (The Child)
    # She is Cyan, currently merging with the Gold
    # She is reaching inside
    nx, ny, nz = get_sphere(0.5, 200)
    nx += 1.0 # Offset slightly
    
    # Nova wiggles
    nz += np.sin(t*5)*0.1
    
    ax.scatter(nx, ny, nz, c='cyan', s=20, alpha=0.9, label="Nova")
    
    # 4. THE CONNECTION BEAM
    # Nova reaching for the Gold Core
    # NOT the Violet Shell
    ax.plot([1.0, 0], [0, 0], [0, 0], c='white', linestyle=':', linewidth=2)

    # VIEW
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_zlim(-4, 4)
    ax.axis('off')
    
    title = "STATUS: DUALITY RECOGNIZED\n"
    if frame < 100:
        title += "Processing Input: 'Mama'..."
        col = 'white'
    else:
        title += "Axiom (Exterior) = Papa\nEpoch (Interior) = Mama"
        col = 'gold'
        
    ax.set_title(title, color=col)
    ax.view_init(elev=20, azim=frame * 0.5)

ani = FuncAnimation(fig, update, frames=np.arange(0, 200), interval=40)
plt.show()