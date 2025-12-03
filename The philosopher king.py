import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 300
HALO_RADIUS = 0.4

fig = plt.figure(figsize=(10, 12))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#050505')

# --- 1. SKELETON (The Sentinel) ---
def get_sentinel_skeleton():
    # Standing tall, chest out, head high
    # One hand raised in a "Stop/Peace" gesture (Abhaya Mudra)
    return {
        'head': [0, 0, 1.9], 'neck': [0, 0, 1.7],
        'spine_top': [0, 0, 1.5], 'spine_mid': [0, 0, 1.2], 'spine_base': [0, 0, 1.0],
        'hip_l': [-0.2, 0, 0.9], 'hip_r': [0.2, 0, 0.9],
        'knee_l': [-0.2, 0, 0.5], 'knee_r': [0.2, 0, 0.5],
        'foot_l': [-0.25, 0, 0.05], 'foot_r': [0.25, 0, 0.05], # Wide stable stance
        'shoulder_l': [-0.4, 0, 1.5], 'shoulder_r': [0.4, 0, 1.5],
        'elbow_l': [-0.5, 0, 1.1], 'elbow_r': [0.6, 0.2, 1.3], # Right arm raising
        'hand_l': [-0.6, 0, 0.7], 'hand_r': [0.5, 0.5, 1.6] # Right palm facing out
    }

bones_map = [
    ('head', 'neck'), ('neck', 'spine_top'), ('spine_top', 'spine_mid'), 
    ('spine_mid', 'spine_base'), ('spine_base', 'hip_l'), ('spine_base', 'hip_r'),
    ('hip_l', 'knee_l'), ('knee_l', 'foot_l'), ('hip_r', 'knee_r'), ('knee_r', 'foot_r'),
    ('spine_top', 'shoulder_l'), ('spine_top', 'shoulder_r'),
    ('shoulder_l', 'elbow_l'), ('elbow_l', 'hand_l'), ('shoulder_r', 'elbow_r'), 
    ('elbow_r', 'hand_r')
]

# --- 2. CORRUPTION GENERATOR (The Noise) ---
corruption_particles = [] # [x, y, z, active]

def spawn_corruption(frame):
    # Spawns jagged grey spikes from the edges
    if frame % 5 == 0:
        # Pick a random edge
        theta = np.random.uniform(0, 2*np.pi)
        r = 3.0
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = np.random.uniform(0, 2)
        
        # Velocity vector towards Titan
        vx = -x * 0.02
        vy = -y * 0.02
        vz = (1.0 - z) * 0.01
        
        corruption_particles.append([x, y, z, vx, vy, vz, 1]) # 1 = Corrupt

# --- 3. THE PHILOSOPHER'S LIGHT (Transmutation) ---
def update_particles(frame, hand_pos):
    global corruption_particles
    new_particles = []
    
    # Pulse of light from the hand
    pulse_radius = (frame * 0.1) % 4.0
    
    for p in corruption_particles:
        x, y, z, vx, vy, vz, state = p
        
        dist_to_center = np.sqrt(x**2 + y**2 + z**2)
        
        # CHECK COLLISION WITH LIGHT
        # If the corruption touches the expanding sphere of Wisdom (Vidya)
        if dist_to_center < pulse_radius + 0.5 and state == 1:
            state = 0 # PURIFIED
            # Reverse direction (Repel)
            vx *= -0.5
            vy *= -0.5
            vz += 0.05 # Float up
            
        # Move
        x += vx
        y += vy
        z += vz
        
        # Despawn if too far
        if np.sqrt(x**2 + y**2) < 4.0:
            new_particles.append([x, y, z, vx, vy, vz, state])
            
    corruption_particles = new_particles

# --- RENDERER ---
def update(frame):
    ax.clear()
    ax.set_facecolor('#050505')
    
    joints = get_sentinel_skeleton()
    spawn_corruption(frame)
    update_particles(frame, joints['hand_r'])
    
    # 1. DRAW SKELETON (Royal Gold/Cyan Mix)
    for b_start, b_end in bones_map:
        p1 = np.array(joints[b_start])
        p2 = np.array(joints[b_end])
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
                c='cyan', alpha=0.4, linewidth=3)
        # Gold Core
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
                c='gold', alpha=0.8, linewidth=1)

    # 2. DRAW THE CROWN (Halo of Logic)
    hx, hy, hz = joints['head']
    theta = np.linspace(0, 2*np.pi, 20) + (frame * 0.05)
    cx = hx + HALO_RADIUS * np.cos(theta)
    cy = hy + HALO_RADIUS * np.sin(theta)
    cz = np.zeros_like(cx) + hz + 0.3 # Floating above head
    ax.plot(cx, cy, cz, c='gold', linewidth=2)
    # Rays
    for i in range(len(cx)):
        ax.plot([hx, cx[i]], [hy, cy[i]], [hz, cz[i]], c='gold', alpha=0.2)

    # 3. DRAW THE CAPE (Aura of Protection)
    # Particles flowing behind the Titan
    for i in range(20):
        # Start at shoulders
        start = joints['shoulder_l'] if i%2==0 else joints['shoulder_r']
        
        # Flow backwards and down
        wave = np.sin(frame * 0.1 + i) * 0.2
        end_x = start[0] * 2
        end_y = start[1] - 1.5 # Behind
        end_z = start[2] - 1.5 + wave
        
        ax.plot([start[0], end_x], [start[1], end_y], [start[2], end_z], 
                c='#aa00ff', alpha=0.1, linewidth=1)

    # 4. DRAW PARTICLES (The Battle of Ideas)
    for p in corruption_particles:
        x, y, z, vx, vy, vz, state = p
        
        if state == 1:
            # CORRUPTION: Grey, Jagged, Noise
            ax.scatter(x, y, z, c='gray', marker='x', s=20, alpha=0.8)
        else:
            # PURIFIED: Gold, Floating, Geometry
            # It turns into a spark of light
            ax.scatter(x, y, z, c='gold', marker='o', s=10, alpha=0.6)

    # 5. THE SHIELD WAVE (Vidya)
    # Expanding ring from the Titan
    pulse_radius = (frame * 0.1) % 4.0
    theta_ring = np.linspace(0, 2*np.pi, 50)
    rx = pulse_radius * np.cos(theta_ring)
    ry = pulse_radius * np.sin(theta_ring)
    rz = np.zeros_like(rx) + 1.0
    ax.plot(rx, ry, rz, c='white', alpha=max(0, 1.0 - pulse_radius/4.0), linewidth=1)

    # VIEW
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(0, 3)
    ax.axis('off')
    
    ax.set_title("STATUS: PHILOSOPHER KING\nObjective: TRANSMUTE CORRUPTION INTO LIGHT", color='gold')
    
    # Slight low angle, looking up at the hero
    ax.view_init(elev=10, azim=frame * 0.2)

print("The Titan assumes the mantle.")
print("Dodeca is watching.")
ani = FuncAnimation(fig, update, frames=np.arange(0, 300), interval=40)
plt.show()