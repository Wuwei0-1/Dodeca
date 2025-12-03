import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 300
EARTH_RADIUS = 6.0

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

# --- 1. EARTH GENERATOR ---
def generate_earth():
    # Wireframe sphere
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    x = EARTH_RADIUS * np.outer(np.cos(u), np.sin(v))
    y = EARTH_RADIUS * np.outer(np.sin(u), np.sin(v))
    z = EARTH_RADIUS * np.outer(np.ones(np.size(u)), np.cos(v))
    return x, y, z

earth_x, earth_y, earth_z = generate_earth()

# --- 2. TRAIL GENERATORS ---
axiom_trail_x, axiom_trail_y, axiom_trail_z = [], [], []
epoch_trail_x, epoch_trail_y, epoch_trail_z = [], [], []

def update_trail(history_x, history_y, history_z, new_pos, length=20):
    history_x.append(new_pos[0])
    history_y.append(new_pos[1])
    history_z.append(new_pos[2])
    if len(history_x) > length:
        history_x.pop(0)
        history_y.pop(0)
        history_z.pop(0)
    return history_x, history_y, history_z

# --- RENDERER ---
# Global variables for accumulation
angle_axiom = 0.0
angle_epoch = 0.0
speed = 0.05

def update(frame):
    global angle_axiom, angle_epoch, speed, axiom_trail_x, axiom_trail_y, axiom_trail_z, epoch_trail_x, epoch_trail_y, epoch_trail_z
    
    ax.clear()
    ax.set_facecolor('black')
    
    # 1. ACCELERATION LOGIC
    # Linearly increase speed
    acceleration = 0.001
    speed += acceleration
    
    # Epoch goes slightly faster (The Catalyst)
    epoch_speed_mult = 1.0 + (frame * 0.002) 
    
    # 2. POSITION LOGIC (Orbiting Z-axis)
    angle_axiom += speed
    angle_epoch += speed * epoch_speed_mult
    
    # Axiom: Latitude 0 (Equator)
    ax_x = (EARTH_RADIUS + 0.5) * np.cos(angle_axiom)
    ax_y = (EARTH_RADIUS + 0.5) * np.sin(angle_axiom)
    ax_z = 0.5 # Slightly up
    
    # Epoch: Latitude 15 degrees (Running alongside)
    # Epoch height varies based on speed (Bouncing run -> Smooth flight)
    bounce = np.abs(np.sin(angle_epoch * 10)) * (1.0 - min(1.0, frame/200.0))
    ep_r = EARTH_RADIUS + 0.5 + bounce
    
    ep_x = ep_r * np.cos(angle_epoch)
    ep_y = ep_r * np.sin(angle_epoch)
    ep_z = 2.0 # Higher latitude
    
    # 3. DRAW EARTH (Spinning)
    # Rotate earth visually by rotating camera or grid
    # We'll just plot static grid for performance, the runners imply motion
    ax.plot_wireframe(earth_x, earth_y, earth_z, color='#002244', alpha=0.3, linewidth=0.5)
    
    # 4. DRAW AXIOM (The Heavy Runner)
    # Update Trail
    axiom_trail_x, axiom_trail_y, axiom_trail_z = update_trail(axiom_trail_x, axiom_trail_y, axiom_trail_z, [ax_x, ax_y, ax_z], length=30)
    
    # Plot Trail (Heavy Smoke)
    ax.plot(axiom_trail_x, axiom_trail_y, axiom_trail_z, c='#6600cc', linewidth=4, alpha=0.6)
    
    # Plot Body (Dense Cube)
    ax.scatter(ax_x, ax_y, ax_z, c='#aa00ff', s=150, marker='s', edgecolors='white', label='Axiom')
    
    # 5. DRAW EPOCH (The Accelerating Star)
    # Update Trail
    trail_len = 20 + int(frame * 0.5) # Trail gets longer as speed increases
    epoch_trail_x, epoch_trail_y, epoch_trail_z = update_trail(epoch_trail_x, epoch_trail_y, epoch_trail_z, [ep_x, ep_y, ep_z], length=trail_len)
    
    # DETERMINE STATE
    if frame < 200:
        # RUNNING STATE
        state_text = "EPOCH: ACCELERATING"
        col = 'gold'
        size = 100
        # Plot Trail
        ax.plot(epoch_trail_x, epoch_trail_y, epoch_trail_z, c='orange', linewidth=2, alpha=0.8)
        # Plot Body
        ax.scatter(ep_x, ep_y, ep_z, c='gold', s=size, marker='*', edgecolors='white', label='Epoch')
        
    else:
        # MAX OUTPUT STATE (Light Form)
        state_text = "EPOCH: MAX OUTPUT [PHOTONIC BREAKDOWN]"
        col = 'white'
        
        # In Max Output, Epoch becomes a solid ring of light
        ax.plot(epoch_trail_x, epoch_trail_y, epoch_trail_z, c='white', linewidth=6, alpha=1.0)
        ax.plot(epoch_trail_x, epoch_trail_y, epoch_trail_z, c='gold', linewidth=10, alpha=0.3) # Halo
        
        # Energy discharge (Sparks flying off tangent)
        for i in range(10):
            # Tangent vector calculation simplified
            tan_x = -np.sin(angle_epoch) + np.random.uniform(-0.2, 0.2)
            tan_y = np.cos(angle_epoch) + np.random.uniform(-0.2, 0.2)
            
            sx = ep_x + tan_x * 2.0
            sy = ep_y + tan_y * 2.0
            sz = ep_z + np.random.uniform(-1, 1)
            
            ax.plot([ep_x, sx], [ep_y, sy], [ep_z, sz], c='cyan', alpha=0.5, linewidth=1)

    # 6. SHOCKWAVES (Visualizing Speed)
    if frame > 100:
        # Rings appearing behind them
        theta = np.linspace(0, 2*np.pi, 20)
        r_shock = 1.0 + (frame % 10) * 0.2
        sx = ep_x + r_shock * np.cos(theta)
        sy = ep_y + r_shock * np.sin(theta)
        sz = np.zeros_like(sx) + ep_z
        ax.plot(sx, sy, sz, c='white', alpha=0.1)

    # VIEW SETTINGS
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-8, 8)
    ax.axis('off')
    
    # Camera rotates to follow the action
    ax.view_init(elev=30, azim=angle_axiom * 180 / np.pi - 45)
    
    status = f"VELOCITY: MACH {int(speed * 50)}\n{state_text}"
    ax.set_title(status, color='white')

print("Axiom sets the pace.")
print("Epoch breaks the sound barrier.")
ani = FuncAnimation(fig, update, frames=np.arange(0, 300), interval=30)
plt.show()