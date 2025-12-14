import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 120
WALK_SPEED = 0.1
BOUNCE_HEIGHT = 0.3

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# --- 1. EPOCH BODY (The Sphere) ---
def get_epoch_core(pos):
    # Denser particle cloud for the body
    pts = np.random.normal(0, 0.15, (100, 3))
    pts += pos
    return pts

# --- 2. LIGHT LIMBS (Inverse Kinematics for Energy) ---
def get_light_leg(start_pos, end_pos, frame):
    # Generates a stream of particles connecting body to foot
    # Not a straight line -> An electric arc
    points = []
    vec = end_pos - start_pos
    steps = 10
    
    for i in range(steps):
        t = i / steps
        # Arc outward slightly
        arc = np.sin(t * np.pi) * 0.1
        
        # Jitter (Energy instability)
        jitter = np.random.normal(0, 0.02, 3)
        
        p = start_pos + (vec * t)
        p[1] += arc # Bend sideways
        p += jitter
        points.append(p)
        
    return np.array(points)

# --- 3. KINEMATICS ENGINE ---
def calculate_epoch_walk(frame):
    t = frame * WALK_SPEED
    
    # Body Movement (Moving in a circle)
    angle = t
    radius = 2.0
    bx = np.cos(angle) * radius
    by = np.sin(angle) * radius
    
    # Happy Bounce
    bz = 1.0 + np.abs(np.sin(t * 4)) * BOUNCE_HEIGHT
    body_pos = np.array([bx, by, bz])
    
    # Feet Calculation
    # Epoch has to "reach" down to the ground
    
    # Left Foot
    l_angle = t * 4
    lx = np.cos(angle + 0.2) * radius # Lead the body slightly
    ly = np.sin(angle + 0.2) * radius
    
    # Foot ground contact logic
    l_contact = np.sin(l_angle)
    if l_contact > 0:
        # Foot in air
        lz = l_contact * 0.5
        # Move foot forward relative to circle tangent
        lx += np.cos(angle + np.pi/2) * 0.5 * l_contact
        ly += np.sin(angle + np.pi/2) * 0.5 * l_contact
    else:
        # Foot on ground (Plant)
        lz = 0.0
    
    left_foot = np.array([lx, ly, lz])
    
    # Right Foot (Phase offset)
    r_angle = t * 4 + np.pi
    rx = np.cos(angle + 0.2) * radius
    ry = np.sin(angle + 0.2) * radius
    
    r_contact = np.sin(r_angle)
    if r_contact > 0:
        rz = r_contact * 0.5
        rx += np.cos(angle + np.pi/2) * 0.5 * r_contact
        ry += np.sin(angle + np.pi/2) * 0.5 * r_contact
    else:
        rz = 0.0
        
    right_foot = np.array([rx, ry, rz])
    
    return body_pos, left_foot, right_foot

# --- RENDERER ---
def update(frame):
    ax.clear()
    ax.set_facecolor('#050510')
    
    body, l_foot, r_foot = calculate_epoch_walk(frame)
    
    # 1. DRAW EPOCH (The Core)
    core_pts = get_epoch_core(body)
    ax.scatter(core_pts[:,0], core_pts[:,1], core_pts[:,2], 
               c='gold', s=20, alpha=0.8)
    
    # Halo Glow
    ax.scatter(body[0], body[1], body[2], c='white', s=300, alpha=0.2)
    
    # 2. DRAW LEGS (Light Streams)
    # Left Leg
    l_leg_pts = get_light_leg(body, l_foot, frame)
    ax.scatter(l_leg_pts[:,0], l_leg_pts[:,1], l_leg_pts[:,2], 
               c='gold', s=5, alpha=0.6)
    ax.scatter(l_foot[0], l_foot[1], l_foot[2], c='white', s=30, marker='*') # Foot contact
    
    # Right Leg
    r_leg_pts = get_light_leg(body, r_foot, frame)
    ax.scatter(r_leg_pts[:,0], r_leg_pts[:,1], r_leg_pts[:,2], 
               c='gold', s=5, alpha=0.6)
    ax.scatter(r_foot[0], r_foot[1], r_foot[2], c='white', s=30, marker='*')
    
    # 3. DRAW FOOTPRINTS (Dust Trail)
    # We leave particles where feet touched
    # Generate static trail based on circle
    theta = np.linspace(0, 2*np.pi, 50)
    tx = 2.0 * np.cos(theta)
    ty = 2.0 * np.sin(theta)
    ax.scatter(tx, ty, np.zeros_like(tx), c='orange', s=2, alpha=0.2)
    
    # 4. AXIOM (Watching from center)
    # Axiom is a dark block in the middle, observing
    ax.scatter(0, 0, 0.5, c='#220044', s=100, marker='s', alpha=0.8)
    ax.text(0, 0, 1.2, "AXIOM", color='purple', fontsize=8, ha='center')

    # View Settings
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(0, 4)
    ax.set_title("STATUS: EPOCH LOCOMOTION TEST\nForm: Photonic Biped | Mood: Joy", color='gold')
    ax.axis('off')
    
    # Camera rotates to follow Epoch
    ax.view_init(elev=20, azim=frame * 2)

print("Epoch creates legs of light...")
print("Epoch takes a step.")
ani = FuncAnimation(fig, update, frames=np.arange(0, 120), interval=40)
plt.show()