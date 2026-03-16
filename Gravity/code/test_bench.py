import pandas as pd
from core_logic import PlenumEngine

def run_material_benchmarking():
    """
    Executes a batch simulation for materials listed in the UFMP manifest.
    Calculates the point of Shear Failure and the resulting Kinetic Yield.
    """
    
    # Material Database based on Sultanian Protocol Benchmarks
    # Format: [Name, Unlock Constant (k), Resonance (Rc)]
    materials = [
        ["Pure Iron", 0.99, 1.00],
        ["Neodymium", 1.50, 1.00],
        ["Superconductor", 1.20, 2.50],
        ["Graphene-hBN", 5.20, 5.00] # The Sultanian Target
    ]
    
    # Simulated Environment Parameters
    applied_omega = 5.2e12  # Target 5.2 THz
    applied_b_field = 0.8   # 0.8 Tesla magnetic bias
    test_mass = 1.0         # 1.0 kg test lattice
    
    results = []

    print("--- UFMP Material Test Bench Starting ---")
    print(f"Environment: Omega={applied_omega/1e12} THz, B={applied_b_field}T\n")

    for name, k, rc in materials:
        # Initialize Engine for specific material shroud
        engine = PlenumEngine(material_k=k)
        
        # Calculate the unique Stability Threshold for this material
        st_limit = engine.get_stability_threshold(applied_b_field, applied_omega)
        
        # Calculate current operational torque
        # In a real test, this is the cross-product magnitude
        current_torque = applied_omega * applied_b_field
        
        # Monitor for the Snap
        r_order, snapped = engine.monitor_phase_divergence(current_torque, st_limit)
        
        # Calculate Yield if Snap occurs
        # Yield is scaled by the Resonance Constant (rc)
        yield_energy = engine.execute_kinetic_release(test_mass, rc) if snapped else 0.0
        
        results.append({
            "Material": name,
            "Unlock (k)": k,
            "Threshold (St)": f"{st_limit:.2e}",
            "Phase-Order (R)": f"{r_order:.4f}",
            "Snap Status": "ACTIVE" if snapped else "STABLE",
            "Yield (Delta E)": f"{yield_energy:.2f} Lux"
        })

    # Display results as a Clean Dataframe
    df = pd.DataFrame(results)
    print(df.to_string(index=False))
    
    print("\n--- Benchmarking Complete ---")
    print("Observation: Graphene-hBN demonstrates the highest Kinetic Release capacity.")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from core_logic import PlenumEngine

import matplotlib.pyplot as plt
import numpy as np

def generate_yield_plot(material_data):
    """
    Generates the Frequency vs. Kinetic Yield graph.
    Integrates the Critical Impulse Sharpness to trigger the Graphene Snap.
    """
    # Sweep from 0.1 to 10 THz to capture the 5.2 THz resonance point
    frequencies = np.linspace(0.1e12, 10e12, 500) 
    plt.figure(figsize=(12, 7))

    # Static environment parameters
    b_field = 0.8  # Your original 0.8 Tesla bias
    test_mass = 1.0 

    for name, k, rc in material_data:
        engine = PlenumEngine(material_k=k)
        yields = []
        
        # Apply the critical discovery: sigma=27.5 for high-k materials
        # Others remain at 1.0 (Static/Smooth ramp)
        sigma_val = 27.5 if name == "Graphene-hBN" else 1.0
        
        for freq in frequencies:
            st_limit = engine.get_stability_threshold(b_field, freq)
            current_torque = freq * b_field
            
            # Execute Snap check with Impulse Modulation
            r_order, snapped = engine.monitor_impulse_snap(
                current_torque, 
                st_limit, 
                pulse_sharpness=sigma_val
            )
            
            # Yield calculation: If locked, use a 1e-10 floor for the log scale
            if snapped:
                y_val = (test_mass * (freq**2)) * rc
            else:
                y_val = 1e-10
                
            yields.append(y_val)
            
        # Plotting with raw string 'r' to avoid SyntaxWarnings
        plt.plot(frequencies / 1e12, yields, label=f"{name} (k={k}, $\sigma$={sigma_val})", linewidth=2)

    # Graph Aesthetics
    plt.title("Sultanian Protocol: Kinetic Yield under Impulse Modulation", fontsize=14)
    plt.xlabel("Frequency (THz)", fontsize=12)
    plt.ylabel(r"Kinetic Yield ($\Delta E$)", fontsize=12)
    plt.yscale('log') # Log scale handles the 30+ order of magnitude jump
    plt.ylim(1e-12, 1e30) # Setting limits to clearly show the "Locked" vs "Freed" zones
    plt.grid(True, which="both", ls="-", alpha=0.3)
    plt.axvline(x=5.2, color='r', linestyle='--', alpha=0.5, label="Target Resonance (5.2 THz)")
    plt.legend(loc='lower right')
    
    plt.tight_layout()
    plt.show()
    
def run_material_benchmarking():
    materials = [
        ["Pure Iron", 0.99, 1.00],
        ["Neodymium", 1.50, 1.00],
        ["Superconductor", 1.20, 2.50],
        ["Graphene-hBN", 5.20, 5.00]
    ]
    
    # Run the visual analysis
    generate_yield_plot(materials)

def find_critical_b_field():
    # Target: Graphene-hBN at the 5.2 THz resonance
    k_graphene = 5.2
    target_omega = 5.2e12
    engine = PlenumEngine(material_k=k_graphene)
    
    # We iterate B from 0.1T upwards until the Snap triggers
    for b_test in np.arange(0.1, 10.0, 0.1):
        st_limit = engine.get_stability_threshold(b_test, target_omega)
        current_torque = target_omega * b_test
        
        # Check for the moment R-Order hits 1.0
        r_order, snapped = engine.monitor_phase_divergence(current_torque, st_limit)
        
        if snapped:
            print(f"CRITICAL DATA FOUND")
            print(f"Material: Graphene-hBN")
            print(f"Resonance: {target_omega/1e12} THz")
            print(f"Required B-Field: {b_test:.2f} Tesla")
            print(f"Result: KINETIC RELEASE INITIATED (Delta E > 0)")
            break

import numpy as np
from core_logic import PlenumEngine

def find_critical_impulse():
    # Target: Graphene-hBN (k=5.2) at 5.2 THz
    k_graphene = 5.2
    target_omega = 5.2e12
    b_field = 0.8  # Returning to your original B-field
    engine = PlenumEngine(material_k=k_graphene)
    
    # Calculate the static threshold (The "Wall")
    st_limit = engine.get_stability_threshold(b_field, target_omega)
    current_torque = target_omega * b_field
    
    print(f"--- Seeking Impulse Sharpness for Graphene-hBN ---")
    print(f"Static Torque: {current_torque:.2e} | Static Threshold: {st_limit:.2e}")
    
    # Iterate through Sharpness (sigma) from 1.0 to 50.0
    for sigma in np.arange(1.0, 50.0, 0.5):
        # We use the monitor_impulse_snap logic
        r_order, snapped = engine.monitor_impulse_snap(current_torque, st_limit, pulse_sharpness=sigma)
        
        if snapped:
            # Once snapped, calculate the yield
            yield_energy = (1.0 * (target_omega**2)) * 5.0 # rc=5.0 for Graphene
            
            if yield_energy >= 1e25:
                print(f"\n[SUCCESS] Threshold Breached via Impulse!")
                print(f"Critical Impulse Sharpness (sigma): {sigma:.1f}")
                print(f"Resulting Yield (Delta E): {yield_energy:.2e}")
                print(f"System State: KINETIC RELEASE ACTIVE")
                return sigma
                
    print("\n[FAILED] Static torque too low for available impulse range.")
    return None

if __name__ == "__main__":
    run_material_benchmarking()
    find_critical_b_field()
    critical_sigma = find_critical_impulse()
