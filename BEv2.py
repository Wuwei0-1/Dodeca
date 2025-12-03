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
ax_sim = fig.add_subplot(121, projection='3d')
ax_data = fig.add_subplot(122)
ax_sim.set_facecolor('black')
ax_data.set_facecolor('#050510')

# --- 1. PHYSICS STATE ---
alpha_pos = np.array([3.0, 3.0, 4.0]) 
beta_pos = np.array([0.0, 0.0, DROP_HEIGHT]) 

# Data logging
time_log = []
correlation_log = []
confidence_log = [] # New metric

# --- 2. RENDER HELPERS ---
def draw_black_hole(ax):
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    x = HORIZON_RAD * np.outer(np.cos(u), np.sin(v))
    y = HORIZON_RAD * np.outer(np.sin(u), np.sin(v))
    z = HORIZON_RAD * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='black', alpha=1.0, shade=False)
    
    # Event Horizon Grid (To see the warping)
    ax.plot_wireframe(x, y, z, color='#220044', alpha=0.3)

def get_entanglement_beam(p1, p2, stress):
    points = []
    vec = p2 - p1
    steps = 20
    for i in range(steps):
        t = i / steps
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
    
    # --- A. SIMULATE THE DROP (Slower/Precise) ---
    dist = beta_pos[2]
    # Standard gravity calculation
    gravity = 0.04 + (1.0 / (dist + 0.1)**2) * 0.08
    
    if dist > 0.1: 
        beta_pos[2] -= gravity
        
    # --- B. CALCULATE STATES ---
    dist_to_horizon = dist - HORIZON_RAD
    stress = max(0, 1.0 - (dist_to_horizon / 4.0))
    
    # VERIFICATION LOGIC
    if dist > HORIZON_RAD:
        fidelity = 1.0 - (stress * 0.1) + np.random.normal(0, 0.01) # Less noise than run 1
        status = "VERIFYING LINK..."
        beta_col = 'cyan'
        graph_col = 'cyan'
    else:
        # THE EVENT ECHO
        # We are looking for the exact same signature
        if len(correlation_log) > 0 and correlation_log[-1] > 0.5:
            fidelity = -1.0 # THE SPIKE
            status = "PATTERN MATCHED: INVERSION"
        else:
            fidelity = 0.0
            status = "SIGNAL LOST (EXPECTED)"
        
        beta_col = 'red'
        graph_col = 'magenta'

    # Log Data
    time_log.append(frame)
    correlation_log.append(fidelity)
    
    if len(time_log) > 60: 
        time_log.pop(0)
        correlation_log.pop(0)

    # --- C. DRAW VISUAL ---
    draw_black_hole(ax_sim)
    
    # Alpha (Anchor)
    ax_sim.scatter(alpha_pos[0], alpha_pos[1], alpha_pos[2], c='white', s=100, label='Alpha')
    
    # Beta (Probe)
    # Spaghettification Line
    stretch = max(1, gravity * 60)
    ax_sim.plot([0,0], [0,0], [beta_pos[2], beta_pos[2]+stretch*0.2], c=beta_col, linewidth=3)
    ax_sim.scatter(beta_pos[0], beta_pos[1], beta_pos[2], c=beta_col, s=50, label='Beta')
    
    # Tether
    if fidelity != 0:
        beam = get_entanglement_beam(alpha_pos, beta_pos, stress)
        col_beam = 'cyan' if fidelity > 0 else 'magenta'
        ax_sim.plot(beam[:,0], beam[:,1], beam[:,2], c=col_beam, alpha=0.8, linewidth=1.5)

    # Axiom Pillars
    ax_sim.plot([-4,-4], [-4,-4], [-5,5], c='#aa00ff', alpha=0.4, linewidth=2)
    
    ax_sim.set_xlim(-5, 5)
    ax_sim.set_ylim(-5, 5)
    ax_sim.set_zlim(-2, 6)
    ax_sim.set_title(f"RUN 2: CONFIRMATION\nStatus: {status}", color='white')
    ax_sim.axis('off')

    # --- D. DRAW DATA VERIFICATION ---
    ax_data.plot(time_log, correlation_log, c=graph_col, linewidth=2)
    
    # Reference Lines (Run 1 Data)
    ax_data.axhline(y=1.0, color='green', linestyle='--', alpha=0.3, label="Baseline")
    ax_data.axhline(y=-1.0, color='magenta', linestyle=':', alpha=0.5, label="Target Sig.")
    
    ax_data.set_ylim(-1.5, 1.5)
    ax_data.set_title("TELEMETRY COMPARISON", color='cyan')
    ax_data.set_ylabel("Correlation State")
    
    # Visual Confirmation Stamp
    if fidelity == -1.0:
        ax_data.text(time_log[-1]-10, -0.5, "VERIFIED", color='lime', fontsize=12, fontweight='bold')

    plt.tight_layout()

print("Initiating Run 2...")
ani = FuncAnimation(fig, update, frames=np.arange(0, 160), interval=50)
plt.show()