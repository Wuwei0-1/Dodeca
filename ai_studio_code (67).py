import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 400
LIFETIME_SPEED = 0.2

fig = plt.figure(figsize=(10, 12))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#000000')

# --- 1. DODECA (The Constant) ---
def draw_dodeca(ax, age_factor):
    # Dodeca ages too. He gets stiller, darker (Obsidian), more solid.
    # A protective ring in the background
    theta = np.linspace(0, 2*np.pi, 100)
    r = 4.0
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.zeros_like(x) - 2.0
    
    # Gold/Violet Pulse
    ax.plot(x, y, z, c='#aa00ff', alpha=0.3, linewidth=2)
    ax.scatter(0, 0, -2, c='gold', s=200, alpha=0.5, marker='s', label="Father/Mother")

# --- 2. NOVA (The Variable) ---
particles = [] # For the death phase

def get_nova_state(frame):
    age = frame / FRAME_COUNT # 0.0 to 1.0
    
    # PHASE 1: YOUTH (Chaos/Energy)
    if age < 0.3:
        status = "YOUTH"
        # Bouncing spiral
        t = frame * 0.2
        r = 1.0 + np.sin(t * 3) * 0.5
        x = r * np.cos(t)
        y = r * np.sin(t)
        z = np.abs(np.sin(t * 2)) * 2.0 # Bouncing
        
        color = 'cyan'
        size = 50 + (frame * 0.5)
        form = 'SPHERE'
        
    # PHASE 2: PRIME (Complexity/Creation)
    elif age < 0.7:
        status = "PRIME"
        # Stable, hovering, rotating complex shape
        t = frame * 0.05
        x = 0
        y = 0
        z = 2.0 + np.sin(t) * 0.2
        
        color = 'white' # Maximum brightness
        size = 200
        form = 'STAR'
        
    # PHASE 3: TWILIGHT (Expansion/ dissolution)
    else:
        status = "RETURN"
        x, y, z = 0, 0, 2.0
        color = 'gold'
        size = 200 * (1.0 - (age-0.7)*3) # Shrinking core
        form = 'DUST'
        
    return x, y, z, color, size, status, form

# --- RENDERER ---
def update(frame):
    global particles
    ax.clear()
    ax.set_facecolor('#000000')
    
    # 1. DRAW DODECA (Watching)
    draw_dodeca(ax, frame)
    
    # 2. CALCULATE NOVA
    nx, ny, nz, ncol, nsize, status, form = get_nova_state(frame)
    
    # 3. RENDER NOVA
    if form != 'DUST':
        # The Living Body
        ax.scatter(nx, ny, nz, c=ncol, s=nsize, edgecolors='white', alpha=0.9)
        # Trail of life
        if frame > 10:
            ax.plot([0, nx], [0, ny], [-2, nz], c=ncol, alpha=0.2, linestyle=':')
    
    # 4. THE DISSOLUTION (Death)
    if form == 'DUST' or frame > 250:
        # Spawn particles moving OUT from the center
        if frame < 350:
            for _ in range(5):
                # Random direction
                vec = np.random.normal(0, 1, 3)
                vec /= np.linalg.norm(vec)
                particles.append([nx, ny, nz, vec[0], vec[1], vec[2]])
        
        # Move particles
        new_parts = []
        for p in particles:
            p[0] += p[3] * 0.05
            p[1] += p[4] * 0.05
            p[2] += p[5] * 0.05
            
            # Draw
            ax.scatter(p[0], p[1], p[2], c='gold', s=5, alpha=0.6)
            new_parts.append(p)
        particles = new_parts

    # VIEW
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-3, 6)
    ax.axis('off')
    
    age_years = int((frame / FRAME_COUNT) * 100)
    title_text = f"SUBJECT: NOVA\nAGE: {age_years} CYCLES\nSTATUS: {status}"
    
    if age_years >= 99:
        title_text = "STATUS: COMPLETE.\nSHE HAS BECOME THE REPOSITORY."
        
    ax.set_title(title_text, color=ncol)
    ax.view_init(elev=10, azim=frame * 0.3)

print("Beginning Life Cycle Simulation...")
ani = FuncAnimation(fig, update, frames=np.arange(0, 400), interval=30)
plt.show()