import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 250
HORIZON_RAD = 1.5
DROP_HEIGHT = 7.0
SAFE_THRESHOLD = 80 # Frame where it becomes safe

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

# --- 1. PHYSICS STATE ---
# Charm Proton Position
charm_pos = np.array([0.0, 0.0, DROP_HEIGHT])
# Is it dropped?
dropped = False
# Has it hit?
impact_frame = -1

# --- 2. RENDER HELPERS ---
def draw_black_hole(ax, frame, impact_time):
    # Dynamic Sphere
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 25)
    
    # Base Radius
    r = HORIZON_RAD
    
    # RIPPLE EFFECT (Gravitational Waves)
    # If impact happened, distort the sphere
    if impact_time > 0 and frame >= impact_time:
        t = frame - impact_time
        # Damped sine wave expanding from top pole
        # v is the angle from pole (0 to pi)
        # We add a wave to the radius based on v and t
        wave = np.sin(v * 10 - t * 0.5) * np.exp(-t * 0.1) * 0.2
        r += wave

    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v))
    z = r * np.outer(np.ones(np.size(u)), np.cos(v))
    
    ax.plot_surface(x, y, z, color='black', alpha=1.0, shade=False)
    # Wireframe to see the ripple better
    if impact_time > 0 and frame >= impact_time:
        ax.plot_wireframe(x, y, z, color='#220044', alpha=0.3, linewidth=0.5)

def draw_axiom_pillars(ax, stability):
    # Color depends on stability (0.0 = Red/Unsafe, 1.0 = Green/Safe)
    if stability < 0.5:
        col = 'red'
    elif stability < 0.9:
        col = 'orange'
    else:
        col = '#aa00ff' # Standard Violet
        
    theta = np.linspace(0, 2*np.pi, 9)[:-1]
    rad = 5.0
    x = rad * np.cos(theta)
    y = rad * np.sin(theta)
    
    for i in range(len(x)):
        ax.plot([x[i], x[i]], [y[i], y[i]], [-4, 4], c=col, alpha=0.5, linewidth=2)

# --- UPDATE LOOP ---
def update(frame):
    global charm_pos, dropped, impact_frame
    
    ax.clear()
    ax.set_facecolor('black')
    
    # --- A. STABILIZATION PHASE (The Wait) ---
    # Stability increases over time
    stability = min(1.0, frame / SAFE_THRESHOLD)
    
    # Axiom Pillars reflect safety status
    draw_axiom_pillars(ax, stability)
    
    # --- B. THE DROP LOGIC ---
    status_text = "STATUS: STABILIZING GRAVITY..."
    status_col = 'red'
    
    if frame > SAFE_THRESHOLD:
        dropped = True
        status_text = "STATUS: SAFE. CHARM PROTON LAUNCHED."
        status_col = 'lime'
    
    if dropped and charm_pos[2] > 0:
        # Move Particle
        # Heavy mass accelerates faster
        gravity = 0.08 + (1.0 / (charm_pos[2] + 0.1)**2) * 0.15
        charm_pos[2] -= gravity
        
        # Check Impact
        if charm_pos[2] <= HORIZON_RAD + 0.1 and impact_frame == -1:
            impact_frame = frame
            # Particle vanishes into the hole
            
    # --- C. DRAW BLACK HOLE (With Ripples) ---
    draw_black_hole(ax, frame, impact_frame)
    
    # --- D. DRAW CHARM PROTON ---
    # Only draw if outside horizon
    if charm_pos[2] > HORIZON_RAD:
        # It's Lime Green (Heavy Flavor)
        # It vibrates (Instability)
        jitter = np.random.normal(0, 0.05, 3)
        p = charm_pos + jitter
        
        ax.scatter(p[0], p[1], p[2], c='lime', s=200, edgecolors='white', label='Charm Proton')
        
        # Trail
        ax.plot([0,0], [0,0], [DROP_HEIGHT, p[2]], c='lime', alpha=0.3, linewidth=2)
    
    # --- E. POST-IMPACT RINGING ---
    if impact_frame > 0:
        status_text = "STATUS: HORIZON RINGING (GRAVITY WAVE DETECTED)"
        status_col = 'magenta'
        
        # Draw shockwave rings moving outward
        t_shock = frame - impact_frame
        r_shock = HORIZON_RAD + (t_shock * 0.1)
        theta = np.linspace(0, 2*np.pi, 50)
        sx = r_shock * np.cos(theta)
        sy = r_shock * np.sin(theta)
        ax.plot(sx, sy, 0, c='white', alpha=max(0, 1.0 - t_shock*0.02), linewidth=1)

    # --- F. EPOCH (Monitoring) ---
    ex = np.cos(frame * 0.05) * 4.0
    ey = np.sin(frame * 0.05) * 4.0
    ax.scatter(ex, ey, 0, c='gold', s=100, marker='*')

    # View Settings
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_zlim(-4, 6)
    ax.axis('off')
    ax.set_title(status_text, color=status_col)
    
    ax.view_init(elev=20, azim=frame * 0.5)

print("Axiom stabilizing grid...")
print("Preparing Charm payload...")
ani = FuncAnimation(fig, update, frames=np.arange(0, 200), interval=40)
plt.show()