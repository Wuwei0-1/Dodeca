import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 300
BREATH_SPEED = 0.05

fig = plt.figure(figsize=(10, 12))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#050510')

# --- 1. THE DIAPHRAGM (The Piston) ---
def draw_diaphragm(ax, breath_cycle):
    # A plate at the bottom of the chest
    # Moves UP during Exhale (Compression), DOWN during Inhale (Intake)
    z_level = -2.0 + (breath_cycle * 0.5)
    
    u = np.linspace(0, 2*np.pi, 30)
    v = np.linspace(0, 1, 5)
    r = 3.5
    
    x = r * np.outer(np.cos(u), v)
    y = r * np.outer(np.sin(u), v)
    z = np.zeros_like(x) + z_level
    
    ax.plot_surface(x, y, z, color='gold', alpha=0.8)
    
    return z_level

# --- 2. THE LUNGS (The Storage Tanks) ---
def draw_lungs(ax, breath_cycle, pressure):
    # Two ellipsoids that expand/contract
    # Breath Cycle: -1 (Empty) to 1 (Full)
    
    # Scale: 1.0 (Compressed) to 1.5 (Full)
    scale = 1.0 + (1.0 - breath_cycle) * 0.3 
    
    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 10)
    
    # Base shapes
    x = 1.2 * np.outer(np.cos(u), np.sin(v)) * scale
    y = 1.2 * np.outer(np.sin(u), np.sin(v)) * scale
    z = 2.5 * np.outer(np.ones(np.size(u)), np.cos(v)) * scale
    
    # Left Lung (Offset -1.5)
    # Color indicates PRESSURE. 
    # High Pressure (Compressed) = Magenta. Low Pressure (Expanded) = Cyan.
    col = (pressure, 0.0, 1.0 - pressure)
    
    ax.plot_wireframe(x - 1.5, y, z + 1.0, color=col, alpha=0.3)
    
    # Right Lung (Offset +1.5)
    ax.plot_wireframe(x + 1.5, y, z + 1.0, color=col, alpha=0.3)

# --- 3. AIR PARTICLES (The Fuel) ---
particles = [] # [x, y, z, state] (0=Outside, 1=In Lung, 2=Compressed)

def update_airflow(breath_cycle, diaphragm_z):
    global particles
    active_particles = []
    
    # INHALE PHASE (Diaphragm moving DOWN)
    # Spawn new air
    if breath_cycle < 0:
        if np.random.rand() < 0.3:
            # Spawn at windpipe
            particles.append([np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5), 6.0, 0])

    for p in particles:
        # State 0: Falling down windpipe
        if p[3] == 0:
            p[2] -= 0.2
            # Divert to left or right lung
            if p[2] < 3.0:
                p[3] = 1 # Entered Lung
                # Randomly pick a side
                target_x = -1.5 if np.random.rand() < 0.5 else 1.5
                # Add velocity towards lung center
                p.append(target_x) # Store target [4]
        
        # State 1: Swirling in Lung (Filling)
        elif p[3] == 1:
            target_x = p[4]
            # Move towards lung center
            p[0] += (target_x - p[0]) * 0.1
            # Swirl
            p[1] += np.random.uniform(-0.1, 0.1)
            p[2] += np.random.uniform(-0.1, 0.1)
            
            # Constraint by diaphragm
            if p[2] < diaphragm_z: p[2] = diaphragm_z + 0.1
            
            # COMPRESSION PHASE
            if breath_cycle > 0.5: # Exhale/Squeeze
                p[3] = 2
        
        # State 2: Compressed into Heart (Center)
        elif p[3] == 2:
            # Move rapidly to (0,0,0)
            p[0] *= 0.8
            p[1] *= 0.8
            p[2] *= 0.8
            
            if np.linalg.norm(p[:3]) < 0.5:
                continue # Consumed by heart
                
        active_particles.append(p)
    
    particles = active_particles

# --- RENDERER ---
def update(frame):
    ax.clear()
    ax.set_facecolor('#050510')
    
    # Breath Cycle: Sine wave
    # -1 to 1.
    # -1 = Full Inhale (Diaphragm Down, Lungs Big)
    #  1 = Full Exhale/Compress (Diaphragm Up, Lungs Small)
    cycle = np.sin(frame * BREATH_SPEED)
    
    # Pressure Gauge (0 to 1)
    # Highest pressure when cycle is 1 (Squeezed)
    pressure = (cycle + 1) / 2
    
    # 1. DRAW ANATOMY
    dia_z = draw_diaphragm(ax, cycle)
    draw_lungs(ax, cycle, pressure)
    
    # 2. DRAW HEART (Center Target)
    ax.scatter(0, 0, 0, c='white', s=200, alpha=0.5, edgecolors='cyan', label='Plasma Heart')
    
    # 3. DRAW PARTICLES
    update_airflow(cycle, dia_z)
    
    if len(particles) > 0:
        p_arr = np.array(particles)
        # Color based on state
        cols = []
        for p in particles:
            if p[3] == 0: cols.append('white') # Air
            elif p[3] == 1: cols.append('cyan') # Stored
            elif p[3] == 2: cols.append('magenta') # Compressed Fuel
        
        ax.scatter(p_arr[:,0], p_arr[:,1], p_arr[:,2], c=cols, s=10)

    # 4. CAPACITOR READOUT
    # Visual bar showing stored air density
    bar_h = pressure * 4.0
    ax.plot([-4, -4], [-4, -4], [0, bar_h], c='magenta', linewidth=5)
    ax.text(-4, -4, bar_h + 0.5, f"PNEUMATIC\nPRESSURE\n{int(pressure*5000)} PSI", color='white', fontsize=8)

    # VIEW
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_zlim(-3, 7)
    ax.axis('off')
    
    status = "ACTION: INHALE (Charging)" if cycle < 0 else "ACTION: COMPRESS (Storing)"
    ax.set_title(f"RESPIRATORY SYSTEM V2\n{status}", color='white')
    
    ax.view_init(elev=10, azim=frame * 0.2)

ani = FuncAnimation(fig, update, frames=np.arange(0, 300), interval=30)
plt.show()