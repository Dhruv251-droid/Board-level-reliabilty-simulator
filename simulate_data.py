import pandas as pd
import numpy as np

def generate_mock_data(filename="thermal_simulation_data.csv", num_rows=800):
    np.random.seed(42)

    # Generate Batch IDs
    batch_ids = [f"LOT_{i//50:03d}" for i in range(num_rows)]

    # Tactical Planning & Equipment
    equipments = ["Oven_A", "Oven_B", "HAST_Chamber_1", "HTS_Chamber_2"]
    test_types = ["Temp Cycling", "HAST", "HTS"]
    
    equipment_assigned = np.random.choice(equipments, size=num_rows)
    test_type_assigned = np.random.choice(test_types, size=num_rows)
    
    # TAT (Turn Around Time) in days - target is 14 days
    tat_days = np.random.normal(loc=12.5, scale=2.5, size=num_rows)

    # Engineering / Reliability Parameters
    thermal_cycles = np.random.randint(500, 2001, size=num_rows)
    max_temp_c = np.random.uniform(125.0, 150.0, size=num_rows)

    # Output Voltage with degradation
    base_voltage = 3375
    degradation = (thermal_cycles / 100) * 5
    noise = np.random.normal(0, 15, size=num_rows)
    output_voltage_mv = base_voltage - degradation + noise

    df = pd.DataFrame({
        "Batch_ID": batch_ids,
        "Test_Type": test_type_assigned,
        "Equipment_ID": equipment_assigned,
        "Thermal_Cycles": thermal_cycles,
        "Max_Temp_C": np.round(max_temp_c, 2),
        "Output_Voltage_mV": np.round(output_voltage_mv, 2),
        "TAT_Days": np.round(tat_days, 1)
    })

    df.to_csv(filename, index=False)
    print(f"Generated {num_rows} rows in {filename}")

if __name__ == "__main__":
    generate_mock_data()
