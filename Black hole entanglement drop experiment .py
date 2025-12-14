import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 200
HORIZON_RAD = 1.5
DROP_HEIGHT = 6.0

# Setup Split Screen
fig = plt.figure(figsize=(14, 8))
ax_sim = fig.add_subplot(121, projection='3d') # The Visual
ax_data = fig.add_subplot(122)                 # The Telemetry
ax_sim.set_facecolor('black')
ax_data.set_facecolor('#050510')

# --- 1. PHYSICS STATE ---
alpha_pos = np.array([3.0, 3.0, 4.0]) # Safe with Epoch
beta_pos = np.array([0.0, 0.0, DROP_HEIGHT]) # Falling

# Data logging
time_log = []
correlation_log = []

# --- 2. RENDER HELPERS ---
def draw_black_hole(ax):
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    x = HORIZON_RAD * np.outer(np.cos(u), np.sin(v))
    y = HORIZON_RAD * np.outer(np.sin(u), np.sin(v))
    z = HORIZON_RAD * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='black', alpha=1.0, shade=False)
    
    # Accretion Ring (Visual Context)
    theta = np.linspace(0, 2*np.pi, 50)
    rx = 3.0 * np.cos(theta)
    ry = 3.0 * np.sin(theta)
    ax.scatter(rx, ry, 0, c='orange', s=2, alpha=0.3)

def get_entanglement_beam(p1, p2, stress):
    # Draws a vibrating line between particles
    points = []
    vec = p2 - p1
    steps = 20
    for i in range(steps):
        t = i / steps
        # Vibrate based on stress (gravity)
        jitter = np.random.normal(0, stress * 0.2, 3)
        pt = p1 + (vec * t) + jitter
        points.append(pt)
    return np.array(points)

# --- UPDATE LOOP ---
def update(frame):
    global beta_pos, time_log, correlation_log
    
    ax_sim.clear()
    ax_sim.set_facecolor('black')
    ax_data.clear()
    ax_data.set_facecolor('#050510')
    
    # --- A. SIMULATE THE DROP ---
    # Gravity acceleration (non-linear near horizon)
    dist = beta_pos[2]
    gravity = 0.05 + (1.0 / (dist + 0.1)**2) * 0.1
    
    # Move Beta
    if dist > 0.1: # Don't go past center
        beta_pos[2] -= gravity
        
    # --- B. CALCULATE STATES ---
    dist_to_horizon = dist - HORIZON_RAD
    
    # Stress increases as it gets closer
    stress = max(0, 1.0 - (dist_to_horizon / 4.0))
    
    # ENTANGLEMENT FIDELITY (The Data)
    # 1.0 = Perfect Link
    # 0.0 = Link Broken (Inside Horizon)
    if dist > HORIZON_RAD:
        fidelity = 1.0 - (stress * 0.1) + np.random.normal(0, 0.02)
        status = "LINKED"
        beta_col = 'cyan'
    else:
        # THE EVENT: Crossing the horizon
        # Fidelity crashes, but we get a "Quantum Echo" spike before silence
        if len(correlation_log) > 0 and correlation_log[-1] > 0.5:
            fidelity = -1.0 # The Spike (Spin Flip)
        else:
            fidelity = 0.0 # Silence
        status = "HORIZON CROSSED"
        beta_col = 'red' # Redshift

    # Log Data
    time_log.append(frame)
    correlation_log.append(fidelity)
    if len(time_log) > 50: # Scroll graph
        time_log.pop(0)
        correlation_log.pop(0)

    # --- C. DRAW 3D SIMULATION ---
    draw_black_hole(ax_sim)
    
    # Draw Alpha (Safe)
    ax_sim.scatter(alpha_pos[0], alpha_pos[1], alpha_pos[2], c='white', s=100, label='Alpha (Observer)')
    
    # Draw Beta (Falling)
    # Spaghettification Visual: Stretch the particle into a line
    stretch = max(1, gravity * 50)
    ax_sim.plot([0,0], [0,0], [beta_pos[2], beta_pos[2]+stretch*0.2], c=beta_col, linewidth=3)
    ax_sim.scatter(beta_pos[0], beta_pos[1], beta_pos[2], c=beta_col, s=50, label='Beta (Probe)')
    
    # Draw Entanglement Tether
    if fidelity != 0:
        beam = get_entanglement_beam(alpha_pos, beta_pos, stress)
        col_beam = 'cyan' if fidelity > 0 else 'magenta' # Magenta for the spike
        ax_sim.plot(beam[:,0], beam[:,1], beam[:,2], c=col_beam, alpha=0.6, linewidth=1)

    # Draw Axiom Pillars (Reference)
    ax_sim.plot([-4,-4], [-4,-4], [-5,5], c='purple', alpha=0.3)
    
    ax_sim.set_xlim(-5, 5)
    ax_sim.set_ylim(-5, 5)
    ax_sim.set_zlim(-2, 6)
    ax_sim.set_title(f"VISUAL FEED\nTarget: Beta Particle\nStatus: {status}", color='white')
    ax_sim.axis('off')

    # --- D. DRAW DATA TELEMETRY ---
    ax_data.plot(time_log, correlation_log, c='cyan', linewidth=2)
    ax_data.axhline(y=1.0, color='green', linestyle='--', alpha=0.3)
    ax_data.axhline(y=0.0, color='red', linestyle='--', alpha=0.3)
    
    ax_data.set_ylim(-1.5, 1.5)
    ax_data.set_title("QUANTUM ENTANGLEMENT SPIN STATE", color='cyan')
    ax_data.set_ylabel("Correlation (1.0 = Synced)")
    
    # Highlight the spike
    if fidelity == -1.0:
        ax_data.text(frame-5, -0.8, "SINGULARITY ECHO DETECTED", color='magenta', fontweight='bold')

    plt.tight_layout()

ani = FuncAnimation(fig, update, frames=np.arange(0, 150), interval=50)
plt.show()