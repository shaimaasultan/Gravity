
from UnifiedSultanianGovernor import UnifiedSultanianGovernor
class ReactorSyncGovernor(UnifiedSultanianGovernor):
    """
    Enhanced Governor with Reactor-Sync for Predictive Neutralization.
    """
    def __init__(self, vessel_class="Heavy-Cruiser"):
        super().__init__(vessel_class)
        self.chi_constant = 4.2e-16 # Flux-Coupling Constant
        
    def calculate_z0_with_sync(self, external_phi, reactor_output_mw):
        """
        Calculates the Cancellation Point by predicting the reactor's
        own effect on the local vacuum.
        """
        # Predictive Term: χ(ΔP)
        # We calculate the internal 'Scrunch' caused by the reactor
        internal_flux = reactor_output_mw * self.chi_constant
        
        # Pass the combined field into the recursive loop
        # The Governor now treats the engine as part of the environment
        total_environmental_phi = external_phi + internal_flux
        
        return self.calculate_cancellation_point(total_environmental_phi)

# Simulation: Reactor Spike during Step-14 Transit
gov = ReactorSyncGovernor("Heavy-Cruiser")
ext_phi = -0.095
reactor_surge = 50000  # 50,000 MW surge for maneuvers

z0_synced = gov.calculate_z0_with_sync(ext_phi, reactor_surge)
print(f"Reactor-Synced Z0: {z0_synced:.18f}")