import pandas as pd
import numpy as np

def generate_mock_data(filename="thermal_simulation_data.csv", num_rows=500):
    np.random.seed(42)  # For reproducibility

    # Generate Batch IDs
    batch_ids = [f"BATCH_{i//50:03d}" for i in range(num_rows)]

    # Generate Thermal Cycles between 500 and 2000
    thermal_cycles = np.random.randint(500, 2001, size=num_rows)

    # Generate Max Temp C between 125.0 and 150.0
    max_temp_c = np.random.uniform(125.0, 150.0, size=num_rows)

    # Generate Output Voltage mV around 3300mV
    # Negative correlation with Thermal Cycles: 
    # Let's say for every 100 cycles, voltage drops by 5mV on average.
    # Base voltage is 3350 so that it degrades to around 3250-3300.
    base_voltage = 3375
    degradation = (thermal_cycles / 100) * 5
    
    # Add some normal noise
    noise = np.random.normal(0, 15, size=num_rows)
    
    output_voltage_mv = base_voltage - degradation + noise

    df = pd.DataFrame({
        "Batch_ID": batch_ids,
        "Thermal_Cycles": thermal_cycles,
        "Max_Temp_C": np.round(max_temp_c, 2),
        "Output_Voltage_mV": np.round(output_voltage_mv, 2)
    })

    df.to_csv(filename, index=False)
    print(f"Generated {num_rows} rows in {filename}")

if __name__ == "__main__":
    generate_mock_data()
