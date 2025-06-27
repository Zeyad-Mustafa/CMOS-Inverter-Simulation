#!/usr/bin/env python3
"""
Basic Demo: CMOS Inverter Simulation Examples
This file demonstrates various usage scenarios of the CMOS inverter simulation
"""

import sys
import os
# Add parent directory to path to import the main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cmos_inverter_simulation import CMOSInverter
import numpy as np
import matplotlib.pyplot as plt

def basic_vtc_demo():
    """Demonstrate basic VTC plotting"""
    print("=" * 50)
    print("BASIC VTC DEMONSTRATION")
    print("=" * 50)
    
    # Create a standard 5V CMOS inverter
    inverter = CMOSInverter(Vdd=5.0, Vtn=1.0, Vtp=-1.0)
    
    # Generate and plot VTC
    inverter.plot_vtc()
    
    # Print summary
    inverter.print_summary()

def technology_comparison():
    """Compare different technology nodes"""
    print("=" * 50)
    print("TECHNOLOGY NODE COMPARISON")
    print("=" * 50)
    
    # Define different technology parameters
    technologies = {
        '5V Technology': {'Vdd': 5.0, 'Vtn': 1.0, 'Vtp': -1.0, 'color': 'blue'},
        '3.3V Technology': {'Vdd': 3.3, 'Vtn': 0.7, 'Vtp': -0.7, 'color': 'red'},
        '1.8V Technology': {'Vdd': 1.8, 'Vtn': 0.4, 'Vtp': -0.4, 'color': 'green'},
    }
    
    plt.figure(figsize=(12, 8))
    
    for i, (tech_name, params) in enumerate(technologies.items()):
        # Create inverter
        inverter = CMOSInverter(
            Vdd=params['Vdd'], 
            Vtn=params['Vtn'], 
            Vtp=params['Vtp']
        )
        
        # Generate VTC
        vin, vout = inverter.generate_vtc()
        
        # Plot in subplot
        plt.subplot(2, 2, i+1)
        plt.plot(vin, vout, color=params['color'], linewidth=2.5, label=tech_name)
        plt.plot([0, params['Vdd']], [params['Vdd'], 0], 'k--', alpha=0.3, label='Ideal')
        plt.xlabel('Input Voltage (V)')
        plt.ylabel('Output Voltage (V)')
        plt.title(f'{tech_name} - VTC')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xlim(0, params['Vdd'])
        plt.ylim(0, params['Vdd'])
        
        # Print switching threshold
        print(f"{tech_name}: Vm = {inverter.Vm:.2f}V")
    
    # Combined comparison
    plt.subplot(2, 2, 4)
    for tech_name, params in technologies.items():
        inverter = CMOSInverter(
            Vdd=params['Vdd'], 
            Vtn=params['Vtn'], 
            Vtp=params['Vtp']
        )
        vin, vout = inverter.generate_vtc()
        
        # Normalize to 0-1 scale for comparison
        vin_norm = vin / params['Vdd']
        vout_norm = vout / params['Vdd']
        
        plt.plot(vin_norm, vout_norm, color=params['color'], 
                linewidth=2.5, label=tech_name)
    
    plt.xlabel('Normalized Input Voltage')
    plt.ylabel('Normalized Output Voltage')
    plt.title('Normalized Comparison')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    
    plt.tight_layout()
    plt.show()

def parameter_sensitivity_analysis():
    """Analyze sensitivity to parameter variations"""
    print("=" * 50)
    print("PARAMETER SENSITIVITY ANALYSIS")
    print("=" * 50)
    
    base_inverter = CMOSInverter(Vdd=5.0, Vtn=1.0, Vtp=-1.0)
    
    # Threshold voltage variations
    print("\n1. Threshold Voltage Sensitivity:")
    vtn_values = [0.8, 1.0, 1.2]  # ±20% variation
    base_inverter.parameter_sweep('Vtn', vtn_values)
    
    # Supply voltage variations
    print("\n2. Supply Voltage Sensitivity:")
    vdd_values = [4.5, 5.0, 5.5]  # ±10% variation
    base_inverter.parameter_sweep('Vdd', vdd_values)
    
    # Beta ratio analysis
    print("\n3. Beta Ratio Analysis:")
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    beta_ratios = [0.5, 1.0, 2.0, 4.0]  # βp/βn ratios
    colors = ['blue', 'green', 'red', 'purple']
    
    for i, ratio in enumerate(beta_ratios):
        inverter = CMOSInverter(
            Vdd=5.0, Vtn=1.0, Vtp=-1.0,
            beta_n=100e-6, beta_p=ratio*100e-6
        )
        vin, vout = inverter.generate_vtc()
        
        # Plot VTC
        axes[0, 0].plot(vin, vout, color=colors[i], linewidth=2, 
                       label=f'βp/βn = {ratio}')
        
        # Plot switching threshold vs ratio
        axes[0, 1].scatter(ratio, inverter.Vm, color=colors[i], s=100)
        
        # Plot noise margins
        axes[1, 0].bar([f'NML\n(β={ratio})', f'NMH\n(β={ratio})'], 
                      [inverter.NML, inverter.NMH], 
                      color=[colors[i], colors[i]], alpha=0.7, width=0.6)
        
        print(f"β ratio {ratio}: Vm = {inverter.Vm:.2f}V, NML = {inverter.NML:.2f}V, NMH = {inverter.NMH:.2f}V")
    
    # Format subplots
    axes[0, 0].set_xlabel('Input Voltage (V)')
    axes[0, 0].set_ylabel('Output Voltage (V)')
    axes[0, 0].set_title('VTC vs Beta Ratio')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend()
    
    axes[0, 1].set_xlabel('Beta Ratio (βp/βn)')
    axes[0, 1].set_ylabel('Switching Threshold (V)')
    axes[0, 1].set_title('Vm vs Beta Ratio')
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[1, 0].set_ylabel('Noise Margin (V)')
    axes[1, 0].set_title('Noise Margins vs Beta Ratio')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Power vs beta ratio
    power_static = []
    for ratio in beta_ratios:
        # Simplified power calculation
        power_static.append(1e-9 * (1 + ratio))  # Rough approximation
    
    axes[1, 1].plot(beta_ratios, np.array(power_static)*1e9, 'ko-', linewidth=2)
    axes[1, 1].set_xlabel('Beta Ratio (βp/βn)')
    axes[1, 1].set_ylabel('Static Power (nW)')
    axes[1, 1].set_title('Power vs Beta Ratio')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def advanced_analysis_demo():
    """Demonstrate advanced analysis features"""
    print("=" * 50)
    print("ADVANCED ANALYSIS DEMONSTRATION")
    print("=" * 50)
    
    # Create high-performance inverter
    inverter = CMOSInverter(
        Vdd=3.3,
        Vtn=0.5,
        Vtp=-0.5,
        beta_n=200e-6,  # Higher drive strength
        beta_p=100e-6,
        CL=5e-12       # Lower load capacitance
    )
    
    print("\n1. Complete VTC Analysis:")
    inverter.plot_vtc(save_fig=True)
    
    print("\n2. Transient Analysis:")
    inverter.transient_analysis(tr=0.5e-9, tf=0.3e-9, save_fig=True)
    
    print("\n3. Power Analysis:")
    inverter.power_analysis(frequency_range=(1e3, 10e9), save_fig=True)
    
    print("\n4. Summary Report:")
    inverter.print_summary()

def process_variation_monte_carlo():
    """Simulate process variations using Monte Carlo method"""
    print("=" * 50)
    print("PROCESS VARIATION ANALYSIS (MONTE CARLO)")
    print("=" * 50)
    
    # Nominal parameters
    nominal_params = {
        'Vdd': 5.0,
        'Vtn': 1.0,
        'Vtp': -1.0,
        'beta_n': 100e-6,
        'beta_p': 50e-6
    }
    
    # Variation percentages (3-sigma)
    variations = {
        'Vtn': 0.1,    # ±10%
        'Vtp': 0.1,    # ±10%
        'beta_n': 0.2, # ±20%
        'beta_p': 0.2  # ±20%
    }
    
    # Monte Carlo simulation
    n_samples = 100
    switching_thresholds = []
    noise_margins_low = []
    noise_margins_high = []
    
    np.random.seed(42)  # For reproducible results
    
    for i in range(n_samples):
        # Generate random variations
        params = nominal_params.copy()
        for param, var in variations.items():
            if param in params:
                variation = np.random.normal(0, var * params[param] / 3)  # 3-sigma
                params[param] += variation
        
        # Create inverter with varied parameters
        inverter = CMOSInverter(**params)
        
        # Collect statistics
        switching_thresholds.append(inverter.Vm)
        noise_margins_low.append(inverter.NML)
        noise_margins_high.append(inverter.NMH)
    
    # Plot histograms
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Switching threshold histogram
    axes[0, 0].hist(switching_thresholds, bins=20, alpha=0.7, color='blue', edgecolor='black')
    axes[0, 0].axvline(np.mean(switching_thresholds), color='red', linestyle='--', 
                      label=f'Mean: {np.mean(switching_thresholds):.2f}V')
    axes[0, 0].set_xlabel('Switching Threshold (V)')
    axes[0, 0].set_ylabel('Count')
    axes[0, 0].set_title('Vm Distribution')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Noise margin low histogram
    axes[0, 1].hist(noise_margins_low, bins=20, alpha=0.7, color='green', edgecolor='black')
    axes[0, 1].axvline(np.mean(noise_margins_low), color='red', linestyle='--',
                      label=f'Mean: {np.mean(noise_margins_low):.2f}V')
    axes[0, 1].set_xlabel('Low Noise Margin (V)')
    axes[0, 1].set_ylabel('Count')
    axes[0, 1].set_title('NML Distribution')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Noise margin high histogram
    axes[1, 0].hist(noise_margins_high, bins=20, alpha=0.7, color='orange', edgecolor='black')
    axes[1, 0].axvline(np.mean(noise_margins_high), color='red', linestyle='--',
                      label=f'Mean: {np.mean(noise_margins_high):.2f}V')
    axes[1, 0].set_xlabel('High Noise Margin (V)')
    axes[1, 0].set_ylabel('Count')
    axes[1, 0].set_title('NMH Distribution')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Correlation plot
    axes[1, 1].scatter(switching_thresholds, noise_margins_low, alpha=0.6, color='purple')
    axes[1, 1].set_xlabel('Switching Threshold (V)')
    axes[1, 1].set_ylabel('Low Noise Margin (V)')
    axes[1, 1].set_title('Vm vs NML Correlation')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Print statistics
    print(f"\nMonte Carlo Results ({n_samples} samples):")
    print(f"Switching Threshold: {np.mean(switching_thresholds):.3f} ± {np.std(switching_thresholds):.3f} V")
    print(f"Low Noise Margin:    {np.mean(noise_margins_low):.3f} ± {np.std(noise_margins_low):.3f} V")
    print(f"High Noise Margin:   {np.mean(noise_margins_high):.3f} ± {np.std(noise_margins_high):.3f} V")
    
    # Yield analysis
    min_nm_spec = 0.3  # Minimum acceptable noise margin
    yield_nml = np.sum(np.array(noise_margins_low) >= min_nm_spec) / n_samples * 100
    yield_nmh = np.sum(np.array(noise_margins_high) >= min_nm_spec) / n_samples * 100
    print(f"\nYield Analysis (NM ≥ {min_nm_spec}V):")
    print(f"NML Yield: {yield_nml:.1f}%")
    print(f"NMH Yield: {yield_nmh:.1f}%")

def main():
    """Run all demonstration examples"""
    print("CMOS INVERTER SIMULATION - COMPREHENSIVE DEMO")
    print("=" * 60)
    
    try:
        # Run basic demonstration
        basic_vtc_demo()
        input("\nPress Enter to continue to technology comparison...")
        
        # Technology comparison
        technology_comparison()
        input("\nPress Enter to continue to sensitivity analysis...")
        
        # Parameter sensitivity
        parameter_sensitivity_analysis()
        input("\nPress Enter to continue to advanced analysis...")
        
        # Advanced analysis
        advanced_analysis_demo()
        input("\nPress Enter to continue to Monte Carlo analysis...")
        
        # Monte Carlo simulation
        process_variation_monte_carlo()
        
        print("\n" + "=" * 60)
        print("ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
        print("Check the generated plots and saved images.")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        print("Please check your Python environment and dependencies.")

if __name__ == "__main__":
    main()