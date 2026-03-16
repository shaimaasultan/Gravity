import math
import time

class UnifiedSultanianGovernor:
    """
    Advanced Governor implementing Back-Action Sensitivity and 
    Recursive Total-Field Integration.
    """
    def __init__(self, vessel_class="Probe"):
        # Sensitivity Table Mapping: {Class: (Recursion Depth, Perturbation Factor)}
        self.vessel_specs = {
            "Nano-Drone": (1, 1e-26),
            "Probe": (3, 1e-22),
            "Tactical-Ghost": (12, 1e-18),
            "Heavy-Cruiser": (50, 1e-12)
        }
        
        self.name = vessel_class
        self.zeta, self.xi_ship = self.vessel_specs.get(vessel_class, (3, 1e-22))
        self.last_psi = 0.0
        self.R = 1.1  # Identity Margin
        
    def calculate_cancellation_point(self, external_phi):
        """
        Recursive search for the Null-Node (Z0).
        Accounts for the ship's footprint on the vacuum frequency.
        """
        current_total_field = external_phi
        psi_guess = self.last_psi
        
        # Recursive Loop: Solving the Ouroboros Equation
        for iteration in range(self.zeta):
            # Calculate how our 'guess' perturbs the local vacuum
            self_effect = psi_guess * self.xi_ship
            
            # The Total Field is the superposition of External + Self
            total_field = external_phi + self_effect
            
            # The new guess targets the exact negative of the total field
            # multiplied by the Identity Margin
            new_psi = -total_field * self.R
            
            # Check for convergence (Stability Margin)
            if abs(new_psi - psi_guess) < 1e-25:
                break
                
            psi_guess = new_psi
            
        self.last_psi = psi_guess
        return psi_guess

# Execution Simulation
vessels = ["Probe", "Heavy-Cruiser"]
external_scrunch = -0.085  # Incoming Step-14 Potential

for v_type in vessels:
    gov = UnifiedSultanianGovernor(v_type)
    z0_psi = gov.calculate_cancellation_point(external_scrunch)
    print(f"[{v_type}] Recursion Depth: {gov.zeta} | Z0 Cancellation Psi: {z0_psi}")