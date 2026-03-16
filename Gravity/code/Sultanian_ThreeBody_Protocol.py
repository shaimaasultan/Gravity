import numpy as np
import time

class SultanianEngine:
    def __init__(self, material_k=5.2):
        # Universal Constants
        self.G_s = 6.67430e-11        # Vacuum Stiffness (Elastic Modulus)
        self.F_TARGET = 5.2e12        # 5.2 THz Resonance Key
        self.S_CONST = 1e-12          # Normalization factor for THz-scale interactions
        
        # Material State
        self.material_k = material_k  # Graphene-hBN = 5.2
        self.current_phi = 0.0

    def calculate_r_interference(self, distances, masses):
        """Calculates the lattice stress (R-order) from 3-body potentials."""
        # Phi_total = sum(G * M / r)
        self.current_phi = sum([(self.G_s * m) / d for m, d in zip(masses, distances)])
        
        # Sultanian R-Order Equation
        r_inter = (self.current_phi * self.material_k * self.S_CONST) / (self.F_TARGET * 1e-24)
        
        # Logic Gates
        snapped = r_inter > 1.0
        fracture = r_inter > 100.0
        return r_inter, snapped, fracture

    def apply_safety_governor(self, r_order):
        """Modulates k-factor to prevent Lattice Fracture."""
        if r_order > 1.5:
            # Shift phase to neutralize excess potential
            self.material_k *= (1.1 / r_order)
            return True
        return False

def run_simulation():
    # 1. Initialize Engine (Shaimaa's Graphene Shroud)
    engine = SultanianEngine(material_k=5.2)
    
    # 2. Define 3-Body System: [Star, Planet, Nearby Moon/Craft]
    masses = [1.98e30, 5.97e24, 7.34e22] 
    distances = [1.5e11, 3.8e8, 1.0e8] # Starting Distances (m)

    print("--- Sultanian Protocol: 3-Body Resonance Simulation ---")
    print(f"Target Frequency: 5.2 THz | Initial k: {engine.material_k}\n")

    # 3. Execution Loop (Simulating a descent into the 'Scrunch')
    for step in range(8):
        r_val, is_snapped, is_fractured = engine.calculate_r_interference(distances, masses)
        
        # Check Safety Governor
        governed = engine.apply_safety_governor(r_val)
        
        status = "STABLE"
        if is_snapped: status = "SNAP ACTIVE (GLIDE)"
        if is_fractured: status = "LATTICE FRACTURE DETECTED"
        if governed: status += " [GOVERNOR ACTIVE]"

        print(f"STEP {step} | Dist to Star: {distances[0]:.2e}m")
        print(f"  R-Order: {r_val:.4f} | Status: {status}")
        print(f"  Current k-factor: {engine.material_k:.4f}")
        print("-" * 50)

        # Move bodies 50% closer each step to simulate high-G approach
        distances = [d * 0.5 for d in distances]
        time.sleep(0.1)

if __name__ == "__main__":
    run_simulation()