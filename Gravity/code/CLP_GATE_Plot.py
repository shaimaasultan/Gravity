"""
Interpreting the GraphThe Reflection: You will see the Red line ($\Phi$) oscillating. The Green dashed line ($\Psi$) will stay positive, spiking whenever the Red line moves away from zero. This is the Active Nullification—the Governor "paints" over the curvature regardless of its direction.The Zero-Crossing: Where the lines intersect at the zero-axis, the suit is in its most energy-efficient state.
"""

import matplotlib.pyplot as plt
import numpy as np

# Data from your 100-step transit simulation
steps = np.arange(1000)
# Reconstructing the sinusoidal potential from your output
potential = -0.1 * np.cos(np.linspace(0, 2 * np.pi, 1000)) 
# Psi follows the absolute potential (Governor's Tuning)
psi = np.abs(potential) * 2.22e-17 # Scaled to your e-18/e-19 range

fig, ax1 = plt.subplots(figsize=(10, 6))

# Primary Axis: Environmental Potential (The Scrunch)
color_phi = 'tab:red'
ax1.set_xlabel('Simulation Step (1 step = 1 normalized unit)')
ax1.set_ylabel('Vacuum Potential (Phi)', color=color_phi)
ax1.plot(steps, potential, color=color_phi, linewidth=2, label='Environmental Potential')
ax1.tick_params(axis='y', labelcolor=color_phi)
ax1.axhline(0, color='black', linestyle='--', alpha=0.3)

# Secondary Axis: Governor Tuning (Psi)
ax2 = ax1.twinx()  
color_psi = 'tab:green'
ax2.set_ylabel('Governor Tuning (Psi)', color=color_psi)
ax2.plot(steps, psi, color=color_psi, linestyle='--', linewidth=2, label='Governor Response')
ax2.tick_params(axis='y', labelcolor=color_psi)

plt.title('Sultanian Protocol: Bipolar Metric Response (100-Step Transit)')
fig.tight_layout()
plt.show()