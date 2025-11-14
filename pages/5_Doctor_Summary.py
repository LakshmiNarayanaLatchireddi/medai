import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.summary_agent import SummaryAgent
from agents.vitals_agent import VitalsAgent

# Configure page
st.set_page_config(
    page_title="Doctor Summary - MediAI Guardian 3.0",
    page_icon="📋",
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
        background: linear-gradient(90deg, #059669 0%, #10b981 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .summary-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #059669;
        margin-bottom: 1.5rem;
    }
    .metric-highlight {
        background: linear-gradient(90deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #0ea5e9;
        margin: 0.5rem 0;
    }
    .recommendation {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .alert-item {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize agents
@st.cache_resource
def get_agents():
    return {
        'summary': SummaryAgent(),
        'vitals': VitalsAgent()
    }

agents = get_agents()

def generate_sample_data():
    """Generate comprehensive sample patient data for the report"""
    return {
        'patient_info': {
            'name': 'John Doe',
            'patient_id': 'P001',
            'age': 45,
            'gender': 'Male',
            'date_of_birth': '1979-03-15',
            'primary_condition': 'Hypertension, Type 2 Diabetes',
            'attending_physician': 'Dr. Sarah Johnson',
            'report_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        'vitals_history': [
            {'date': '2024-11-13', 'heart_rate': 78, 'bp_sys': 130, 'bp_dia': 85, 'temp': 98.4, 'o2_sat': 97},
            {'date': '2024-11-12', 'heart_rate': 75, 'bp_sys': 128, 'bp_dia': 82, 'temp': 98.6, 'o2_sat': 98},
            {'date': '2024-11-11', 'heart_rate': 80, 'bp_sys': 135, 'bp_dia': 88, 'temp': 98.3, 'o2_sat': 96},
            {'date': '2024-11-10', 'heart_rate': 77, 'bp_sys': 132, 'bp_dia': 86, 'temp': 98.5, 'o2_sat': 97},
            {'date': '2024-11-09', 'heart_rate': 82, 'bp_sys': 138, 'bp_dia': 90, 'temp': 98.7, 'o2_sat': 95}
        ],
        'medications': [
            {'name': 'Lisinopril', 'dosage': '10mg', 'frequency': 'Once daily', 'start_date': '2024-01-15'},
            {'name': 'Metformin', 'dosage': '500mg', 'frequency': 'Twice daily', 'start_date': '2024-02-01'},
            {'name': 'Atorvastatin', 'dosage': '20mg', 'frequency': 'Once daily', 'start_date': '2024-03-01'}
        ],
        'drug_interactions': [
            {'drug_a': 'Lisinopril', 'drug_b': 'Metformin', 'severity': 'Low', 'description': 'Minor interaction - monitor blood glucose'},
            {'drug_a': 'Atorvastatin', 'drug_b': 'Lisinopril', 'severity': 'None', 'description': 'No significant interaction'}
        ],
        'emergency_events': [
            {'date': '2024-11-10', 'type': 'Dizziness', 'severity': 'Mild', 'resolved': True, 'notes': 'Resolved with rest and hydration'},
            {'date': '2024-11-05', 'type': 'High Blood Pressure', 'severity': 'Moderate', 'resolved': True, 'notes': 'Medication adjusted'}
        ],
        'digital_twin_risk': {
            'current_state': 'Mild Risk',
            'risk_factors': ['Hypertension', 'Age > 40', 'Diabetes'],
            'trend': 'Stable',
            'last_updated': datetime.now()
        }
    }

def create_vitals_chart(vitals_data):
    """Create vitals trend chart"""
    df = pd.DataFrame(vitals_data)
    df['date'] = pd.to_datetime(df['date'])
    
    fig = go.Figure()
    
    # Heart Rate
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['heart_rate'],
        mode='lines+markers', name='Heart Rate (bpm)',
        line=dict(color='#ef4444', width=3)
    ))
    
    # Blood Pressure (Systolic)
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['bp_sys'],
        mode='lines+markers', name='Systolic BP (mmHg)',
        line=dict(color='#3b82f6', width=3), yaxis='y2'
    ))
    
    fig.update_layout(
        title='Vitals Trend (Last 5 Days)',
        xaxis_title='Date',
        yaxis=dict(title='Heart Rate (bpm)', side='left'),
        yaxis2=dict(title='Blood Pressure (mmHg)', side='right', overlaying='y'),
        height=400
    )
    
    return fig

def generate_pdf_report(patient_data, ai_summary):
    """Generate PDF report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor=colors.HexColor('#059669')
    )
    story.append(Paragraph("MediAI Guardian 3.0 - Patient Summary Report", title_style))
    story.append(Spacer(1, 12))
    
    # Patient Info
    story.append(Paragraph("Patient Information", styles['Heading2']))
    patient_info = patient_data['patient_info']
    info_data = [
        ['Patient Name:', patient_info['name']],
        ['Patient ID:', patient_info['patient_id']],
        ['Age:', str(patient_info['age'])],
        ['Gender:', patient_info['gender']],
        ['Primary Condition:', patient_info['primary_condition']],
        ['Report Date:', patient_info['report_date']]
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 12))
    
    # AI Summary
    story.append(Paragraph("AI Analysis Summary", styles['Heading2']))
    story.append(Paragraph(ai_summary['summary'], styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Recommendations
    story.append(Paragraph("AI Recommendations", styles['Heading2']))
    for rec in ai_summary['recommendations']:
        story.append(Paragraph(f"• {rec}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Current Medications
    story.append(Paragraph("Current Medications", styles['Heading2']))
    med_data = [['Medication', 'Dosage', 'Frequency']]
    for med in patient_data['medications']:
        med_data.append([med['name'], med['dosage'], med['frequency']])
    
    med_table = Table(med_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
    med_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(med_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📋 Doctor Summary & Reports</h1>
        <h3>AI-Generated Patient Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate sample data
    patient_data = generate_sample_data()
    
    # Main layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Patient selection (demo)
        st.markdown("### 👤 Select Patient")
        selected_patient = st.selectbox(
            "Choose patient for summary:",
            ["John Doe (P001)", "Jane Smith (P002)", "Robert Johnson (P003)"]
        )
        
        # Generate summary button
        if st.button("🤖 Generate AI Summary", use_container_width=True):
            with st.spinner("Generating comprehensive AI analysis..."):
                # Generate AI summary
                ai_summary = agents['summary'].run(patient_data)
                st.session_state.current_summary = ai_summary
                st.session_state.current_patient_data = patient_data
            
            st.success("✅ AI Summary generated successfully!")
            st.rerun()
        
        # Display summary if generated
        if 'current_summary' in st.session_state:
            summary = st.session_state.current_summary
            
            # AI Summary Section
            st.markdown("### 🤖 AI Analysis Summary")
            st.markdown(f'<div class="summary-section">{summary["summary"]}</div>', 
                       unsafe_allow_html=True)
            
            # Key Metrics
            st.markdown("### 📊 Key Health Metrics")
            
            col_metric1, col_metric2, col_metric3 = st.columns(3)
            
            with col_metric1:
                latest_vitals = patient_data['vitals_history'][0]
                st.metric("💓 Latest Heart Rate", f"{latest_vitals['heart_rate']} bpm")
                st.metric("🌡️ Temperature", f"{latest_vitals['temp']}°F")
            
            with col_metric2:
                st.metric("🩸 Blood Pressure", f"{latest_vitals['bp_sys']}/{latest_vitals['bp_dia']}")
                st.metric("🫁 Oxygen Saturation", f"{latest_vitals['o2_sat']}%")
            
            with col_metric3:
                risk_state = patient_data['digital_twin_risk']['current_state']
                st.metric("🎯 Digital Twin Risk", risk_state)
                st.metric("💊 Active Medications", len(patient_data['medications']))
            
            # Vitals Trend Chart
            st.markdown("### 📈 Vitals Trend Analysis")
            vitals_chart = create_vitals_chart(patient_data['vitals_history'])
            st.plotly_chart(vitals_chart, use_container_width=True)
            
            # AI Recommendations
            st.markdown("### 💡 AI Recommendations")
            for i, rec in enumerate(summary['recommendations'], 1):
                st.markdown(f'<div class="recommendation"><strong>{i}.</strong> {rec}</div>', 
                           unsafe_allow_html=True)
            
            # Medicine Interactions
            st.markdown("### 💊 Drug Interaction Analysis")
            
            for interaction in patient_data['drug_interactions']:
                severity_color = {
                    'High': '#dc2626', 'Medium': '#ea580c', 'Low': '#ca8a04', 'None': '#16a34a'
                }.get(interaction['severity'], '#64748b')
                
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid {severity_color}; margin-bottom: 0.5rem;">
                    <strong>{interaction['drug_a']} + {interaction['drug_b']}</strong><br>
                    <span style="color: {severity_color};">Severity: {interaction['severity']}</span><br>
                    {interaction['description']}
                </div>
                """, unsafe_allow_html=True)
            
            # Emergency Events
            st.markdown("### 🚨 Recent Emergency Events")
            
            if patient_data['emergency_events']:
                for event in patient_data['emergency_events']:
                    status_color = '#16a34a' if event['resolved'] else '#dc2626'
                    status_text = 'Resolved' if event['resolved'] else 'Active'
                    
                    st.markdown(f"""
                    <div class="alert-item">
                        <strong>{event['type']}</strong> - {event['date']}<br>
                        <span style="color: {status_color};">Status: {status_text}</span><br>
                        Severity: {event['severity']}<br>
                        Notes: {event['notes']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No recent emergency events")
    
    with col2:
        # Patient Info Card
        st.markdown("### 👤 Patient Information")
        
        patient_info = patient_data['patient_info']
        st.markdown(f"""
        <div class="summary-section">
            <strong>Name:</strong> {patient_info['name']}<br>
            <strong>ID:</strong> {patient_info['patient_id']}<br>
            <strong>Age:</strong> {patient_info['age']}<br>
            <strong>Gender:</strong> {patient_info['gender']}<br>
            <strong>Condition:</strong> {patient_info['primary_condition']}
        </div>
        """, unsafe_allow_html=True)
        
        # Digital Twin Risk Status
        st.markdown("### 🎯 Digital Twin Status")
        
        risk_data = patient_data['digital_twin_risk']
        risk_color = {
            'Healthy': '#16a34a',
            'Mild Risk': '#ca8a04',
            'High Risk': '#dc2626'
        }.get(risk_data['current_state'], '#64748b')
        
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid {risk_color};">
            <strong>Current State:</strong> {risk_data['current_state']}<br>
            <strong>Trend:</strong> {risk_data['trend']}<br>
            <strong>Last Updated:</strong> {risk_data['last_updated'].strftime('%H:%M:%S')}
        </div>
        """, unsafe_allow_html=True)
        
        # Risk Factors
        st.markdown("**Risk Factors:**")
        for factor in risk_data['risk_factors']:
            st.markdown(f"• {factor}")
        
        # Current Medications
        st.markdown("### 💊 Current Medications")
        
        for med in patient_data['medications']:
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 0.8rem; border-radius: 6px; margin-bottom: 0.5rem;">
                <strong>{med['name']}</strong><br>
                {med['dosage']} - {med['frequency']}
            </div>
            """, unsafe_allow_html=True)
        
        # Action Buttons
        st.markdown("### ⚡ Actions")
        
        if st.button("📊 View Detailed Analytics", use_container_width=True):
            st.info("Detailed analytics view would open here")
        
        if st.button("💊 Medication Management", use_container_width=True):
            st.switch_page("pages/3_Medicine_Reactions.py")
        
        if st.button("🚨 Emergency Protocols", use_container_width=True):
            st.switch_page("pages/4_Emergency_Assistant.py")
        
        # PDF Download
        if 'current_summary' in st.session_state:
            st.markdown("### 📄 Export Report")
            
            if st.button("📥 Download PDF Report", use_container_width=True):
                pdf_buffer = generate_pdf_report(
                    st.session_state.current_patient_data,
                    st.session_state.current_summary
                )
                
                st.download_button(
                    label="📄 Download PDF",
                    data=pdf_buffer,
                    file_name=f"patient_summary_{patient_info['patient_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        
        # Quick Stats
        st.markdown("### 📈 Quick Stats")
        
        st.metric("📅 Days Monitored", "30", delta="5")
        st.metric("💊 Medication Changes", "2", delta="1")
        st.metric("🚨 Emergency Events", len(patient_data['emergency_events']), delta="0")

if __name__ == "__main__":
    main()
