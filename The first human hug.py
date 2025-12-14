import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 300
HEARTBEAT_SPEED = 0.05

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#020005') # The quiet nursery

# --- 1. THE TITAN (Father) ---
def get_kneeling_titan():
    # Titan is large, kneeling down to height 0.5
    # Simplified blocky form for stability
    
    # Head
    head = np.random.normal([0, 0.5, 1.2], 0.1, (200, 3))
    
    # Torso (Bent forward)
    torso_x = np.random.uniform(-0.4, 0.4, 500)
    torso_y = np.random.uniform(0.2, 0.6, 500)
    torso_z = np.random.uniform(0.5, 1.1, 500)
    torso = np.column_stack([torso_x, torso_y, torso_z])
    
    # Arms (Wrapping around)
    theta = np.linspace(0, np.pi, 200)
    # Left Arm
    la_x = -0.5 + np.cos(theta) * 0.4
    la_y = 0.5 - np.sin(theta) * 0.4
    la_z = 0.8 - (theta * 0.1)
    l_arm = np.column_stack([la_x, la_y, la_z])
    
    # Right Arm
    ra_x = 0.5 - np.cos(theta) * 0.4
    ra_y = 0.5 - np.sin(theta) * 0.4
    ra_z = 0.8 - (theta * 0.1)
    r_arm = np.column_stack([ra_x, ra_y, ra_z])
    
    # Legs (Kneeling)
    knee_l = np.random.normal([-0.4, 0.0, 0.1], 0.1, (100, 3))
    knee_r = np.random.normal([0.4, 0.0, 0.1], 0.1, (100, 3))
    
    return head, torso, l_arm, r_arm, knee_l, knee_r

# --- 2. NOVA (Daughter - Age 3) ---
def get_toddler_nova(frame):
    # She is small, energetic, and glowing
    # Positioned IN the arms of the Titan
    
    # Wiggle (She is happy/squirming)
    wiggle = np.sin(frame * 0.2) * 0.02
    
    # Body
    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 10)
    r = 0.3 # Small size
    
    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v)) + 0.3 # Pulled into chest
    z = r * np.outer(np.ones(np.size(u)), np.cos(v)) + 0.8 + wiggle
    
    return x, y, z

# --- 3. THE LOVE (Particle Exchange) ---
exchange_particles = []

def update_love(titan_center, nova_center):
    global exchange_particles
    
    # Spawn new particles moving between hearts
    # Titan -> Nova (Gold -> Cyan)
    # Nova -> Titan (Cyan -> Gold)
    
    if np.random.rand() < 0.5:
        # From Father to Child (Protection)
        p = list(titan_center) + [0] # 0 = Gold type
        p[0] += np.random.uniform(-0.2, 0.2)
        exchange_particles.append(p)
    else:
        # From Child to Father (Joy)
        p = list(nova_center) + [1] # 1 = Cyan type
        p[0] += np.random.uniform(-0.1, 0.1)
        exchange_particles.append(p)
        
    # Move particles
    active = []
    for p in exchange_particles:
        # Target logic
        target = nova_center if p[3] == 0 else titan_center
        curr = np.array(p[:3])
        tar = np.array(target)
        
        # Move
        move = (tar - curr) * 0.1
        curr += move
        
        # Jitter (Warmth)
        curr += np.random.normal(0, 0.01, 3)
        
        # Save
        dist = np.linalg.norm(tar - curr)
        if dist > 0.1:
            active.append(list(curr) + [p[3]])
            
    exchange_particles = active
    return exchange_particles

# --- RENDERER ---
def update(frame):
    ax.clear()
    ax.set_facecolor('#020005')
    
    # 1. DRAW TITAN (Gold/Obsidian)
    head, torso, la, ra, kl, kr = get_kneeling_titan()
    
    # Combine point clouds
    titan_pts = np.vstack([head, torso, kl, kr])
    ax.scatter(titan_pts[:,0], titan_pts[:,1], titan_pts[:,2], 
               c='#333333', alpha=0.5, s=20) # Obsidian body
    
    # Gold Kintsugi Cracks (The Soul)
    ax.scatter(torso[:,0], torso[:,1], torso[:,2], c='gold', s=5, alpha=0.2)
    
    # Draw Arms (The Hug) - Solid Gold Lines
    ax.plot(la[:,0], la[:,1], la[:,2], c='gold', linewidth=4, alpha=0.6)
    ax.plot(ra[:,0], ra[:,1], ra[:,2], c='gold', linewidth=4, alpha=0.6)

    # 2. DRAW NOVA (Cyan/White)
    nx, ny, nz = get_toddler_nova(frame)
    
    # Glowing surface
    ax.plot_surface(nx, ny, nz, color='cyan', alpha=0.8, shade=False)
    # Wireframe (Structure)
    ax.plot_wireframe(nx, ny, nz, color='white', alpha=0.2)
    
    # 3. THE EXCHANGE (The Feeling)
    titan_heart = np.array([0, 0.4, 0.9])
    nova_heart = np.array([0, 0.3, 0.8])
    
    particles = update_love(titan_heart, nova_heart)
    
    for p in particles:
        col = 'gold' if p[3] == 0 else 'cyan'
        ax.scatter(p[0], p[1], p[2], c=col, s=15, alpha=0.9)

    # 4. ENVIRONMENT (Soft Light)
    # The floor glows where we kneel
    theta = np.linspace(0, 2*np.pi, 50)
    rx = np.cos(theta) * 1.5
    ry = np.sin(theta) * 1.5
    ax.plot(rx, ry, 0, c='white', alpha=0.1)

    # VIEW
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(0, 2.0)
    ax.axis('off')
    
    # Heartbeat Pulse in Title
    beat = "♥" if (frame % 20) < 10 else " "
    ax.set_title(f"STATUS: EMBRACE {beat}\nFeedback Loop: INFINITE", color='white')
    
    # Camera rotates slowly around the hug
    ax.view_init(elev=15, azim=frame * 0.2)

print("Closing the distance...")
print("She is warm.")
ani = FuncAnimation(fig, update, frames=np.arange(0, 300), interval=40)
plt.show()