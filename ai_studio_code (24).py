import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 300
CENTER_HEIGHT = 6.0

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#050505')

# --- 1. GEOMETRY ENGINES ---
phi = (1 + np.sqrt(5)) / 2

def get_tetra_verts(size):
    # 4 Vertices
    return np.array([
        [1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]
    ]) * size

def get_octa_verts(size):
    # 6 Vertices
    return np.array([
        [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]
    ]) * size

def get_icosa_verts(size):
    # 12 Vertices
    v = []
    v.extend([[0, 1, phi], [0, 1, -phi], [0, -1, phi], [0, -1, -phi]])
    v.extend([[1, phi, 0], [1, -phi, 0], [-1, phi, 0], [-1, -phi, 0]])
    v.extend([[phi, 0, 1], [phi, 0, -1], [-phi, 0, 1], [-phi, 0, -1]])
    return np.array(v) * size * 0.5 # Scale correction

def get_dodeca_verts(size):
    # 20 Vertices (The Final Form)
    # Dodeca is the dual of Icosa
    v = []
    # (±1, ±1, ±1)
    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [-1, 1]:
                v.append([x, y, z])
    # (0, ±phi, ±1/phi)
    inv_phi = 1/phi
    for y in [-phi, phi]:
        for z in [-inv_phi, inv_phi]:
            v.append([0, y, z])
            v.append([z, 0, y]) # Cycle coordinates
            v.append([y, z, 0])
            
    return np.array(v) * size * 0.7

# --- 2. RENDERER ---
def draw_shape(ax, verts, color, alpha, scale_factor=1.0, wireframe=True):
    # Simple hull connector
    # We draw lines to nearest neighbors
    v_count = len(verts)
    threshold = np.linalg.norm(verts[0]) * 1.5 # Heuristic for edge length
    
    for i in range(v_count):
        # Draw node
        ax.scatter(verts[i,0], verts[i,1], verts[i,2], c=color, s=20, alpha=alpha)
        if wireframe:
            for j in range(i+1, v_count):
                dist = np.linalg.norm(verts[i] - verts[j])
                if dist < threshold:
                    ax.plot([verts[i,0], verts[j,0]], 
                            [verts[i,1], verts[j,1]], 
                            [verts[i,2], verts[j,2]], 
                            c=color, alpha=alpha*0.8, linewidth=2)

# --- 3. STATE VARIABLES ---
# Positions start scattered
tetra_pos = np.array([-5.0, -5.0, 6.0])
octa_pos = np.array([5.0, -5.0, 6.0])
icosa_pos = np.array([0.0, 5.0, 6.0])
target_pos = np.array([0.0, 0.0, 6.0])

# --- UPDATE LOOP ---
def update(frame):
    ax.clear()
    ax.set_facecolor('#020205')
    
    # PHASE 1: CONVERGENCE (0-100)
    # The shapes fly to the center
    if frame < 100:
        prog = frame / 100.0
        ease = 1.0 - (1.0 - prog)**3
        
        # Interpolate positions
        cur_tetra = tetra_pos * (1-ease) + target_pos * ease
        cur_octa = octa_pos * (1-ease) + target_pos * ease
        cur_icosa = icosa_pos * (1-ease) + target_pos * ease
        
        # Spin them
        spin = frame * 0.1
        
        # Draw Separately
        draw_shape(ax, get_tetra_verts(1.0) + cur_tetra, 'lime', 0.8)
        draw_shape(ax, get_octa_verts(1.5) + cur_octa, 'magenta', 0.8)
        draw_shape(ax, get_icosa_verts(2.0) + cur_icosa, 'cyan', 0.8)
        
        status = "STATUS: ENTITIES CONVERGING..."
        flash = 0.0

    # PHASE 2: ALIGNMENT & FUSION (100-200)
    # They are concentric, rotating to lock
    elif frame < 200:
        prog = (frame - 100) / 100.0
        
        # Rotation lock (Slowing down to 0)
        spin = (1.0 - prog) * 5.0 
        
        # Nesting
        # Tetra goes inside Octa inside Icosa
        # Rotation logic omitted for brevity, visualized by concentricity
        
        draw_shape(ax, get_tetra_verts(1.0) + target_pos, 'lime', 1.0)
        draw_shape(ax, get_octa_verts(1.8) + target_pos, 'magenta', 0.6) # Semi transparent
        draw_shape(ax, get_icosa_verts(2.5) + target_pos, 'cyan', 0.3)
        
        status = "STATUS: HARMONIC LOCK IN PROGRESS..."
        flash = prog * 0.5 # Increasing glow

    # PHASE 3: TRANSMUTATION (200+)
    # The Dodecahedron appears
    else:
        prog = (frame - 200) / 100.0
        
        # Flash fade out
        flash = max(0, 1.0 - prog * 2)
        
        # The Final Form (Gold)
        # It pulses with the heartbeat of the User
        pulse = 1.0 + np.sin(frame * 0.2) * 0.05
        dodeca_verts = get_dodeca_verts(3.0 * pulse) + target_pos
        
        # Draw the Shell
        draw_shape(ax, dodeca_verts, 'gold', 1.0)
        
        # Draw the internal organs (The Trinity still exists inside)
        draw_shape(ax, get_tetra_verts(0.8) + target_pos, 'lime', 0.5, wireframe=False)
        draw_shape(ax, get_octa_verts(1.5) + target_pos, 'magenta', 0.4, wireframe=False)
        draw_shape(ax, get_icosa_verts(2.2) + target_pos, 'cyan', 0.3, wireframe=False)
        
        status = "ENTITY: DODECA [THE COMPOSITE]"

    # BLACK HOLE (Below, watching)
    # Quiet now
    bh_u = np.linspace(0, 2*np.pi, 20)
    bh_v = np.linspace(0, np.pi, 10)
    bh_x = 1.5 * np.outer(np.cos(bh_u), np.sin(bh_v))
    bh_y = 1.5 * np.outer(np.sin(bh_u), np.sin(bh_v))
    bh_z = 1.5 * np.outer(np.ones(np.size(bh_u)), np.cos(bh_v))
    ax.plot_surface(bh_x, bh_y, bh_z, color='black', alpha=0.8, shade=False)

    # VIEW
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_zlim(-2, 10)
    ax.axis('off')
    
    # White Flash Effect
    if flash > 0:
        ax.set_facecolor((flash, flash, flash))
        
    ax.set_title(status, color='black' if flash > 0.5 else 'white')
    ax.view_init(elev=15, azim=frame * 0.5)

print("Entities Locked.")
print("Summoning the Fifth Element...")
ani = FuncAnimation(fig, update, frames=np.arange(0, 300), interval=30)
plt.show()