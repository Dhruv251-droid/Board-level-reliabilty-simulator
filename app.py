import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import datetime
import random

def calculate_cpk(data, lsl, usl):
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    if std == 0: return float('inf')
    cpl = (mean - lsl) / (3 * std)
    cpu = (usl - mean) / (3 * std)
    return min(cpl, cpu)

st.set_page_config(page_title="Micron BLR & Tactical Planning Dashboard", layout="wide")

st.title("Board-Level Reliability (BLR) & Lab Operations Dashboard")
st.markdown("Integrated platform for **Reliability Engineering (JEDEC standards)** and **Tactical Lab Planning**.")

# ----------------------------------------------------------------------
# DATA INGESTION: CSV OR REAL-TIME API
# ----------------------------------------------------------------------
st.sidebar.header("Data Source")
data_source = st.sidebar.radio("Select Data Source:", ["Local CSV (Historical)", "Real-time Lab API"])

@st.cache_data(ttl=60)
def load_csv_data():
    try:
        return pd.read_csv("thermal_simulation_data.csv")
    except FileNotFoundError:
        return None

df = load_csv_data()

if data_source == "Local CSV (Historical)":
    if df is None:
        st.error("Data file not found. Please run simulate_data.py first.")
else:
    # --- REAL TIME API MOCK ---
    st.sidebar.info("🔌 Listening to equipment IoT feeds...")
    live_payload = None
    try:
        # Attempt to reach the local backend if running locally
        response = requests.get("http://localhost:8000/api/live_equipment_data", timeout=1)
        if response.status_code == 200:
            live_payload = response.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        # Fallback for Streamlit Cloud deployment demo
        # If backend is unreachable, we simulate the backend response directly here
        live_payload = {
            "timestamp": datetime.datetime.now().isoformat(),
            "Batch_ID": f"LIVE_LOT_{random.randint(1000, 9999)}",
            "Test_Type": random.choice(["Temp Cycling", "HAST", "HTS"]),
            "Equipment_ID": random.choice(["Oven_A", "Oven_B", "HAST_Chamber_1", "HTS_Chamber_2"]),
            "Thermal_Cycles": random.randint(500, 2000),
            "Max_Temp_C": round(random.uniform(125.0, 150.0), 2),
            "Output_Voltage_mV": round(random.uniform(3200.0, 3400.0), 2),
            "TAT_Days": round(random.uniform(10.0, 18.0), 1),
            "Status": "Running"
        }
        st.sidebar.caption("*(Note: Using internal mock stream. Local FastAPI backend not detected on port 8000)*")

    if live_payload:
        st.sidebar.success(f"Latest read from: {live_payload['Equipment_ID']}")
        st.sidebar.json(live_payload)
        
        # Append live read to historical data
        if df is not None:
            live_df = pd.DataFrame([live_payload])
            df = pd.concat([df, live_df], ignore_index=True)
        else:
            df = pd.DataFrame([live_payload])

# ----------------------------------------------------------------------
# DASHBOARD RENDERING
# ----------------------------------------------------------------------
if df is not None and not df.empty:
    tab1, tab2 = st.tabs(["🔧 Reliability Engineering (Process & CpK)", "📊 Tactical Planning & Lab Operations"])
    
    with tab1:
        st.header("Process Capability & DOE Analysis")
        st.markdown("*Emulating PCB Board-Level Reliability under JEDEC standard conditions (HAST, HTS, Temp Cycling).*")
        
        col1, col2 = st.columns(2)
        with col1:
            LSL = 3150.0
            USL = 3450.0
            
            df['Output_Voltage_mV'] = pd.to_numeric(df['Output_Voltage_mV'], errors='coerce')
            voltages = df['Output_Voltage_mV'].dropna().values
            
            cpk_value = calculate_cpk(voltages, LSL, USL)
            
            st.metric(
                label="Process Capability Index (CpK)", 
                value=f"{cpk_value:.2f}",
                delta="Target >= 1.33",
                delta_color="normal" if cpk_value >= 1.33 else "inverse"
            )
            
        with col2:
            st.metric("Total Qualifications Monitored", len(df))
            st.metric("JEDEC Test Excursions (CpK < 1.33)", "Active" if cpk_value < 1.33 else "Clear")

        st.subheader("DOE: Voltage Degradation vs Thermal Stress")
        fig_doe = px.scatter(
            df, x="Thermal_Cycles", y="Output_Voltage_mV", color="Test_Type",
            title="DOE Evaluation: Process Deviation under Thermal Stress",
            labels={"Thermal_Cycles": "Thermal Cycles", "Output_Voltage_mV": "Output Voltage (mV)"},
            trendline="ols" if len(df) > 1 else None
        )
        fig_doe.add_hline(y=LSL, line_dash="dash", line_color="red", annotation_text="LSL")
        fig_doe.add_hline(y=USL, line_dash="dash", line_color="red", annotation_text="USL")
        st.plotly_chart(fig_doe, use_container_width=True)

        if cpk_value < 1.33:
            st.error("🚨 **PROCESS DEVIATION DETECTED**: CpK < 1.33. Generating 8D Report.")
            with st.expander("📄 View Automated 8D Troubleshooting Report", expanded=False):
                st.markdown("""
                **D1: Form the Team** | Cross-functional team (Quality, Mfg, Planning) assembled.
                
                **D2: Describe the Problem** | Board-level reliability emulating customer PCB shows CpK dropping below 1.33 during high thermal cycle HAST/HTS.
                
                **D3: Interim Containment** | Pause lab loading for affected lots. Quarantine material exceeding 1500 cycles.
                
                **D4: Root Cause Analysis** | Systemic process deviation identified: equipment interaction causing severe solder fatigue under JEDEC Temp Cycling.
                
                **D5: Permanent Corrective Action** | Implement process control methods; adjust oven calibration; modify package material to meet standard reliability methodologies.
                
                **D6: Implement & Validate** | Run Special Work Request (SWR) DOE to validate new process limits.
                
                **D7: Prevent Recurrence** | Integrate AI-driven monitoring for proactive CpK prediction.
                
                **D8: Recognize the Team** | Issue contained.
                """)
        else:
            st.success(f"✅ Process is capable. CpK is {cpk_value:.2f} (Target >= 1.33).")

    with tab2:
        st.header("Lab Loading & Turn Around Time (TAT) Management")
        st.markdown("*Scheduling, Equipment Utilization, and KPI tracking for Reliability Program Monitoring (RPM).*")

        df['TAT_Days'] = pd.to_numeric(df['TAT_Days'], errors='coerce')
        avg_tat = df['TAT_Days'].mean()
        tat_target = 14.0
        
        col_t1, col_t2, col_t3 = st.columns(3)
        col_t1.metric("Average TAT (Days)", f"{avg_tat:.1f}", f"{tat_target - avg_tat:.1f} days ahead of target" if avg_tat < tat_target else f"{avg_tat - tat_target:.1f} days behind target")
        col_t2.metric("Active Test Chambers", df['Equipment_ID'].nunique())
        col_t3.metric("Samples in Corridor Test", len(df[df['Test_Type'] == 'HTS']))

        st.subheader("Lab Equipment Utilization (4M Readiness)")
        equip_counts = df['Equipment_ID'].value_counts().reset_index()
        equip_counts.columns = ['Equipment', 'Lots_Assigned']
        
        fig_util = px.bar(
            equip_counts, x='Equipment', y='Lots_Assigned', 
            title="Lab Loading by Equipment", 
            color='Lots_Assigned',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_util, use_container_width=True)

        if len(df) > 1:
            st.subheader("Turn Around Time (TAT) Cadence KPI")
            fig_tat = px.box(
                df, x="Test_Type", y="TAT_Days", color="Test_Type",
                title="TAT Distribution by Reliability Test (JEDEC)",
            )
            fig_tat.add_hline(y=tat_target, line_dash="dash", line_color="red", annotation_text="TAT Target (14 Days)")
            st.plotly_chart(fig_tat, use_container_width=True)
        
        st.info("💡 **AI Planner Recommendation**: 'Oven_A' is approaching a bottleneck based on loading forecast. Recommend staggered preventive maintenance for 'Oven_B' to absorb upcoming Special Work Requests (SWR).")
