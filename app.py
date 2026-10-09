import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def calculate_cpk(data, lsl, usl):
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    
    if std == 0:
        return float('inf')
        
    cpl = (mean - lsl) / (3 * std)
    cpu = (usl - mean) / (3 * std)
    
    return min(cpl, cpu)

st.set_page_config(page_title="BLR Simulator Dashboard", layout="wide")

st.title("Board-Level Reliability (BLR) Simulator")
st.markdown("Dashboard for evaluating thermal simulation data, Process Capability (CpK), and DOE metrics.")

# 1. Data Ingestion
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("thermal_simulation_data.csv")
        return df
    except FileNotFoundError:
        st.error("Data file 'thermal_simulation_data.csv' not found. Please run the simulation step first.")
        return None

df = load_data()

if df is not None:
    st.header("1. Design of Experiments (DOE) Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(df.head(10))
        
    with col2:
        st.markdown("**Simulation Parameters:**")
        st.markdown(f"- **Total Runs:** {len(df)}")
        st.markdown(f"- **Thermal Cycles Range:** {df['Thermal_Cycles'].min()} to {df['Thermal_Cycles'].max()}")
        st.markdown(f"- **Max Temp Range:** {df['Max_Temp_C'].min()}°C to {df['Max_Temp_C'].max()}°C")
    
    # DOE Visuals
    st.subheader("DOE Metrics: Thermal Cycles vs Output Voltage")
    
    fig = px.scatter(
        df, 
        x="Thermal_Cycles", 
        y="Output_Voltage_mV", 
        color="Max_Temp_C",
        title="Thermal Degradation: Output Voltage vs Cycles",
        labels={"Thermal_Cycles": "Thermal Cycles", "Output_Voltage_mV": "Output Voltage (mV)", "Max_Temp_C": "Max Temp (°C)"},
        trendline="ols"
    )
    st.plotly_chart(fig, use_container_width=True)

    # 2. Process Capability (CpK)
    st.header("2. Process Capability (CpK)")
    
    LSL = 3150.0
    USL = 3450.0
    
    voltages = df['Output_Voltage_mV'].dropna().values
    cpk_value = calculate_cpk(voltages, LSL, USL)
    
    st.metric(
        label="Process Capability Index (CpK)", 
        value=f"{cpk_value:.2f}",
        delta="Target >= 1.33",
        delta_color="normal" if cpk_value >= 1.33 else "inverse"
    )
    
    # Visualizing the distribution against limits
    fig_hist = px.histogram(
        df, 
        x="Output_Voltage_mV", 
        nbins=30, 
        title="Voltage Distribution vs Specification Limits",
        marginal="box"
    )
    fig_hist.add_vline(x=LSL, line_dash="dash", line_color="red", annotation_text="LSL (3150mV)")
    fig_hist.add_vline(x=USL, line_dash="dash", line_color="red", annotation_text="USL (3450mV)")
    st.plotly_chart(fig_hist, use_container_width=True)

    # 3. Automated 8D Report
    if cpk_value < 1.33:
        st.error(f"🚨 **WARNING**: CpK is {cpk_value:.2f}, which is below the industry standard of 1.33. Initiating automated 8D Report.")
        
        st.header("Automated 8D Problem Solving Report")
        
        st.markdown("""
        **D1: Form the Team**
        - Automated Reliability System & Thermal Analysis Subsystem.

        **D2: Describe the Problem**
        - The process capability index (CpK) for the Board-Level Reliability (BLR) simulation has dropped to an unacceptable level (below 1.33). Specifically, the output voltage demonstrates significant degradation across thermal cycles, risking operation outside the specification limits (3150mV - 3450mV).

        **D3: Interim Containment Actions (ICA)**
        - Halt simulated batch approvals. 
        - Flag lots operating above 135°C and > 1500 thermal cycles for immediate manual review.

        **D4: Root Cause Analysis (RCA)**
        - **Data Correlation:** Scatter plot indicates a strong negative correlation between the number of Thermal Cycles and Output Voltage.
        - **Physical Mechanism:** Suspected solder joint fatigue and increased parasitic resistance due to severe thermal stress (simulating HAST/HTS conditions), causing voltage drops.

        **D5: Develop Permanent Corrective Actions (PCA)**
        - Re-design PCB layout to improve thermal dissipation.
        - Evaluate alternative solder alloys with higher thermal fatigue resistance.
        - Adjust microcontroller embedded tolerances to handle increased parasitic load.

        **D6: Implement and Validate PCA**
        - *Pending Engineering Action.* (Requires physical DOE verification of new alloy/layout).

        **D7: Prevent Recurrence**
        - Integrate continuous CpK monitoring (this dashboard) into the CI/CD pipeline for hardware readiness.
        - Update design rules to enforce stricter thermal margins.

        **D8: Recognize the Team**
        - Automated issue detection successful. Ready for engineering handover.
        """)
    else:
        st.success(f"✅ Process is capable. CpK is {cpk_value:.2f} (Target >= 1.33).")

