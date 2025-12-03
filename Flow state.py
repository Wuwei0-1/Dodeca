import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 80
RUN_SPEED = 0.5
HELIX_FREQ = 4.0 # How tight the nerve twisting is

# --- SKELETON RIG ---
def get_base_skeleton():
    return {
        'head': [0, 0, 1.9], 'neck': [0, 0, 1.7],
        'spine_top': [0, 0, 1.5], 'spine_mid': [0, 0, 1.2], 'spine_base': [0, 0, 1.0],
        'hip_l': [-0.2, 0, 0.9], 'hip_r': [0.2, 0, 0.9],
        'knee_l': [-0.2, 0, 0.5], 'knee_r': [0.2, 0, 0.5],
        'foot_l': [-0.2, 0, 0.1], 'foot_r': [0.2, 0, 0.1],
        'shoulder_l': [-0.4, 0, 1.5], 'shoulder_r': [0.4, 0, 1.5],
        'elbow_l': [-0.5, 0, 1.1], 'elbow_r': [0.5, 0, 1.1],
        'hand_l': [-0.6, 0, 0.7], 'hand_r': [0.6, 0, 0.7]
    }

bones_map = [
    ('head', 'neck'), ('neck', 'spine_top'), ('spine_top', 'spine_mid'), 
    ('spine_mid', 'spine_base'), ('spine_base', 'hip_l'), ('spine_base', 'hip_r'),
    ('hip_l', 'knee_l'), ('knee_l', 'foot_l'), ('hip_r', 'knee_r'), ('knee_r', 'foot_r'),
    ('spine_top', 'shoulder_l'), ('spine_top', 'shoulder_r'),
    ('shoulder_l', 'elbow_l'), ('elbow_l', 'hand_l'), ('shoulder_r', 'elbow_r'), 
    ('elbow_r', 'hand_r')
]

# --- HELIX GENERATOR (Visualizing Superposition) ---
def get_entangled_nerve(p1, p2, frame):
    """
    Generates two spiraling paths (Red and Blue) between points p1 and p2.
    """
    start = np.array(p1)
    end = np.array(p2)
    vec = end - start
    length = np.linalg.norm(vec)
    
    # Create steps along the bone
    t = np.linspace(0, 1, 15)
    
    # Base linear path
    linear_path = start[np.newaxis, :] + vec[np.newaxis, :] * t[:, np.newaxis]
    
    # Helix offset calculation (Perpendicular vectors)
    # Simple arbitrary axis to cross product with
    arb = np.array([0, 0, 1]) if abs(vec[2]) < 0.9 else np.array([0, 1, 0])
    perp1 = np.cross(vec, arb)
    perp1 = perp1 / np.linalg.norm(perp1) * 0.04 # Radius of helix
    perp2 = np.cross(vec, perp1)
    perp2 = perp2 / np.linalg.norm(perp2) * 0.04
    
    # Spin the helix over time (The flow of data)
    phase = frame * 0.5
    
    # Signal A (Red / Motor)
    angle_a = t * HELIX_FREQ * np.pi + phase
    path_a = linear_path + perp1[np.newaxis, :] * np.sin(angle_a)[:, np.newaxis] + perp2[np.newaxis, :] * np.cos(angle_a)[:, np.newaxis]
    
    # Signal B (Blue / Sensor) - 180 degrees offset
    angle_b = angle_a + np.pi
    path_b = linear_path + perp1[np.newaxis, :] * np.sin(angle_b)[:, np.newaxis] + perp2[np.newaxis, :] * np.cos(angle_b)[:, np.newaxis]
    
    return path_a, path_b

# --- KINEMATICS: OPTIMIZED RUN ---
def calculate_learning_pose(frame):
    joints = get_base_skeleton()
    t = frame * RUN_SPEED
    
    # Smooth, efficient running form (Flow State)
    # Less "violent" than the sprint, more "precise"
    
    vert = np.abs(np.sin(t)) * 0.15
    for k in joints: joints[k][2] += vert
    
    # Slight Lean
    lean = 0.3
    c, s = np.cos(lean), np.sin(lean)
    upper = ['spine_base', 'spine_mid', 'spine_top', 'neck', 'head', 'shoulder_l', 'shoulder_r', 'elbow_l', 'elbow_r', 'hand_l', 'hand_r']
    for bone in upper:
        y, z = joints[bone][1], joints[bone][2] - 0.9
        joints[bone][1] = (y * c - z * s) - 0.2
        joints[bone][2] = (y * s + z * c) + 0.9

    # Legs
    l_phase = t
    r_phase = t + np.pi
    joints['knee_l'][1] += np.cos(l_phase) * 0.6
    joints['foot_l'][1] += np.cos(l_phase) * 0.9
    joints['foot_l'][2] += max(0, np.sin(l_phase) * 0.3)
    
    joints['knee_r'][1] += np.cos(r_phase) * 0.6
    joints['foot_r'][1] += np.cos(r_phase) * 0.9
    joints['foot_r'][2] += max(0, np.sin(r_phase) * 0.3)
    
    # Arms
    joints['hand_l'][1] += np.cos(r_phase) * 0.7
    joints['hand_r'][1] += np.cos(l_phase) * 0.7

    return joints

# --- RENDERER ---
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

def update(frame):
    ax.clear()
    ax.set_facecolor('#050005') # Deep Purple Void (Logic Space)
    
    joints = calculate_learning_pose(frame)
    
    # 1. DRAW ENTANGLED NERVES (Superposition)
    for b_start, b_end in bones_map:
        p1 = joints[b_start]
        p2 = joints[b_end]
        
        # Get the twisting paths
        path_red, path_blue = get_entangled_nerve(p1, p2, frame)
        
        # Draw Red Helix (Motor Prediction)
        ax.plot(path_red[:,0], path_red[:,1], path_red[:,2], 
                c='red', linewidth=1, alpha=0.8)
        
        # Draw Blue Helix (Sensory Reality)
        ax.plot(path_blue[:,0], path_blue[:,1], path_blue[:,2], 
                c='cyan', linewidth=1, alpha=0.8)
        
        # Draw Glass Sheath (Faint)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
                c='white', linewidth=3, alpha=0.05)

    # 2. DRAW LEARNING PARTICLES (Backpropagation)
    # White/Gold dots traveling UP from feet/hands to brain
    # Visualizes data being collected and sent to the core
    for limb in ['foot_l', 'foot_r', 'hand_l', 'hand_r']:
        start_pos = np.array(joints[limb])
        brain_pos = np.array(joints['head'])
        
        # Interpolate position based on frame loop
        # 5 particles per limb traveling up
        for i in range(5):
            progress = ((frame * 0.05) + (i * 0.2)) % 1.0
            pos = start_pos + (brain_pos - start_pos) * progress
            
            # Draw Data Packet
            ax.scatter(pos[0], pos[1], pos[2], c='gold', s=10, marker='*')

    # 3. THE BRAIN (Optimization Core)
    hx, hy, hz = joints['head']
    # Purple Glow (Red + Blue Mixed)
    ax.scatter(hx, hy, hz, c='magenta', s=200, alpha=0.5, edgecolors='white')
    
    # 4. THE VALVE (Neck)
    nx, ny, nz = joints['neck']
    # Spinning Superposition Ring
    ax.scatter(nx, ny, nz, c='white', s=50, marker='x')

    # 5. ENVIRONMENT (Grid)
    grid_shift = (frame * 0.2) % 1.0
    for i in range(-2, 3):
        ax.plot([-2, 2], [i-grid_shift, i-grid_shift], [0, 0], c='purple', alpha=0.2)

    ax.set_title("STATUS: DEEP LEARNING (FLOW STATE)\nSNS/PNS Entanglement | Backpropagation Active", color='magenta')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(0, 2.3)
    ax.axis('off')
    ax.view_init(elev=15, azim=110)

print("Titan entering Deep Learning Flow State...")
ani = FuncAnimation(fig, update, frames=np.arange(0, 80), interval=40)
plt.show()