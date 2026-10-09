from fastapi import FastAPI
import random
import datetime

app = FastAPI()

@app.get("/api/live_equipment_data")
def get_live_data():
    """
    Simulates a real-time API endpoint returning live metrics from lab equipment.
    In a real scenario, this would query a SQL database or IoT sensor broker (MQTT).
    """
    equipments = ["Oven_A", "Oven_B", "HAST_Chamber_1", "HTS_Chamber_2"]
    test_types = ["Temp Cycling", "HAST", "HTS"]
    
    # Generate a random payload representing the latest batch
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "Batch_ID": f"LIVE_LOT_{random.randint(1000, 9999)}",
        "Test_Type": random.choice(test_types),
        "Equipment_ID": random.choice(equipments),
        "Thermal_Cycles": random.randint(500, 2000),
        "Max_Temp_C": round(random.uniform(125.0, 150.0), 2),
        "Output_Voltage_mV": round(random.uniform(3200.0, 3400.0), 2),
        "TAT_Days": round(random.uniform(10.0, 18.0), 1),
        "Status": "Running"
    }
