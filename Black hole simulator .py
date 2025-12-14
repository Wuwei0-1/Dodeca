import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 300
EVENT_HORIZON_RAD = 1.5
SAFE_ORBIT_RAD = 4.0 # Epoch stays here
CONTAINMENT_RAD = 5.0 # Axiom stands here

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#050005')

# --- 1. THE SPACETIME GRID (Warping) ---
def get_warped_grid(strength):
    # Create a meshgrid
    x = np.linspace(-8, 8, 30)
    y = np.linspace(-8, 8, 30)
    X, Y = np.meshgrid(x, y)
    
    # Calculate radius from center
    R = np.sqrt(X**2 + Y**2)
    
    # Warping Logic (Gravity Well)
    # As strength increases, Z drops into infinity near 0
    # We clamp it to avoid divide by zero visual glitches
    with np.errstate(divide='ignore'):
        Z = -strength / (R + 0.5) 
    
    # Flatten the center so it doesn't cover the black hole sphere
    Z[R < EVENT_HORIZON_RAD] = -10 
    
    return X, Y, Z

# --- 2. THE BLACK HOLE (The Void) ---
def get_event_horizon():
    # A perfect sphere
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    x = EVENT_HORIZON_RAD * np.outer(np.cos(u), np.sin(v))
    y = EVENT_HORIZON_RAD * np.outer(np.sin(u), np.sin(v))
    z = EVENT_HORIZON_RAD * np.outer(np.ones(np.size(u)), np.cos(v))
    return x, y, z

# --- 3. AXIOM CONTAINMENT FIELD ---
def get_axiom_pillars(frame):
    # 8 Pillars standing in a circle
    theta = np.linspace(0, 2*np.pi, 9)[:-1]
    
    # They rotate slowly to maintain the field
    spin = frame * 0.01
    
    x = CONTAINMENT_RAD * np.cos(theta + spin)
    y = CONTAINMENT_RAD * np.sin(theta + spin)
    z = np.zeros_like(x) # Mid-plane
    
    return x, y, z

# --- RENDERER ---
def update(frame):
    ax.clear()
    ax.set_facecolor('#020005') # Deep purple/black void
    
    # TIMING
    # 0-100: Gravity Well Forms (Safe)
    # 100-200: Event Horizon Manifests (Caution)
    # 200-300: Stable Orbit (Success)
    prog = min(1.0, frame / 150.0)
    
    # 1. DRAW SPACETIME GRID
    # The grid slowly sinks
    warp_strength = 5.0 * prog
    gx, gy, gz = get_warped_grid(warp_strength)
    
    # Color mapping based on depth (Blue -> Purple -> Black)
    ax.plot_wireframe(gx, gy, gz, color='#330066', alpha=0.3, linewidth=0.5)
    
    # 2. DRAW AXIOM (The Pillars)
    ax_x, ax_y, ax_z = get_axiom_pillars(frame)
    # Vertical lines for pillars
    for i in range(len(ax_x)):
        ax.plot([ax_x[i], ax_x[i]], [ax_y[i], ax_y[i]], [-5, 5], 
                c='#aa00ff', alpha=0.6, linewidth=2)
        # The node itself
        ax.scatter(ax_x[i], ax_y[i], 0, c='#aa00ff', s=100, marker='s', edgecolors='white')

    # Draw Containment Ring (Connecting pillars)
    # This represents the "Fence" preventing expansion
    theta_ring = np.linspace(0, 2*np.pi, 100)
    rx = CONTAINMENT_RAD * np.cos(theta_ring)
    ry = CONTAINMENT_RAD * np.sin(theta_ring)
    ax.plot(rx, ry, 0, c='#aa00ff', linestyle='--', alpha=0.4)

    # 3. DRAW THE EVENT HORIZON
    if prog > 0.5:
        # It fades in
        opacity = (prog - 0.5) * 2.0
        hx, hy, hz = get_event_horizon()
        # ABSOLUTE BLACK
        ax.plot_surface(hx, hy, hz, color='black', alpha=opacity, shade=False)
        
        # Accretion Disk (User Matter)
        # Cyan particles swirling into the void
        for i in range(50):
            # Spiral math
            angle = frame * 0.1 + (i * 0.5)
            dist = EVENT_HORIZON_RAD + 0.2 + (i * 0.05)
            dx = dist * np.cos(angle)
            dy = dist * np.sin(angle)
            ax.scatter(dx, dy, 0, c='cyan', s=5, alpha=opacity)

    # 4. DRAW EPOCH (The Lighthouse)
    # Epoch MUST stay at SAFE_ORBIT_RAD
    ep_angle = frame * 0.05
    ep_x = SAFE_ORBIT_RAD * np.cos(ep_angle)
    ep_y = SAFE_ORBIT_RAD * np.sin(ep_angle)
    ep_z = np.sin(frame * 0.05) * 1.0 # Slight bob
    
    # The Body
    ax.scatter(ep_x, ep_y, ep_z, c='gold', s=150, marker='*', edgecolors='white')
    
    # THE SAFETY TETHER
    # A beam of light connecting Epoch to the Axiom Pillars
    # This visually confirms Epoch is being held back from falling in
    # Find nearest pillar
    min_dist = 999
    nearest_idx = 0
    for i in range(len(ax_x)):
        d = np.sqrt((ep_x - ax_x[i])**2 + (ep_y - ax_y[i])**2)
        if d < min_dist:
            min_dist = d
            nearest_idx = i
            
    # Draw tether
    ax.plot([ep_x, ax_x[nearest_idx]], [ep_y, ax_y[nearest_idx]], [ep_z, 0], 
            c='gold', linestyle=':', alpha=0.5)

    # VIEW SETUP
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_zlim(-5, 5)
    ax.axis('off')
    
    # Status Text
    if prog < 0.5:
        status = "STATUS: COMPRESSING SPACE..."
        col = 'cyan'
    else:
        status = "STATUS: HORIZON STABLE. EPOCH SECURE."
        col = 'gold'
        
    ax.set_title(status, color=col)
    
    # Slow rotation
    ax.view_init(elev=30, azim=frame * 0.2)

print("Axiom establishes the perimeter.")
print("Gravity increasing...")
print("Horizon formed. Epoch is safe.")
ani = FuncAnimation(fig, update, frames=np.arange(0, 300), interval=40)
plt.show()