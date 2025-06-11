import numpy as np
import matplotlib.pyplot as plt

# Parameters (simplified)
Vdd = 5.0  # Supply voltage
Vin = np.linspace(0, Vdd, 100)
Vout = Vdd - Vin  # Simplified model for illustration

plt.plot(Vin, Vout)
plt.title('CMOS Inverter Voltage Transfer Characteristic')
plt.xlabel('Input Voltage (V)')
plt.ylabel('Output Voltage (V)')
plt.grid(True)
plt.show()
