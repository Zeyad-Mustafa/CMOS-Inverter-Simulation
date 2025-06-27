# CMOS Inverter Simulation

A comprehensive Python simulation of CMOS (Complementary Metal-Oxide-Semiconductor) inverter characteristics, including voltage transfer curves, transient analysis, and power consumption analysis.

## 🔧 Features

- **Voltage Transfer Characteristic (VTC)** - Detailed analysis of input-output voltage relationship
- **Transient Response** - Time-domain behavior analysis
- **Power Analysis** - Static and dynamic power consumption
- **Noise Margins** - VOH, VOL, VIH, VIL calculations
- **Interactive Plots** - Professional visualization with matplotlib
- **Parametric Analysis** - Easy parameter adjustment for different technologies

## 📋 Requirements

- Python 3.7+
- NumPy
- Matplotlib
- SciPy

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/Zeyad-Mustafa/CMOS-Inverter-Simulation.git
cd CMOS-Inverter-Simulation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the simulation:
```bash
python cmos_inverter_simulation.py
```

## 📊 Simulation Results

The simulation generates several key plots:

1. **Voltage Transfer Characteristic** - Shows the relationship between input and output voltages
2. **Transient Response** - Demonstrates switching behavior over time
3. **Power vs. Frequency** - Analyzes power consumption at different frequencies
4. **Current Analysis** - Shows supply current variations

## 🔬 Technical Details

### CMOS Inverter Model

The simulation uses a simplified but accurate model based on:
- NMOS and PMOS transistor characteristics
- Threshold voltages and transconductance parameters
- Capacitive loading effects
- Supply voltage scaling

### Key Parameters

- **Vdd**: Supply voltage (default: 5V, configurable for 3.3V, 1.8V)
- **Vtn**: NMOS threshold voltage
- **Vtp**: PMOS threshold voltage  
- **βn, βp**: Transconductance parameters
- **CL**: Load capacitance

## 📈 Usage Examples

### Basic Simulation
```python
from cmos_inverter_simulation import CMOSInverter

# Create inverter instance
inverter = CMOSInverter(Vdd=5.0, Vtn=1.0, Vtp=-1.0)

# Generate VTC
inverter.plot_vtc()

# Run transient analysis
inverter.transient_analysis()
```

### Parameter Sweep
```python
# Analyze different supply voltages
for vdd in [1.8, 3.3, 5.0]:
    inverter = CMOSInverter(Vdd=vdd)
    inverter.plot_vtc()
```

## 🎯 Applications

- **Digital Circuit Design** - Understanding logic gate behavior
- **VLSI Course Projects** - Educational tool for semiconductor courses
- **Performance Analysis** - Evaluating different CMOS technologies
- **Research** - Baseline for advanced CMOS modeling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Zeyad Mustafa**
- GitHub: [@Zeyad-Mustafa](https://github.com/Zeyad-Mustafa)

## 🙏 Acknowledgments

- Based on fundamental CMOS theory from Razavi, Sedra & Smith
- Inspired by academic VLSI coursework
- Community feedback and contributions

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the documentation
- Review example usage in the code
- I have got lots of help from AI.
---

*Last updated: June 2025*
