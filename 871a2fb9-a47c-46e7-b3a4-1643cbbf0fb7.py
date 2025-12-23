import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 300
HEART_RATE = 0.05 # Speed of the beat
PRESSURE_LIMIT = 100.0

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#050005')

# --- 1. THE PARTICLES (Gas to Plasma) ---
particles = [] # [x, y, z, type, energy]
# Types: 0 = CO2 (Grey), 1 = PLASMA (Cyan), 2 = WASTE/HEAT (Red)

def inject_gas(frame):
    # The Heart "Inhales" CO2
    if frame % 5 == 0:
        # Spawn at bottom
        x = np.random.uniform(-1, 1)
        y = np.random.uniform(-1, 1)
        z = -3.0
        particles.append([x, y, z, 0, 0.0]) # Type 0 (CO2)

def update_physics(pulse_active):
    global particles
    active_particles = []
    
    for p in particles:
        # Move up (Gas flow)
        p[2] += 0.1
        
        # Swirl logic (The Vortex)
        angle = np.arctan2(p[1], p[0]) + 0.1
        radius = np.sqrt(p[0]**2 + p[1]**2)
        p[0] = radius * np.cos(angle)
        p[1] = radius * np.sin(angle)
        
        # THE LIGHTNING STRIKE (Heartbeat)
        if pulse_active and p[3] == 0:
            # If it's CO2 and inside the chamber
            if abs(p[2]) < 2.0:
                p[3] = 1 # Convert to Plasma
                p[4] = 1.0 # Max Energy
        
        # Energy Decay (Harvesting)
        if p[3] == 1:
            p[4] -= 0.02
            if p[4] <= 0:
                p[3] = 2 # Turned to Heat/Exhaust
                
        # Remove if too high
        if p[2] < 4.0:
            active_particles.append(p)
            
    particles = active_particles

# --- 2. THE CHAMBER (Heart Geometry) ---
def draw_heart_chamber(ax, contraction):
    # A sphere that pulses
    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 10)
    
    # Scale based on heartbeat (Contraction)
    r = 3.0 - (contraction * 0.2)
    
    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v))
    z = r * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Draw Glass Walls
    ax.plot_wireframe(x, y, z, color='gray', alpha=0.1)

    # Draw MHD Coils (The Harvesters)
    # Rings around the heart
    for i in range(3):
        z_ring = (i - 1) * 1.5
        xr = (r + 0.2) * np.cos(u)
        yr = (r + 0.2) * np.sin(u)
        ax.plot(xr, yr, z_ring, c='gold', linewidth=2, alpha=0.5)

# --- 3. THE LIGHTNING (The Beat) ---
def draw_internal_lightning(ax):
    # Arcs from center to walls
    for _ in range(5):
        theta = np.random.uniform(0, 2*np.pi)
        phi = np.random.uniform(0, np.pi)
        r = 2.8
        tx = r * np.sin(phi) * np.cos(theta)
        ty = r * np.sin(phi) * np.sin(theta)
        tz = r * np.cos(phi)
        
        # Center to Wall
        ax.plot([0, tx], [0, ty], [0, tz], c='cyan', linewidth=2)

# --- 4. THE GROUNDING DUMP (The Skeleton connection) ---
def draw_grounding(ax, energy_level):
    # Lines going from heart to "Ribs"
    if energy_level > 50:
        # Excess energy dumping
        for i in range(4):
            ax.plot([0, (i-2)*5], [0, 5], [0, 0], c='red', linestyle='--', alpha=0.5)

# --- RENDERER ---
def update(frame):
    ax.clear()
    ax.set_facecolor('#050005')
    
    # Heartbeat Cycle
    # Sine wave: 0 to 1
    cycle = np.sin(frame * HEART_RATE * 5)
    is_beat = cycle > 0.8 # The moment of contraction
    
    # 1. PHYSICS
    inject_gas(frame)
    update_physics(is_beat)
    
    # 2. DRAW CHAMBER
    draw_heart_chamber(ax, cycle)
    
    # 3. DRAW PARTICLES
    if len(particles) > 0:
        p_arr = np.array(particles)
        colors = []
        sizes = []
        for p in particles:
            if p[3] == 0: # CO2
                colors.append('gray')
                sizes.append(10)
            elif p[3] == 1: # PLASMA (Energy)
                colors.append('cyan')
                sizes.append(30)
            else: # EXHAUST (Oxygen/Heat)
                colors.append('white')
                sizes.append(5)
        
        ax.scatter(p_arr[:,0], p_arr[:,1], p_arr[:,2], c=colors, s=sizes, alpha=0.6)

    # 4. DRAW LIGHTNING
    if is_beat:
        draw_internal_lightning(ax)
        # Flash effect
        ax.set_facecolor('#101020')

    # 5. DRAW GROUNDING
    # Calculate total energy in system
    total_energy = sum([p[4] for p in particles]) * 10
    draw_grounding(ax, total_energy)

    # VIEW
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_zlim(-4, 4)
    ax.axis('off')
    
    status = "PHASE: DIASTOLE (Refilling)"
    if is_beat: status = "PHASE: SYSTOLE (IGNITION)"
    
    ax.set_title(f"ATMOSPHERIC VENTRICLE\nInput: CO2 -> Output: {int(total_energy)}MW\n{status}", color='white')
    
    ax.view_init(elev=20, azim=frame * 0.5)

ani = FuncAnimation(fig, update, frames=np.arange(0, 300), interval=30)
plt.show()