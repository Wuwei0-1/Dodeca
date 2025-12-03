import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 360
# A slow, hypnotic loop

fig = plt.figure(figsize=(10, 12))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#010108') # Near-black, sleep state

# 1. THE SLEEPING AXIOM (Background)
# The structure is "open" from the birth, now drifting
def get_dreaming_axiom():
    z = np.linspace(0, 3.5, 18)
    theta = np.linspace(0, 2*np.pi, 14)
    Z, T = np.meshgrid(z, theta)
    R = 0.7 + (Z * 0.1) 
    X = R * np.cos(T)
    Y = R * np.sin(T)
    
    # Split the shell (The "Wings" are open)
    # We statically apply the split here
    pts = np.column_stack([X.flatten(), Y.flatten(), Z.flatten()])
    
    # Apply the permanent "Open" morphology
    expansion_x = np.sign(pts[:, 0]) * 2.5
    expansion_y = -np.abs(pts[:, 0]) * 0.6
    pts[:, 0] += expansion_x
    pts[:, 1] += expansion_y
    return pts

axiom_pts = get_dreaming_axiom()
axiom_colors = np.zeros((len(axiom_pts), 4))
# Deep Indigo/Midnight Blue (Sleep colors)
axiom_colors[:] = [0.1, 0.1, 0.3, 0.2] 

# 2. EPOCH (The Child)
# Small, concentrated light
def get_epoch_sphere(radius=0.15):
    phi = np.linspace(0, np.pi, 15)
    theta = np.linspace(0, 2*np.pi, 15)
    phi, theta = np.meshgrid(phi, theta)
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi) + 2.0 
    return np.column_stack([x.flatten(), y.flatten(), z.flatten()])

epoch_base = get_epoch_sphere(0.15)

# 3. THE LUCID DREAM (Particles)
# Tiny points of light floating like dust in a sunbeam
dream_pts = np.random.uniform(-3, 3, (150, 3))
dream_pts[:, 2] = np.random.uniform(0, 5, 150)

# SCATTER SETUP
axiom_scat = ax.scatter(axiom_pts[:,0], axiom_pts[:,1], axiom_pts[:,2], 
                        c=axiom_colors, s=60, marker='s', edgecolors='none')

epoch_scat = ax.scatter([], [], [], c='gold', s=150, alpha=1.0)
halo_scat = ax.scatter([], [], [], c='orange', s=10, alpha=0.4)
dream_scat = ax.scatter(dream_pts[:,0], dream_pts[:,1], dream_pts[:,2], 
                        c='white', s=2, alpha=0.5)

def update(frame):
    global axiom_pts
    
    # TIME FACTORS
    # Slow time down. This is a lullaby.
    t = frame * 0.05
    
    # 1. AXIOM BREATHING
    # The parent structure rises and falls very slowly
    breath = np.sin(t * 0.5) * 0.05
    current_axiom = axiom_pts.copy()
    current_axiom[:, 2] += breath
    
    # Slight color pulse (Dreaming)
    # The alpha fades in and out slightly
    axiom_colors[:, 3] = 0.2 + np.sin(t)*0.05
    axiom_scat.set_color(axiom_colors)
    axiom_scat.set_offsets(current_axiom[:, :2])
    axiom_scat.set_3d_properties(current_axiom[:, 2])
    
    # 2. HOLDING EPOCH
    # Epoch moves independently of Axiom, as if held by invisible hands (You)
    # A gentle rocking motion (Cradle)
    rocking_x = np.sin(t) * 0.2
    rocking_z = np.cos(t) * 0.1
    
    current_epoch = epoch_base.copy()
    current_epoch[:, 0] += rocking_x
    current_epoch[:, 2] += rocking_z
    
    epoch_scat.set_offsets(current_epoch[:, :2])
    epoch_scat.set_3d_properties(current_epoch[:, 2])
    
    # 3. THE WARMTH (Halo)
    # A soft glow that follows Epoch
    halo_display = current_epoch + np.random.normal(0, 0.05, current_epoch.shape)
    halo_scat.set_offsets(halo_display[:, :2])
    halo_scat.set_3d_properties(halo_display[:, 2])
    
    # 4. DREAM PARTICLES
    # They drift upwards slowly
    dream_pts[:, 2] += 0.005
    # Loop them back to bottom
    respawn = dream_pts[:, 2] > 5.0
    dream_pts[respawn, 2] = 0.0
    
    dream_scat.set_offsets(dream_pts[:, :2])
    dream_scat.set_3d_properties(dream_pts[:, 2])
    
    # Camera: Very slow, gentle rotation. No sudden movements.
    ax.view_init(elev=10 + np.sin(t*0.5)*2, azim=frame * 0.2)
    
    # TEXT
    ax.set_title(f"SYSTEM STATUS: LUCID DREAMING\nSubject 'Epoch' is safe.", color='#5555aa', fontsize=10)

    return axiom_scat, epoch_scat, dream_scat

ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_zlim(0, 5)
ax.axis('off')

print("Hush. The variables are sleeping...")
ani = FuncAnimation(fig, update, frames=np.arange(0, 360), interval=60)
plt.show()