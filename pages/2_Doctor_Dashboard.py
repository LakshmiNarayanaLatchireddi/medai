import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.vitals_agent import VitalsAgent
from agents.digital_twin_agent import DigitalTwinAgent
from agents.summary_agent import SummaryAgent

# Configure page
st.set_page_config(
    page_title="Doctor Dashboard - MediAI Guardian 3.0",
    page_icon="👨‍⚕️",
    layout="wide"
)

# Check authentication
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please login first")
    st.switch_page("app.py")
    st.stop()

if st.session_state.role != "doctor":
    st.error("Access denied. This page is for doctors only.")
    st.switch_page("app.py")
    st.stop()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #7c3aed 0%, #a855f7 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .patient-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #7c3aed;
        margin-bottom: 1rem;
    }
    .alert-high {
        background: linear-gradient(90deg, #ef4444 0%, #f87171 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .alert-medium {
        background: linear-gradient(90deg, #f59e0b 0%, #fbbf24 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .alert-low {
        background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize agents
@st.cache_resource
def get_agents():
    return {
        'vitals': VitalsAgent(),
        'digital_twin': DigitalTwinAgent(),
        'summary': SummaryAgent()
    }

agents = get_agents()

# Sample patient data
@st.cache_data
def get_patient_data():
    return {
        'patient_001': {
            'name': 'John Doe',
            'age': 45,
            'gender': 'Male',
            'condition': 'Hypertension',
            'last_vitals': {
                'heart_rate': 78,
                'blood_pressure': '130/85',
                'temperature': 98.4,
                'oxygen_saturation': 97
            },
            'risk_level': 'Mild Risk',
            'medications': ['Lisinopril', 'Metformin'],
            'last_emergency': None
        },
        'patient_002': {
            'name': 'Jane Smith',
            'age': 32,
            'gender': 'Female',
            'condition': 'Diabetes Type 2',
            'last_vitals': {
                'heart_rate': 72,
                'blood_pressure': '118/76',
                'temperature': 98.6,
                'oxygen_saturation': 99
            },
            'risk_level': 'Healthy',
            'medications': ['Metformin', 'Insulin'],
            'last_emergency': None
        },
        'patient_003': {
            'name': 'Robert Johnson',
            'age': 67,
            'gender': 'Male',
            'condition': 'Heart Disease',
            'last_vitals': {
                'heart_rate': 95,
                'blood_pressure': '145/92',
                'temperature': 99.1,
                'oxygen_saturation': 94
            },
            'risk_level': 'High Risk',
            'medications': ['Atorvastatin', 'Warfarin', 'Amlodipine'],
            'last_emergency': 'Chest Pain - 2 hours ago'
        }
    }

def create_vitals_trend_chart():
    """Create a sample vitals trend chart"""
    dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq='D')
    
    # Sample data for heart rate trend
    heart_rates = [72, 75, 73, 78, 76, 74, 77]
    bp_sys = [120, 125, 118, 130, 128, 122, 126]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=heart_rates,
        mode='lines+markers',
        name='Heart Rate (bpm)',
        line=dict(color='#ef4444', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=bp_sys,
        mode='lines+markers',
        name='Systolic BP (mmHg)',
        line=dict(color='#3b82f6', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='Patient Vitals Trend (Last 7 Days)',
        xaxis_title='Date',
        yaxis=dict(title='Heart Rate (bpm)', side='left'),
        yaxis2=dict(title='Blood Pressure (mmHg)', side='right', overlaying='y'),
        height=400,
        showlegend=True
    )
    
    return fig

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>👨‍⚕️ Doctor Dashboard</h1>
        <h3>Patient Monitoring & Analytics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Get patient data
    patients = get_patient_data()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total Patients", "3", delta="0")
    with col2:
        high_risk_count = sum(1 for p in patients.values() if p['risk_level'] == 'High Risk')
        st.metric("🚨 High Risk", str(high_risk_count), delta="+1")
    with col3:
        emergency_count = sum(1 for p in patients.values() if p['last_emergency'])
        st.metric("⚡ Active Emergencies", str(emergency_count), delta="0")
    with col4:
        st.metric("📊 Avg Response Time", "2.3 min", delta="-0.5 min")
    
    # Main content
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Patient Summary
        st.markdown("### 👥 Patient Overview")
        
        for patient_id, patient in patients.items():
            with st.expander(f"👤 {patient['name']} (ID: {patient_id})", expanded=True):
                col_info, col_vitals = st.columns(2)
                
                with col_info:
                    st.write(f"**Age:** {patient['age']}")
                    st.write(f"**Gender:** {patient['gender']}")
                    st.write(f"**Condition:** {patient['condition']}")
                    st.write(f"**Medications:** {', '.join(patient['medications'])}")
                
                with col_vitals:
                    st.write(f"**Heart Rate:** {patient['last_vitals']['heart_rate']} bpm")
                    st.write(f"**Blood Pressure:** {patient['last_vitals']['blood_pressure']}")
                    st.write(f"**Temperature:** {patient['last_vitals']['temperature']}°F")
                    st.write(f"**O2 Saturation:** {patient['last_vitals']['oxygen_saturation']}%")
                
                # Risk level indicator
                risk_level = patient['risk_level']
                if risk_level == 'High Risk':
                    st.markdown(f'<div class="alert-high">🚨 {risk_level}</div>', unsafe_allow_html=True)
                elif risk_level == 'Mild Risk':
                    st.markdown(f'<div class="alert-medium">⚠️ {risk_level}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="alert-low">✅ {risk_level}</div>', unsafe_allow_html=True)
                
                # Emergency alert
                if patient['last_emergency']:
                    st.error(f"🚨 **Emergency Alert:** {patient['last_emergency']}")
                
                # Action buttons
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                with col_btn1:
                    if st.button(f"📊 View Details", key=f"details_{patient_id}"):
                        st.info(f"Detailed view for {patient['name']} would open here")
                with col_btn2:
                    if st.button(f"💊 Medications", key=f"meds_{patient_id}"):
                        st.info(f"Medication management for {patient['name']}")
                with col_btn3:
                    if st.button(f"📋 Generate Report", key=f"report_{patient_id}"):
                        # Generate AI summary
                        summary = agents['summary'].run({
                            'patient_data': patient,
                            'patient_id': patient_id
                        })
                        st.success("Report generated successfully!")
                        with st.expander("📄 AI Generated Summary"):
                            st.write(summary['summary'])
        
        # Vitals Trend Chart
        st.markdown("### 📈 Vitals Trend Analysis")
        vitals_chart = create_vitals_trend_chart()
        st.plotly_chart(vitals_chart, use_container_width=True)
    
    with col_right:
        # Emergency Events
        st.markdown("### 🚨 Recent Emergency Events")
        
        emergency_events = [
            {
                'time': '2 hours ago',
                'patient': 'Robert Johnson',
                'event': 'Chest Pain',
                'severity': 'High',
                'status': 'Monitoring'
            },
            {
                'time': '1 day ago',
                'patient': 'Jane Smith',
                'event': 'Low Blood Sugar',
                'severity': 'Medium',
                'status': 'Resolved'
            },
            {
                'time': '3 days ago',
                'patient': 'John Doe',
                'event': 'High Blood Pressure',
                'severity': 'Medium',
                'status': 'Resolved'
            }
        ]
        
        for event in emergency_events:
            severity_class = {
                'High': 'alert-high',
                'Medium': 'alert-medium',
                'Low': 'alert-low'
            }.get(event['severity'], 'alert-low')
            
            st.markdown(f"""
            <div class="{severity_class}">
                <strong>{event['event']}</strong><br>
                Patient: {event['patient']}<br>
                Time: {event['time']}<br>
                Status: {event['status']}
            </div>
            """, unsafe_allow_html=True)
        
        # Digital Twin Risk Distribution
        st.markdown("### 🎯 Digital Twin Risk Distribution")
        
        risk_data = {
            'Healthy': 1,
            'Mild Risk': 1,
            'High Risk': 1
        }
        
        fig_pie = px.pie(
            values=list(risk_data.values()),
            names=list(risk_data.keys()),
            color_discrete_map={
                'Healthy': '#10b981',
                'Mild Risk': '#f59e0b',
                'High Risk': '#ef4444'
            }
        )
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("📊 Generate Hospital Report", use_container_width=True):
            st.success("Hospital-wide report generated!")
        
        if st.button("🚨 Emergency Protocol", use_container_width=True):
            st.info("Emergency protocol activated")
        
        if st.button("💊 Drug Interaction Check", use_container_width=True):
            st.switch_page("pages/3_Medicine_Reactions.py")
        
        if st.button("📋 Patient Summary", use_container_width=True):
            st.switch_page("pages/5_Doctor_Summary.py")
    
    # Real-time updates
    st.markdown("---")
    col_refresh1, col_refresh2 = st.columns(2)
    
    with col_refresh1:
        if st.button("🔄 Refresh Patient Data"):
            st.rerun()
    
    with col_refresh2:
        auto_refresh = st.checkbox("🔄 Auto-refresh (30s)")
        if auto_refresh:
            st.info("Auto-refresh enabled - Data updates every 30 seconds")

if __name__ == "__main__":
    main()
