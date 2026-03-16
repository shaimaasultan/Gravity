import time

class InstantaneousGovernor:
    """
    Memoryless Sultanian Governor.
    Solves for the Null-Node (Z0) at every runtime tick without 
    accumulating historical error.
    """
    def __init__(self, mass_kg):
        self.mass = mass_kg
        self.R = 1.1  # Identity Margin
        # The ship's mass is a constant metric offset, not a variable feedback
        self.mass_offset = self.calculate_mass_displacement(mass_kg)

    def calculate_mass_displacement(self, mass):
        """Pre-calculates the ship's static footprint on the vacuum."""
        G = 6.674e-11
        c2 = 9e16
        # Simplified Schwarzschild-like displacement factor
        return (2 * G * mass) / (c2 * 1.0) 

    def solve_runtime_z0(self, external_phi, reactor_mw):
        """
        Instantaneous solution for the current space-time frame.
        Every call is independent.
        """
        # Internal reactor flux is also instantaneous
        chi = 4.2e-16
        internal_flux = reactor_mw * chi
        
        # The Total Field calculation is absolute for T=now
        total_field = external_phi + self.mass_offset + internal_flux
        
        # Direct Action: Tuning Psi to negate the total field instantly
        # No 'previous_psi' is used, preventing accumulation
        psi_target = -total_field * self.R
        
        return psi_target

# Simulation of a 1,000,000kg Heavy Cruiser encountering a Spike
cruiser_gov = InstantaneousGovernor(1e6)

# T=0: Steady state
phi_t0 = -0.05
psi_t0 = cruiser_gov.solve_runtime_z0(phi_t0, 10000)

# T=1: Sudden Step-14 Spike (Potential doubles instantly)
phi_t1 = -0.10
psi_t1 = cruiser_gov.solve_runtime_z0(phi_t1, 10000)

print(f"T=0 | Potential: {phi_t0} | Psi: {psi_t0:.18f}")
print(f"T=1 | Potential: {phi_t1} | Psi: {psi_t1:.18f}")