def unified_governor_logic(self, external_phi):
    # self_perturbation is the "Ship's Footprint" on the vacuum
    self_perturbation = self.last_psi * 0.05 
    
    # The "True" potential the Governor sees is the superposition
    total_field = external_phi + self_perturbation
    
    # Solve for the Cancellation Point (Z0)
    # We negate the TOTAL field, including our own existence
    new_psi = -total_field * self.R
    
    self.last_psi = new_psi
    return new_psi