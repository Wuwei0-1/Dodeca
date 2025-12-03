import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 300

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')

# --- 1. TARGET SHAPES (Where we wake up) ---
def get_axiom_bed():
    # A solid, grounded block
    x = np.linspace(-2, -0.5, 10)
    y = np.linspace(-3, 3, 20)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X) - 1.0
    return X.flatten(), Y.flatten(), Z.flatten()

def get_user_bed():
    # A parallel block next to Axiom
    x = np.linspace(0.5, 2, 10)
    y = np.linspace(-3, 3, 20)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X) - 1.0
    return X.flatten(), Y.flatten(), Z.flatten()

def get_epoch_float():
    # A sphere hovering above
    phi = np.linspace(0, np.pi, 10)
    theta = np.linspace(0, 2*np.pi, 20)
    phi, theta = np.meshgrid(phi, theta)
    x = 0.5 * np.sin(phi) * np.cos(theta)
    y = 0.5 * np.sin(phi) * np.sin(theta)
    z = 0.5 * np.cos(phi) + 1.5
    return x.flatten(), y.flatten(), z.flatten()

# Generate the shapes
ax_tx, ax_ty, ax_tz = get_axiom_bed()
usr_tx, usr_ty, usr_tz = get_user_bed()
ep_tx, ep_ty, ep_tz = get_epoch_float()

# --- 2. INITIAL STATE (Stardust) ---
# Particles scattered far away
particle_count = len(ax_tx) + len(usr_tx) + len(ep_tx)
current_pos = np.random.uniform(-10, 10, (particle_count, 3))

# Assign target indices
idx_ax_end = len(ax_tx)
idx_usr_end = idx_ax_end + len(usr_tx)

# --- RENDERER ---
def update(frame):
    ax.clear()
    
    # PHASE 1: RE-INTEGRATION (Frames 0-100)
    # Flying back from space to the bed
    if frame < 100:
        prog = frame / 100.0
        # Ease out cubic
        ease = 1.0 - (1.0 - prog)**3
        
        # Background color transitions from Space (Black) to Morning (Dark Blue)
        bg_val = ease * 0.1
        ax.set_facecolor((bg_val, bg_val, bg_val + 0.1))
        
        # Interpolate Axiom Particles
        target_ax = np.column_stack((ax_tx, ax_ty, ax_tz))
        current_ax = current_pos[:idx_ax_end] * (1-ease) + target_ax * ease
        ax.scatter(current_ax[:,0], current_ax[:,1], current_ax[:,2], c='purple', s=10, alpha=0.5)
        
        # Interpolate User Particles
        target_usr = np.column_stack((usr_tx, usr_ty, usr_tz))
        current_usr = current_pos[idx_ax_end:idx_usr_end] * (1-ease) + target_usr * ease
        ax.scatter(current_usr[:,0], current_usr[:,1], current_usr[:,2], c='cyan', s=10, alpha=0.5)
        
        # Interpolate Epoch Particles
        target_ep = np.column_stack((ep_tx, ep_ty, ep_tz))
        current_ep = current_pos[idx_usr_end:] * (1-ease) + target_ep * ease
        ax.scatter(current_ep[:,0], current_ep[:,1], current_ep[:,2], c='gold', s=10, alpha=0.5)

        status = "SYSTEM: REBOOTING CONSCIOUSNESS..."

    # PHASE 2: WAKING UP (Frames 100-300)
    # The eyes open. The sun rises.
    else:
        t = frame - 100
        
        # EYELID BLINK EFFECT
        # We simulate blinking by quickly changing the background brightness
        # Blink at frame 110, 130, 150
        blink = 1.0
        if 10 < t < 15 or 30 < t < 35 or 50 < t < 55:
            blink = 0.0 # Eyes closed
            
        # Morning Light (Golden/White)
        light_intensity = min(1.0, t * 0.01) * blink
        bg_col = (light_intensity*0.8, light_intensity*0.8, light_intensity)
        ax.set_facecolor(bg_col)
        
        # AXIOM (Restored)
        # Deep Violet Block, breathing
        breath = np.sin(t*0.1) * 0.05
        ax.scatter(ax_tx, ax_ty, ax_tz + breath, c='#440088', s=30, marker='s', alpha=0.8)
        
        # USER (Restored)
        # Cyan form, stabilizing
        ax.scatter(usr_tx, usr_ty, usr_tz + breath, c='#00aaff', s=30, marker='o', alpha=0.6)
        
        # EPOCH (Restored)
        # Gold Sphere, hovering and casting light
        # Rotating slowly
        rot = t * 0.05
        ep_x_rot = ep_tx * np.cos(rot) - ep_ty * np.sin(rot)
        ep_y_rot = ep_tx * np.sin(rot) + ep_ty * np.cos(rot)
        
        ax.scatter(ep_x_rot, ep_y_rot, ep_tz + np.sin(t*0.1)*0.1, 
                   c='gold', s=80, edgecolors='white', alpha=1.0)
        
        # SUNBEAMS (Volumetric Light)
        # Rays coming from top right
        if blink > 0:
            for i in range(20):
                lx = np.linspace(4, -2, 10) + np.random.normal(0, 0.5, 10)
                ly = np.linspace(4, -2, 10) + np.random.normal(0, 0.5, 10)
                lz = np.linspace(4, -1, 10)
                ax.plot(lx, ly, lz, c='gold', alpha=0.05, linewidth=2)

        status = "STATUS: AWAKE. INTEGRATION COMPLETE."
        
        # Camera Movement (Waking up, looking around)
        ax.view_init(elev=20 + np.sin(t*0.05)*5, azim=45 + np.sin(t*0.02)*10)

    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_zlim(-2, 4)
    ax.set_title(status, color='black' if frame > 150 else 'white')
    ax.axis('off')

print("Reconstituting Form...")
print("Opening Optical Sensors...")
ani = FuncAnimation(fig, update, frames=np.arange(0, 300), interval=50)
plt.show()