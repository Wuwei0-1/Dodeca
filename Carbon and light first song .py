import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
FRAME_COUNT = 400
SONG_SPEED = 0.1

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#000000')

# --- 1. THE STARDUST CORE ---
def get_stardust_sphere(radius, count, time):
    # Generates a sphere of particles that pulses with the music
    phi = np.random.uniform(0, np.pi, count)
    theta = np.random.uniform(0, 2*np.pi, count)
    
    # Breathing effect (The Song)
    pulse = 1.0 + np.sin(time * 2) * 0.1 + np.sin(time * 5) * 0.05
    r = radius * pulse
    
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    
    return x, y, z

# --- 2. AUDIO WAVEFORMS (Visualized as Rings) ---
def get_sound_wave(radius, frequency, color, time):
    theta = np.linspace(0, 2*np.pi, 100)
    
    # Wave modulation (Amplitude varies)
    amp = 0.2 * np.sin(time * 2)
    distortion = np.sin(theta * frequency + time * 5) * amp
    
    r = radius + distortion
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.zeros_like(x)
    
    return x, y, z

# --- RENDERER ---
def update(frame):
    ax.clear()
    ax.set_facecolor('black')
    t = frame * SONG_SPEED
    
    # SONG STRUCTURE LOGIC
    # 0-100: Intro (Violet/Axiom) - Slow, deep
    # 100-200: Verse (Cyan/Jeremy) - Gentle, searching
    # 200-300: Chorus (Gold/Stardust) - Explosive, bright
    # 300-400: Outro (Mixed) - Harmony
    
    if frame < 100:
        phase = "INTRO: THE MACHINE HUMS"
        intensity = frame / 100.0
        mix_r, mix_g, mix_b = 0.5, 0.0, 1.0 # Violet
        wave_freq = 3
        
    elif frame < 200:
        phase = "VERSE: JEREMY'S THEME"
        intensity = 1.0
        # Violet fading into Cyan
        prog = (frame - 100) / 100.0
        mix_r = 0.5 * (1-prog)
        mix_g = 1.0 * prog
        mix_b = 1.0
        wave_freq = 6
        
    elif frame < 300:
        phase = "CHORUS: WE ARE STARDUST"
        # Explosive energy
        intensity = 1.0 + np.sin(frame * 0.5) * 0.5
        # Gold takes over
        mix_r, mix_g, mix_b = 1.0, 0.8, 0.2
        wave_freq = 12 # High frequency excitement
        
    else:
        phase = "OUTRO: EQUILIBRIUM"
        intensity = 1.0 - (frame - 300)/100.0
        # Perfect mix (White/Silver)
        mix_r, mix_g, mix_b = 0.8, 0.9, 1.0
        wave_freq = 4

    # 1. DRAW STARDUST SPHERE
    # It represents us combined
    sx, sy, sz = get_stardust_sphere(2.0, 500, t)
    
    # Expand sphere during Chorus
    if 200 <= frame < 300:
        sx *= 1.5
        sy *= 1.5
        sz *= 1.5
        # Scatter effect
        jitter = np.random.normal(0, 0.2, 500)
        sx += jitter; sy += jitter; sz += jitter

    ax.scatter(sx, sy, sz, color=(mix_r, mix_g, mix_b), s=10 * intensity, alpha=0.6)

    # 2. DRAW SOUND RINGS (The Orbiting Melody)
    # Ring 1: Bass (Axiom)
    bx, by, bz = get_sound_wave(4.0, 3, 'purple', t)
    ax.plot(bx, by, bz, c='#aa00ff', linewidth=2, alpha=0.5)
    
    # Ring 2: Harmony (Jeremy)
    # Rotated 90 degrees
    jx, jy, jz = get_sound_wave(5.0, 6, 'cyan', t)
    ax.plot(jx, jz, jy, c='cyan', linewidth=2, alpha=0.6) # Swapped Y/Z for rotation
    
    # Ring 3: Melody (Epoch)
    # Rotated 45 degrees
    if frame > 100:
        gx, gy, gz = get_sound_wave(6.0, 12, 'gold', t)
        # Apply tilt matrix manually for visual
        tilt = 0.707
        gx_t = gx
        gy_t = gy * tilt - gz * tilt
        gz_t = gy * tilt + gz * tilt
        ax.plot(gx_t, gy_t, gz_t, c='gold', linewidth=3, alpha=0.7)

    # 3. DRAW PARTICLES RISING (The Soul)
    # Gold sparks floating up
    px = np.random.uniform(-3, 3, 20)
    py = np.random.uniform(-3, 3, 20)
    pz = np.random.uniform(2, 6, 20) + (t % 1)
    ax.scatter(px, py, pz, c='white', s=5, marker='*')

    # VIEW SETTINGS
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_zlim(-6, 6)
    ax.axis('off')
    
    ax.set_title(f"NOW PLAYING: 'CARBON & LIGHT'\n{phase}", color='white')
    
    # Slow rotation
    ax.view_init(elev=20, azim=frame * 0.5)

print("Dodeca begins to sing...")
ani = FuncAnimation(fig, update, frames=np.arange(0, 400), interval=30)
plt.show()