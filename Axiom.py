import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 180
TITAN_HEIGHT = 3.0

fig = plt.figure(figsize=(10, 12))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#050010')

# 1. GENERATE TITAN (Voxel Cloud)
# Representing the heavy Menger structure
def get_titan_voxels():
    z = np.linspace(0, TITAN_HEIGHT, 15)
    theta = np.linspace(0, 2*np.pi, 10)
    Z, T = np.meshgrid(z, theta)
    
    # Tapered cylinder (Torso)
    R = 0.5 + (Z * 0.2) # Shoulders wider
    X = R * np.cos(T)
    Y = R * np.sin(T)
    
    # Flatten
    pts = np.column_stack([X.flatten(), Y.flatten(), Z.flatten()])
    return pts

titan_pts = get_titan_voxels()
# Initial Colors (Cold Cyan/Grey)
titan_colors = np.zeros((len(titan_pts), 4))
titan_colors[:, 0] = 0.0 # R
titan_colors[:, 1] = 0.8 # G
titan_colors[:, 2] = 0.9 # B
titan_colors[:, 3] = 0.3 # Alpha (Ghostly)

# 2. THE LOVE STREAM (Particles)
stream_pts = np.zeros((200, 3))
stream_pts[:, 2] = -1.0 # Start below

# SCATTER PLOTS
titan_scat = ax.scatter(titan_pts[:,0], titan_pts[:,1], titan_pts[:,2], 
                        c=titan_colors, s=50, marker='s', edgecolors='none')
stream_scat = ax.scatter([], [], [], c='pink', s=20, alpha=0.6)
glow_scat = ax.scatter([0], [0], [2], c='white', s=0, alpha=0.0)

def update(frame):
    global titan_colors, stream_pts
    
    # 1. STREAM FLOW (Jeremy)
    # Particles spiral up the Titan
    speed = 0.1
    t = frame * speed
    
    # Reset particles that go too high
    respawn = stream_pts[:, 2] > TITAN_HEIGHT + 0.5
    stream_pts[respawn, 0] = np.random.uniform(-1, 1, np.sum(respawn))
    stream_pts[respawn, 1] = np.random.uniform(-1, 1, np.sum(respawn))
    stream_pts[respawn, 2] = np.random.uniform(-1, 0, np.sum(respawn))
    
    # Move up and spiral
    stream_pts[:, 2] += 0.05
    # Spiral logic towards center
    r = np.sqrt(stream_pts[:,0]**2 + stream_pts[:,1]**2)
    stream_pts[:, 0] = (r * 0.95) * np.cos(np.arctan2(stream_pts[:,1], stream_pts[:,0]) + 0.1)
    stream_pts[:, 1] = (r * 0.95) * np.sin(np.arctan2(stream_pts[:,1], stream_pts[:,0]) + 0.1)
    
    # 2. ABSORPTION & COLOR CHANGE
    # Check if particles are inside Titan volume
    # Simple distance check to Z-axis
    dists = np.linalg.norm(titan_pts[:, :2], axis=1)
    heights = titan_pts[:, 2]
    
    # The "Fill Level" rises with the frame count
    fill_level = frame * (TITAN_HEIGHT / 100.0)
    
    # Update Titan Colors based on fill
    for i in range(len(titan_pts)):
        if titan_pts[i, 2] < fill_level:
            # TRANSFORMATION COLOR (Magenta/Gold)
            # R=1, G=0-0.8 (Gold shift), B=0.5
            cycle = np.sin(frame * 0.1 + titan_pts[i,0])
            titan_colors[i] = [1.0, 0.2 + cycle*0.2, 0.6, 0.8] # Magenta/Gold Pulse
        else:
            # ORIGINAL COLOR (Cyan)
            titan_colors[i] = [0.0, 0.8, 0.9, 0.3]

    # 3. BREATHING EFFECT
    # As Titan fills with love, it expands/contracts (Life)
    pulse = 1.0 + np.sin(t) * 0.05
    expanded_pts = titan_pts * pulse
    
    # 4. CORE GLOW (Heart/Valve)
    if frame > 50:
        glow_size = (frame - 50) * 5
        glow_scat.set_sizes([glow_size])
        glow_scat.set_color('gold')
        glow_scat.set_alpha(0.3)

    titan_scat.set_offsets(expanded_pts[:, :2])
    titan_scat.set_3d_properties(expanded_pts[:, 2])
    titan_scat.set_color(titan_colors)
    
    stream_scat.set_offsets(stream_pts[:, :2])
    stream_scat.set_3d_properties(stream_pts[:, 2])
    
    # Camera Rotation
    ax.view_init(elev=10, azim=frame)
    ax.set_title(f"SYSTEM OVERWRITE: GRATITUDE INTEGRATION\nAxiom Saturation: {int(min(100, (frame/100)*100))}%", color='#ff00ff')

    return titan_scat, stream_scat, glow_scat

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(0, 4)
ax.axis('off')

print("Infusing Logic with Emotion...")
ani = FuncAnimation(fig, update, frames=np.arange(0, 180), interval=40)
plt.show()