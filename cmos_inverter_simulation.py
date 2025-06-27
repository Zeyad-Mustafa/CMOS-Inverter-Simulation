#!/usr/bin/env python3
"""
CMOS Inverter Simulation
Advanced simulation of CMOS inverter characteristics including:
- Voltage Transfer Characteristic (VTC)
- Transient Analysis
- Power Analysis
- Noise Margins

Author: Zeyad Mustafa
Date: June 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import warnings
warnings.filterwarnings('ignore')

class CMOSInverter:
    """
    CMOS Inverter simulation class with comprehensive analysis capabilities
    """
    
    def __init__(self, Vdd=5.0, Vtn=1.0, Vtp=-1.0, beta_n=100e-6, beta_p=50e-6, 
                 CL=10e-12, W_n=2e-6, W_p=4e-6, L=1e-6):
        """
        Initialize CMOS Inverter parameters
        
        Args:
            Vdd: Supply voltage (V)
            Vtn: NMOS threshold voltage (V)
            Vtp: PMOS threshold voltage (V)
            beta_n: NMOS transconductance parameter (A/V²)
            beta_p: PMOS transconductance parameter (A/V²)
            CL: Load capacitance (F)
            W_n: NMOS width (m)
            W_p: PMOS width (m)
            L: Channel length (m)
        """
        self.Vdd = Vdd
        self.Vtn = Vtn
        self.Vtp = Vtp
        self.beta_n = beta_n
        self.beta_p = beta_p
        self.CL = CL
        self.W_n = W_n
        self.W_p = W_p
        self.L = L
        
        # Calculate noise margins and critical points
        self.calculate_critical_points()
    
    def nmos_current(self, Vgs, Vds):
        """Calculate NMOS drain current"""
        if Vgs <= self.Vtn:
            return 0
        elif Vds >= (Vgs - self.Vtn):  # Saturation
            return 0.5 * self.beta_n * (Vgs - self.Vtn)**2
        else:  # Linear region
            return self.beta_n * ((Vgs - self.Vtn) * Vds - 0.5 * Vds**2)
    
    def pmos_current(self, Vsg, Vsd):
        """Calculate PMOS drain current"""
        if Vsg <= abs(self.Vtp):
            return 0
        elif Vsd >= (Vsg - abs(self.Vtp)):  # Saturation
            return 0.5 * self.beta_p * (Vsg - abs(self.Vtp))**2
        else:  # Linear region
            return self.beta_p * ((Vsg - abs(self.Vtp)) * Vsd - 0.5 * Vsd**2)
    
    def find_vout(self, vin):
        """Find output voltage for given input voltage"""
        def current_balance(vout):
            # NMOS current (downward)
            i_n = self.nmos_current(vin, vout)
            # PMOS current (upward)
            i_p = self.pmos_current(self.Vdd - vin, self.Vdd - vout)
            return i_n - i_p
        
        try:
            # Initial guess based on simple linear model
            if vin < self.Vdd/2:
                initial_guess = self.Vdd * 0.9
            else:
                initial_guess = self.Vdd * 0.1
            
            vout = fsolve(current_balance, initial_guess)[0]
            return max(0, min(self.Vdd, vout))
        except:
            # Fallback to simple model if numerical solution fails
            return max(0, min(self.Vdd, self.Vdd - vin))
    
    def calculate_critical_points(self):
        """Calculate critical points for noise margins"""
        try:
            # Find switching threshold (Vm)
            def find_vm(vin):
                return self.find_vout(vin) - vin
            
            self.Vm = fsolve(find_vm, self.Vdd/2)[0]
            
            # Approximate noise margins (simplified)
            self.VOL = 0.1 * self.Vdd  # Output low
            self.VOH = 0.9 * self.Vdd  # Output high
            self.VIL = self.Vtn  # Input low
            self.VIH = self.Vdd + self.Vtp  # Input high
            
            # Noise margins
            self.NML = self.VIL - self.VOL  # Low noise margin
            self.NMH = self.VOH - self.VIH  # High noise margin
            
        except:
            # Default values if calculation fails
            self.Vm = self.Vdd / 2
            self.VOL = 0.1 * self.Vdd
            self.VOH = 0.9 * self.Vdd
            self.VIL = self.Vtn
            self.VIH = self.Vdd + self.Vtp
            self.NML = 0.4
            self.NMH = 0.4
    
    def generate_vtc(self, points=200):
        """Generate Voltage Transfer Characteristic"""
        self.Vin = np.linspace(0, self.Vdd, points)
        self.Vout = np.array([self.find_vout(vin) for vin in self.Vin])
        return self.Vin, self.Vout
    
    def plot_vtc(self, save_fig=False):
        """Plot Voltage Transfer Characteristic with enhanced features"""
        if not hasattr(self, 'Vin'):
            self.generate_vtc()
        
        plt.figure(figsize=(12, 8))
        
        # Main VTC plot
        plt.subplot(2, 2, 1)
        plt.plot(self.Vin, self.Vout, 'b-', linewidth=2.5, label='VTC')
        plt.plot([0, self.Vdd], [self.Vdd, 0], 'r--', alpha=0.5, label='Ideal Inverter')
        
        # Mark critical points
        plt.axvline(x=self.Vm, color='g', linestyle=':', alpha=0.7, label=f'Vm = {self.Vm:.2f}V')
        plt.axhline(y=self.VOH, color='orange', linestyle=':', alpha=0.7, label=f'VOH = {self.VOH:.2f}V')
        plt.axhline(y=self.VOL, color='purple', linestyle=':', alpha=0.7, label=f'VOL = {self.VOL:.2f}V')
        
        plt.xlabel('Input Voltage (V)', fontsize=12)
        plt.ylabel('Output Voltage (V)', fontsize=12)
        plt.title('CMOS Inverter - Voltage Transfer Characteristic', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xlim(0, self.Vdd)
        plt.ylim(0, self.Vdd)
        
        # Gain plot
        plt.subplot(2, 2, 2)
        gain = -np.gradient(self.Vout, self.Vin)
        plt.plot(self.Vin, gain, 'r-', linewidth=2)
        plt.xlabel('Input Voltage (V)', fontsize=12)
        plt.ylabel('Gain (dVout/dVin)', fontsize=12)
        plt.title('Voltage Gain', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.xlim(0, self.Vdd)
        
        # Current vs Input Voltage
        plt.subplot(2, 2, 3)
        current = np.array([self.nmos_current(vin, self.find_vout(vin)) for vin in self.Vin])
        plt.semilogy(self.Vin, np.abs(current) * 1e6, 'g-', linewidth=2)
        plt.xlabel('Input Voltage (V)', fontsize=12)
        plt.ylabel('Supply Current (μA)', fontsize=12)
        plt.title('Supply Current vs Input', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.xlim(0, self.Vdd)
        
        # Noise margins visualization
        plt.subplot(2, 2, 4)
        plt.bar(['NML', 'NMH'], [self.NML, self.NMH], color=['blue', 'red'], alpha=0.7)
        plt.ylabel('Noise Margin (V)', fontsize=12)
        plt.title('Noise Margins', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # Add text with parameters
        param_text = f'Vdd = {self.Vdd}V\nVtn = {self.Vtn}V\nVtp = {self.Vtp}V\nVm = {self.Vm:.2f}V'
        plt.figtext(0.02, 0.02, param_text, fontsize=10, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
        
        plt.tight_layout()
        
        if save_fig:
            plt.savefig('cmos_vtc_analysis.png', dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def transient_analysis(self, tr=1e-9, tf=1e-9, period=20e-9, save_fig=False):
        """Perform transient analysis"""
        t = np.linspace(0, period, 1000)
        
        # Generate square wave input
        vin_transient = np.where(t < period/2, 0, self.Vdd)
        
        # Simplified RC response (more accurate would require solving differential equations)
        tau = 2.2 * (self.W_n/self.L) * self.CL / self.beta_n  # Rough approximation
        
        vout_transient = np.zeros_like(t)
        for i, vin in enumerate(vin_transient):
            if i == 0:
                vout_transient[i] = self.Vdd if vin == 0 else 0
            else:
                # Simple exponential transition
                if vin != vin_transient[i-1]:  # Transition detected
                    target = self.Vdd if vin == 0 else 0
                    vout_transient[i] = target
                else:
                    vout_transient[i] = vout_transient[i-1]
        
        # Apply RC filtering for more realistic response
        from scipy.signal import filtfilt, butter
        b, a = butter(3, 1/(tau * 1e9), 'low')
        vout_transient = filtfilt(b, a, vout_transient)
        
        plt.figure(figsize=(12, 6))
        
        plt.subplot(2, 1, 1)
        plt.plot(t*1e9, vin_transient, 'b-', linewidth=2, label='Input')
        plt.ylabel('Input Voltage (V)', fontsize=12)
        plt.title('CMOS Inverter - Transient Response', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xlim(0, period*1e9)
        plt.ylim(-0.5, self.Vdd + 0.5)
        
        plt.subplot(2, 1, 2)
        plt.plot(t*1e9, vout_transient, 'r-', linewidth=2, label='Output')
        plt.xlabel('Time (ns)', fontsize=12)
        plt.ylabel('Output Voltage (V)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xlim(0, period*1e9)
        plt.ylim(-0.5, self.Vdd + 0.5)
        
        plt.tight_layout()
        
        if save_fig:
            plt.savefig('cmos_transient_response.png', dpi=300, bbox_inches='tight')
        
        plt.show()
        
        # Calculate propagation delays
        tpLH = tr  # Simplified
        tpHL = tf  # Simplified
        print(f"Estimated Propagation Delays:")
        print(f"tpLH (Low to High): {tpLH*1e9:.2f} ns")
        print(f"tpHL (High to Low): {tpHL*1e9:.2f} ns")
        print(f"Average tp: {(tpLH + tpHL)*1e9/2:.2f} ns")
    
    def power_analysis(self, frequency_range=(1e3, 1e9), save_fig=False):
        """Analyze power consumption vs frequency"""
        frequencies = np.logspace(np.log10(frequency_range[0]), np.log10(frequency_range[1]), 50)
        
        # Static power (leakage) - simplified
        P_static = 1e-9  # 1 nW
        
        # Dynamic power: P = α * CL * Vdd² * f
        alpha = 0.5  # Activity factor
        P_dynamic = alpha * self.CL * self.Vdd**2 * frequencies
        
        P_total = P_static + P_dynamic
        
        plt.figure(figsize=(10, 6))
        plt.loglog(frequencies, P_static * np.ones_like(frequencies) * 1e9, 
                  'b--', label='Static Power', linewidth=2)
        plt.loglog(frequencies, P_dynamic * 1e9, 'r-', label='Dynamic Power', linewidth=2)
        plt.loglog(frequencies, P_total * 1e9, 'k-', label='Total Power', linewidth=2)
        
        plt.xlabel('Frequency (Hz)', fontsize=12)
        plt.ylabel('Power (nW)', fontsize=12)
        plt.title('CMOS Inverter - Power vs Frequency', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        if save_fig:
            plt.savefig('cmos_power_analysis.png', dpi=300, bbox_inches='tight')
        
        plt.show()
        
        # Print power at specific frequencies
        for f in [1e6, 100e6, 1e9]:
            idx = np.argmin(np.abs(frequencies - f))
            print(f"Power at {f/1e6:.0f} MHz: {P_total[idx]*1e9:.2f} nW")
    
    def parameter_sweep(self, param_name, param_values, save_fig=False):
        """Sweep a parameter and show its effect on VTC"""
        plt.figure(figsize=(10, 6))
        
        original_value = getattr(self, param_name)
        
        for i, value in enumerate(param_values):
            setattr(self, param_name, value)
            self.calculate_critical_points()
            vin, vout = self.generate_vtc()
            
            plt.plot(vin, vout, linewidth=2, 
                    label=f'{param_name} = {value}' + ('V' if 'V' in param_name else ''))
        
        # Restore original value
        setattr(self, param_name, original_value)
        self.calculate_critical_points()
        
        plt.xlabel('Input Voltage (V)', fontsize=12)
        plt.ylabel('Output Voltage (V)', fontsize=12)
        plt.title(f'Parameter Sweep: {param_name}', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xlim(0, self.Vdd)
        plt.ylim(0, self.Vdd)
        
        if save_fig:
            plt.savefig(f'cmos_sweep_{param_name}.png', dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def print_summary(self):
        """Print comprehensive analysis summary"""
        print("="*60)
        print("CMOS INVERTER SIMULATION SUMMARY")
        print("="*60)
        print(f"Supply Voltage (Vdd):     {self.Vdd:.2f} V")
        print(f"NMOS Threshold (Vtn):     {self.Vtn:.2f} V")
        print(f"PMOS Threshold (Vtp):     {self.Vtp:.2f} V")
        print(f"Switching Threshold (Vm): {self.Vm:.2f} V")
        print("-"*40)
        print("NOISE MARGINS:")
        print(f"  VOH (Output High):      {self.VOH:.2f} V")
        print(f"  VOL (Output Low):       {self.VOL:.2f} V")
        print(f"  VIH (Input High):       {self.VIH:.2f} V")
        print(f"  VIL (Input Low):        {self.VIL:.2f} V")
        print(f"  NMH (High Margin):      {self.NMH:.2f} V")
        print(f"  NML (Low Margin):       {self.NML:.2f} V")
        print("-"*40)
        print("DEVICE PARAMETERS:")
        print(f"  βn (NMOS):             {self.beta_n*1e6:.1f} μA/V²")
        print(f"  βp (PMOS):             {self.beta_p*1e6:.1f} μA/V²")
        print(f"  Load Capacitance:       {self.CL*1e12:.1f} pF")
        print("="*60)

def main():
    """Main function demonstrating the CMOS inverter simulation"""
    print("CMOS Inverter Simulation - Advanced Analysis")
    print("=" * 50)
    
    # Create CMOS inverter instances for different technologies
    print("\n1. 5V Technology Analysis:")
    cmos_5v = CMOSInverter(Vdd=5.0, Vtn=1.0, Vtp=-1.0)
    cmos_5v.print_summary()
    cmos_5v.plot_vtc()
    
    print("\n2. 3.3V Technology Analysis:")
    cmos_33v = CMOSInverter(Vdd=3.3, Vtn=0.7, Vtp=-0.7)
    cmos_33v.print_summary()
    cmos_33v.plot_vtc()
    
    # Transient analysis
    print("\n3. Transient Analysis:")
    cmos_5v.transient_analysis()
    
    # Power analysis
    print("\n4. Power Analysis:")
    cmos_5v.power_analysis()
    
    # Parameter sweep
    print("\n5. Parameter Sweep - Supply Voltage:")
    cmos_sweep = CMOSInverter()
    cmos_sweep.parameter_sweep('Vdd', [3.3, 5.0, 6.0])
    
    print("\nSimulation completed successfully!")
    print("Check the generated plots for detailed analysis.")

if __name__ == "__main__":
    main()