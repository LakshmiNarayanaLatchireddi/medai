import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.vitals_agent import VitalsAgent
from agents.medicine_agent import MedicineAgent
from agents.digital_twin_agent import DigitalTwinAgent

# Configure page
st.set_page_config(
    page_title="MediAI Guardian 3.0 - Enhanced Patient Dashboard",
    page_icon="🧬",
    layout="wide"
)

# ---------- AUTH CHECK ----------
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please login first")
    st.switch_page("app.py")
    st.stop()

if st.session_state.role != "patient":
    st.error("Access denied. This page is for patients only.")
    st.switch_page("app.py")
    st.stop()

# ---------- SESSION STATE ----------
for key, default in [
    ("agent_actions_log", []),
    ("health_alerts", []),
    ("vitals_history", []),
    ("life_saved_counter", 0),
    ("guardian_mode", True),
    ("medicine_history", []),
    ("current_medicine_effect", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ---------- CACHED AGENTS ----------
@st.cache_resource
def get_medicine_agent():
    return MedicineAgent()

# ---------- ENHANCED CSS ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 4s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 1rem 0 0 0;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }
    
    .guardian-status {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 30px;
        font-weight: 700;
        z-index: 1000;
        animation: guardian-pulse 3s ease-in-out infinite;
        box-shadow: 0 8px 30px rgba(16, 185, 129, 0.4);
        backdrop-filter: blur(10px);
    }

    @keyframes guardian-pulse {
        0%, 100% { 
            transform: scale(1); 
            box-shadow: 0 8px 30px rgba(16, 185, 129, 0.4);
        }
        50% { 
            transform: scale(1.05); 
            box-shadow: 0 12px 40px rgba(16, 185, 129, 0.6);
        }
    }

    .dashboard-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 2rem;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .dashboard-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
    }

    .vital-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border: 2px solid transparent;
        transition: all 0.4s ease;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .vital-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, transparent 0%, rgba(255,255,255,0.1) 50%, transparent 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .vital-card:hover::before {
        opacity: 1;
    }
    
    .vital-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }

    .vital-card.normal { 
        border-color: #10b981; 
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    }
    .vital-card.warning { 
        border-color: #f59e0b; 
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
    }
    .vital-card.critical { 
        border-color: #ef4444; 
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        animation: critical-pulse 2s infinite;
    }
    
    @keyframes critical-pulse {
        0%, 100% { box-shadow: 0 8px 25px rgba(239, 68, 68, 0.2); }
        50% { box-shadow: 0 12px 35px rgba(239, 68, 68, 0.4); }
    }

    .heartbeat {
        animation: heartbeat 1.2s ease-in-out infinite;
    }

    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        14% { transform: scale(1.2); }
        28% { transform: scale(1); }
        42% { transform: scale(1.2); }
        70% { transform: scale(1); }
    }

    .digital-twin-panel {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        border-radius: 25px;
        padding: 2rem;
        height: 600px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(14, 165, 233, 0.3);
        border: 3px solid rgba(255,255,255,0.2);
    }
    
    .digital-twin-panel::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #0ea5e9, #3b82f6, #6366f1, #8b5cf6);
        border-radius: 25px;
        z-index: -1;
        animation: gradient-border 3s linear infinite;
    }
    
    @keyframes gradient-border {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .organ-status {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        margin: 0.5rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .organ-status:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }

    .organ-healthy { 
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); 
        color: #166534; 
        border: 2px solid #22c55e;
    }
    .organ-warning { 
        background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%); 
        color: #92400e; 
        border: 2px solid #f59e0b;
    }
    .organ-critical { 
        background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%); 
        color: #991b1b; 
        border: 2px solid #ef4444;
    }

    .agent-log {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #0891b2;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .agent-log:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(8, 145, 178, 0.15);
    }

    .chat-panel {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 2px solid #0891b2;
        position: relative;
        overflow: hidden;
    }
    
    .chat-panel::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #0891b2, #06b6d4);
    }

    .risk-timeline {
        background: linear-gradient(90deg, #10b981 0%, #f59e0b 50%, #ef4444 100%);
        height: 25px;
        border-radius: 15px;
        position: relative;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .alert-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border-left: 5px solid;
        transition: all 0.3s ease;
    }
    
    .alert-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.12);
    }
    
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .floating-refresh {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50%;
        width: 70px;
        height: 70px;
        font-size: 1.8rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        z-index: 1000;
        cursor: pointer;
    }
    
    .floating-refresh:hover {
        transform: scale(1.1) rotate(180deg);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# ---------- RENDER HELPERS ----------

def render_guardian_mode():
    if st.session_state.guardian_mode:
        st.markdown(
            '<div class="guardian-status">🛡️ Guardian Active: Monitoring Health</div>',
            unsafe_allow_html=True,
        )

def render_health_alerts():
    st.markdown('<div class="section-title">🚨 Health Guardian Alerts</div>', unsafe_allow_html=True)
    
    current_alerts = [
        {"type": "warning", "message": "Blood pressure trending upward", "action": "Monitor closely, consider medication", "priority": "High"},
        {"type": "info", "message": "Medicine effect wearing off in 2 hours", "action": "Prepare next dose", "priority": "Medium"},
        {"type": "success", "message": "Heart rate normalized", "action": "Continue current treatment", "priority": "Low"},
    ]
    
    for i, alert in enumerate(current_alerts):
        colors = {
            "warning": {"bg": "#fef3c7", "border": "#f59e0b", "text": "#92400e"},
            "info": {"bg": "#dbeafe", "border": "#0891b2", "text": "#1e40af"},
            "success": {"bg": "#dcfce7", "border": "#10b981", "text": "#166534"}
        }[alert["type"]]
        
        icon = {"warning": "⚠️", "info": "ℹ️", "success": "✅"}[alert["type"]]
        priority_color = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}[alert["priority"]]
        
        st.markdown(
            f"""
            <div class="alert-card" style="border-left-color: {colors['border']}; background: linear-gradient(135deg, {colors['bg']} 0%, white 100%);">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.75rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 1.2rem;">{icon}</span>
                        <strong style="color: {colors['text']}; font-size: 1rem;">{alert['message']}</strong>
                    </div>
                    <span style="background: {priority_color}; color: white; padding: 0.25rem 0.75rem; 
                                border-radius: 20px; font-size: 0.75rem; font-weight: 600;">
                        {alert['priority']}
                    </span>
                </div>
                <div style="color: {colors['text']}; font-size: 0.9rem; opacity: 0.8;">
                    <strong>Action:</strong> {alert['action']}
                </div>
                <div style="margin-top: 0.5rem; font-size: 0.8rem; color: #6b7280;">
                    <span>🕒 {2 + i} minutes ago</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def render_agent_actions_log():
    st.markdown('<div class="section-title">🤖 AI Agent Activity</div>', unsafe_allow_html=True)
    
    agent_actions = [
        {"agent": "DDI Agent", "action": "Checked drug interaction: Lisinopril + Aspirin", "result": "Safe combination", "time": "2 min ago", "status": "success", "icon": "🔬"},
        {"agent": "Digital Twin Agent", "action": "Updated cardiovascular model", "result": "BP trending up", "time": "5 min ago", "status": "warning", "icon": "🧬"},
        {"agent": "Safety Agent", "action": "Risk assessment completed", "result": "Moderate risk detected", "time": "8 min ago", "status": "info", "icon": "🛡️"},
        {"agent": "First-Aid Agent", "action": "Emergency protocol ready", "result": "Standby mode", "time": "10 min ago", "status": "success", "icon": "🚑"},
    ]
    
    for action in agent_actions:
        status_colors = {
            "success": {"bg": "#f0fdf4", "border": "#10b981", "text": "#166534"},
            "warning": {"bg": "#fffbeb", "border": "#f59e0b", "text": "#92400e"},
            "info": {"bg": "#f0f9ff", "border": "#0891b2", "text": "#1e40af"}
        }[action["status"]]
        
        st.markdown(
            f"""
            <div class="agent-log" style="border-left-color: {status_colors['border']}; background: linear-gradient(135deg, {status_colors['bg']} 0%, white 100%);">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.75rem;">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <span style="font-size: 1.5rem;">{action['icon']}</span>
                        <div>
                            <strong style="color: {status_colors['text']}; font-size: 1rem;">{action['agent']}</strong>
                            <div style="color: #6b7280; font-size: 0.85rem; margin-top: 0.25rem;">{action['action']}</div>
                        </div>
                    </div>
                    <span style="color: #9ca3af; font-size: 0.8rem;">{action['time']}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: {status_colors['text']}; font-size: 0.9rem;">✓</span>
                    <span style="color: {status_colors['text']}; font-size: 0.9rem; font-weight: 500;">{action['result']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def render_organ_health_panel():
    st.markdown('<div class="section-title">🫀 Organ Health Matrix</div>', unsafe_allow_html=True)
    
    organs = {
        "Heart": {"status": "healthy", "score": 85, "icon": "❤️", "trend": "stable", "last_check": "5 min ago"},
        "Liver": {"status": "warning", "score": 72, "icon": "🫘", "trend": "declining", "last_check": "3 min ago"},
        "Kidneys": {"status": "healthy", "score": 88, "icon": "🫘", "trend": "improving", "last_check": "7 min ago"},
        "Brain": {"status": "healthy", "score": 92, "icon": "🧠", "trend": "stable", "last_check": "2 min ago"},
    }
    
    cols = st.columns(2)
    for i, (organ, data) in enumerate(organs.items()):
        with cols[i % 2]:
            status_class = {
                "healthy": "organ-healthy",
                "warning": "organ-warning", 
                "critical": "organ-critical",
            }[data["status"]]
            
            trend_icons = {
                "improving": "📈",
                "stable": "➡️", 
                "declining": "📉"
            }
            
            trend_colors = {
                "improving": "#10b981",
                "stable": "#6b7280",
                "declining": "#ef4444"
            }
            
            st.markdown(
                f"""
                <div class="organ-status {status_class}" style="width: 100%; margin: 0.5rem 0; padding: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <span style="font-size: 1.5rem;">{data["icon"]}</span>
                            <strong style="font-size: 1rem;">{organ}</strong>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.2rem; font-weight: 700;">{data["score"]}%</div>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; opacity: 0.8;">
                        <div style="display: flex; align-items: center; gap: 0.25rem;">
                            <span style="color: {trend_colors[data['trend']]};">{trend_icons[data["trend"]]}</span>
                            <span style="color: {trend_colors[data['trend']]};">{data["trend"].title()}</span>
                        </div>
                        <span>🕒 {data["last_check"]}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

def render_enhanced_digital_twin():
    st.markdown('<div class="section-title">🧬 Human Digital Twin (Body View)</div>', unsafe_allow_html=True)
    
    # Get current medicine effect
    medicine_effect = st.session_state.get("current_medicine_effect")
    if medicine_effect:
        effect_color = "#10b981" if medicine_effect["effectiveness"] == "Effective" else "#ef4444"
        target_organ = medicine_effect.get("condition", "General")
        medicine_name = medicine_effect.get("medicine", "Unknown")
    else:
        effect_color = "#64748b"
        target_organ = "None"
        medicine_name = "None"

    # Map condition text to organ flags
    brain_active = "Brain" in target_organ or "Nervous" in target_organ
    heart_active = "Heart" in target_organ or "Cardiovascular" in target_organ
    lung_active = "Lung" in target_organ or "Respiratory" in target_organ
    stomach_active = "Stomach" in target_organ or "Digestive" in target_organ
    liver_active = "Liver" in target_organ or "Digestive" in target_organ
    kidney_active = "Kidney" in target_organ or "Urinary" in target_organ

    # Colors per organ
    def organ_color(active):
        return "#bbf7d0" if active else "#e5e7eb"

    def organ_border(active):
        return "#22c55e" if active else "#94a3b8"

    def organ_shadow(active):
        return "0 0 18px rgba(34, 197, 94, 0.9)" if active else "0 4px 10px rgba(15, 23, 42, 0.25)"

    brain_bg = organ_color(brain_active)
    heart_bg = organ_color(heart_active)
    lung_bg = organ_color(lung_active)
    liver_bg = organ_color(liver_active)
    stomach_bg = organ_color(stomach_active)
    kidney_bg = organ_color(kidney_active)

    brain_border = organ_border(brain_active)
    heart_border = organ_border(heart_active)
    lung_border = organ_border(lung_active)
    liver_border = organ_border(liver_active)
    stomach_border = organ_border(stomach_active)
    kidney_border = organ_border(kidney_active)

    brain_shadow = organ_shadow(brain_active)
    heart_shadow = organ_shadow(heart_active)
    lung_shadow = organ_shadow(lung_active)
    liver_shadow = organ_shadow(liver_active)
    stomach_shadow = organ_shadow(stomach_active)
    kidney_shadow = organ_shadow(kidney_active)

    # Create clean human body using Streamlit columns
    st.markdown("### 👤 Human Body Digital Twin")
    
    # Drug-to-Drug Interaction Selection
    st.markdown("### 💊 Drug Interaction Analysis")
    
    # Medicine selection for interactions
    medicines_list = [
        "Aspirin", "Lisinopril", "Metformin", "Albuterol", 
        "Ibuprofen", "Sertraline", "Warfarin", "Atorvastatin"
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Primary Medicine**")
        medicine1 = st.selectbox(
            "Select first medicine:",
            ["Select medicine..."] + medicines_list,
            key="medicine1_selector"
        )
    
    with col2:
        st.markdown("**Secondary Medicine**")
        medicine2 = st.selectbox(
            "Select second medicine:",
            ["Select medicine..."] + medicines_list,
            key="medicine2_selector"
        )
    
    # Determine which organs are affected by the selected medicines
    medicine_effects = {
        "Aspirin": ["Heart", "Stomach"],
        "Warfarin": ["Heart", "Liver"],
        "Lisinopril": ["Heart", "Kidneys"],
        "Ibuprofen": ["Brain", "Stomach", "Kidneys"],
        "Sertraline": ["Brain"],
        "Metformin": ["Liver", "Stomach"],
        "Albuterol": ["Lungs"],
        "Atorvastatin": ["Liver", "Heart"]
    }
    
    # Update organ activity based on selected medicines
    if medicine1 != "Select medicine..." or medicine2 != "Select medicine...":
        affected_systems = set()
        if medicine1 != "Select medicine..." and medicine1 in medicine_effects:
            affected_systems.update(medicine_effects[medicine1])
        if medicine2 != "Select medicine..." and medicine2 in medicine_effects:
            affected_systems.update(medicine_effects[medicine2])
        
        # Override organ states based on selected medicines
        brain_active = "Brain" in affected_systems
        heart_active = "Heart" in affected_systems
        lung_active = "Lungs" in affected_systems
        stomach_active = "Stomach" in affected_systems
        liver_active = "Liver" in affected_systems
        kidney_active = "Kidneys" in affected_systems
    
    # Create two main columns - body on left, interaction analysis on right
    body_col, interaction_col = st.columns([1, 1])
    
    with body_col:
        st.markdown("**🧑 Human Body View**")
        
        # Enhanced human body visualization
        current_medicines = []
        if medicine1 != "Select medicine...":
            current_medicines.append(medicine1)
        if medicine2 != "Select medicine...":
            current_medicines.append(medicine2)
        
        medicine_display = " + ".join(current_medicines) if current_medicines else "No medicines selected"
        
        st.markdown(
            f"""
            <div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       border-radius: 25px; padding: 2.5rem; margin: 1rem 0; border: 3px solid #4f46e5; 
                       box-shadow: 0 20px 40px rgba(79, 70, 229, 0.3);">
                <div style="background: rgba(255,255,255,0.95); border-radius: 20px; padding: 2rem; 
                           box-shadow: inset 0 4px 20px rgba(0,0,0,0.1);">
                    <div style="font-size: 5rem; margin-bottom: 1rem; 
                               filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));">👨‍⚕️</div>
                    <div style="font-size: 1.4rem; font-weight: 700; color: #4f46e5; margin-bottom: 0.5rem; 
                               text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        Advanced Digital Twin
                    </div>
                    <div style="font-size: 1rem; color: #6366f1; font-weight: 500;">
                        AI-Powered Drug Interaction Monitor
                    </div>
                    <div style="margin-top: 1rem; padding: 0.75rem; background: linear-gradient(90deg, #f0f9ff, #e0f2fe); 
                               border-radius: 12px; border-left: 4px solid #0891b2;">
                        <div style="font-size: 0.9rem; color: #0891b2; font-weight: 600;">
                            {"🟢 Analyzing: " + medicine_display if current_medicines else "⚪ Ready for Drug Selection"}
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Interactive Body Systems using Streamlit components
        st.markdown("### 🫀 Interactive Body Systems")
        st.markdown("*Real-time organ monitoring based on selected medicines*")
        
        # Create container for body systems
        with st.container():
            # Head area - Brain
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if brain_active:
                    st.success("🧠 **Brain** - 🟢 Active")
                else:
                    st.info("🧠 **Brain** - ⚪ Normal")
            
            st.markdown("---")
            
            # Chest area - Lungs and Heart
            chest_col1, chest_col2, chest_col3 = st.columns([1, 1, 1])
            
            with chest_col1:
                if lung_active:
                    st.success("🫁 **Left Lung** - 🟢 Active")
                else:
                    st.info("🫁 **Left Lung** - ⚪ Normal")
            
            with chest_col2:
                if heart_active:
                    st.error("❤️ **Heart** - 🟢 Active")
                else:
                    st.info("❤️ **Heart** - ⚪ Normal")
            
            with chest_col3:
                if lung_active:
                    st.success("🫁 **Right Lung** - 🟢 Active")
                else:
                    st.info("🫁 **Right Lung** - ⚪ Normal")
            
            st.markdown("---")
            
            # Abdomen area - Stomach, Kidneys, Liver
            abdomen_col1, abdomen_col2, abdomen_col3 = st.columns([1, 1, 1])
            
            with abdomen_col1:
                if stomach_active:
                    st.warning("🫄 **Stomach** - 🟢 Active")
                else:
                    st.info("🫄 **Stomach** - ⚪ Normal")
            
            with abdomen_col2:
                if kidney_active:
                    st.success("🫘 **Kidneys** - 🟢 Active")
                else:
                    st.info("🫘 **Kidneys** - ⚪ Normal")
            
            with abdomen_col3:
                if liver_active:
                    st.success("🫘 **Liver** - 🟢 Active")
                else:
                    st.info("🫘 **Liver** - ⚪ Normal")
        
        # Single medicine simulation option
        if (medicine1 != "Select medicine..." or medicine2 != "Select medicine...") and not (medicine1 != "Select medicine..." and medicine2 != "Select medicine..."):
            selected_medicine = medicine1 if medicine1 != "Select medicine..." else medicine2
            st.markdown("### 💊 Single Medicine Analysis")
            st.info(f"**Selected Medicine:** {selected_medicine}")
            
            if st.button(f"🔬 Simulate {selected_medicine} Effects", key="simulate_single_medicine"):
                st.session_state.current_medicine_effect = {
                    "medicine": selected_medicine,
                    "condition": "Single Medicine",
                    "effectiveness": "Effective",
                    "timestamp": datetime.now(),
                }
                st.success(f"✅ **{selected_medicine} simulation activated!** Check the body systems above to see the effects.")
                st.rerun()
    
    with interaction_col:
        st.markdown("**🔬 Drug Interaction Analysis**")
        
        if medicine1 != "Select medicine..." and medicine2 != "Select medicine..." and medicine1 != medicine2:
            # Show interaction analysis
            st.markdown("#### ⚡ Interaction Effects")
        
            # Medicine info cards
            med_col1, med_col2 = st.columns(2)
            
            with med_col1:
                st.markdown(
                    f"""
                    <div style="background: linear-gradient(135deg, #dbeafe, #bfdbfe); border: 2px solid #3b82f6; 
                               border-radius: 15px; padding: 1.5rem; text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">💊</div>
                        <div style="font-size: 1.2rem; font-weight: 700; color: #1d4ed8; margin-bottom: 0.5rem;">
                            {medicine1}
                        </div>
                        <div style="font-size: 0.9rem; color: #1e40af;">
                            Primary Medicine
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with med_col2:
                st.markdown(
                    f"""
                    <div style="background: linear-gradient(135deg, #fef3c7, #fde68a); border: 2px solid #f59e0b; 
                               border-radius: 15px; padding: 1.5rem; text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">💊</div>
                        <div style="font-size: 1.2rem; font-weight: 700; color: #d97706; margin-bottom: 0.5rem;">
                            {medicine2}
                        </div>
                        <div style="font-size: 0.9rem; color: #b45309;">
                            Secondary Medicine
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Interaction analysis
            interaction_data = {
                ("Aspirin", "Warfarin"): {"risk": "High", "effect": "Increased bleeding risk", "color": "#ef4444"},
                ("Aspirin", "Ibuprofen"): {"risk": "Moderate", "effect": "Stomach irritation", "color": "#f59e0b"},
                ("Lisinoprin", "Ibuprofen"): {"risk": "Moderate", "effect": "Reduced blood pressure control", "color": "#f59e0b"},
                ("Sertraline", "Aspirin"): {"risk": "Low", "effect": "Mild bleeding risk", "color": "#10b981"},
                ("Metformin", "Atorvastatin"): {"risk": "Low", "effect": "No significant interaction", "color": "#10b981"},
            }
            
            # Check both directions
            interaction_key = (medicine1, medicine2)
            reverse_key = (medicine2, medicine1)
            
            if interaction_key in interaction_data:
                interaction = interaction_data[interaction_key]
            elif reverse_key in interaction_data:
                interaction = interaction_data[reverse_key]
            else:
                interaction = {"risk": "Unknown", "effect": "Interaction data not available", "color": "#6b7280"}
            
            # Display interaction result
            st.markdown(
                f"""
                <div style="background: white; border: 3px solid {interaction['color']}; border-radius: 15px; 
                           padding: 1.5rem; margin: 1rem 0; text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">
                        {"⚠️" if interaction['risk'] == "High" else "🔶" if interaction['risk'] == "Moderate" else "✅"}
                    </div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: {interaction['color']}; margin-bottom: 0.5rem;">
                        {interaction['risk']} Risk
                    </div>
                    <div style="font-size: 0.9rem; color: #374151;">
                        {interaction['effect']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Simulate interaction button
            if st.button("🔬 Simulate Interaction", key="simulate_interaction"):
                st.session_state.current_medicine_effect = {
                    "medicine": f"{medicine1} + {medicine2}",
                    "condition": "Multiple Systems",
                    "effectiveness": "Monitoring",
                    "timestamp": datetime.now(),
                    "interaction_risk": interaction['risk']
                }
                st.success(f"✅ **Interaction simulation activated!** Monitoring {medicine1} + {medicine2} effects.")
                st.rerun()
        
        elif medicine1 != "Select medicine..." and medicine2 != "Select medicine..." and medicine1 == medicine2:
            st.warning("⚠️ Please select two different medicines to analyze interactions.")
        
        else:
            st.info("👆 Select two different medicines above to analyze their drug-to-drug interactions.")
        
        # Reset button for interactions
        if medicine_effect and hasattr(medicine_effect, 'get') and medicine_effect.get("interaction_risk"):
            if st.button("🔄 Reset Analysis", key="reset_interaction"):
                if 'current_medicine_effect' in st.session_state:
                    del st.session_state.current_medicine_effect
                st.success("✅ **Analysis reset!**")
                st.rerun()
    
    # Medicine pathway section (kept from your previous logic)
    st.markdown("### 💊 Medicine Journey Through Body")
    
    if medicine_effect:
        st.markdown("**📊 System Status**")
        
        # Current status
        if medicine_effect:
            if medicine_effect['effectiveness'] == "Effective":
                st.success("🟢 **Medicine working effectively**")
            else:
                st.warning("🟡 **Monitoring medicine impact**")
            st.info(f"**Medicine:** {medicine_name}")
            st.info(f"**Target:** {target_organ}")
        else:
            st.info("⚪ **Baseline state** - No active medicine simulation")

    # Medicine pathway section (kept from your previous logic)
    st.markdown("### 💊 Medicine Journey Through Body")
    
    if medicine_effect:
        path_col1, path_col2, path_col3, path_col4 = st.columns(4)
        
        with path_col1:
            st.info("**1. INGESTION** 👄\n\nMedicine enters through mouth")
        
        with path_col2:
            st.warning("**2. ABSORPTION** 🫄\n\nStomach processes medicine")
        
        with path_col3:
            st.error("**3. CIRCULATION** ❤️\n\nHeart pumps medicine via blood")
        
        with path_col4:
            st.success("**4. TARGET** 🎯\n\nMedicine reaches target organ")
        
        st.info(f"**💊 Current Medicine:** {medicine_name} → **🎯 Target:** {target_organ}")
        
        if medicine_effect["effectiveness"] == "Effective":
            st.success("✅ **Medicine is working effectively!**")
        else:
            st.warning("⚠️ **Medicine effectiveness needs monitoring**")
        
        # Always show reset button when simulation is active
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Reset Simulation", key="reset_active_simulation"):
                if 'current_medicine_effect' in st.session_state:
                    del st.session_state.current_medicine_effect
                st.success("✅ **Simulation reset!** All organs returned to baseline state.")
                st.rerun()
    else:
        # Medicine Selection for Body Flow Simulation
        st.markdown("### 💊 Select Medicine to See Body Flow")
        
        # Common medicines with their target organs
        medicines_flow = {
            "Select a medicine...": {"target": "None", "pathway": [], "description": ""},
            "Aspirin": {
                "target": "Heart", 
                "pathway": ["Mouth", "Stomach", "Bloodstream", "Heart"],
                "description": "Blood thinner that reduces heart attack risk"
            },
            "Lisinopril": {
                "target": "Heart", 
                "pathway": ["Mouth", "Stomach", "Bloodstream", "Heart", "Kidneys"],
                "description": "ACE inhibitor for blood pressure control"
            },
            "Metformin": {
                "target": "Liver", 
                "pathway": ["Mouth", "Stomach", "Liver", "Bloodstream"],
                "description": "Diabetes medication that controls blood sugar"
            },
            "Albuterol": {
                "target": "Lung", 
                "pathway": ["Inhaler", "Lungs", "Bloodstream"],
                "description": "Bronchodilator for asthma and breathing"
            },
            "Ibuprofen": {
                "target": "Brain", 
                "pathway": ["Mouth", "Stomach", "Bloodstream", "Brain"],
                "description": "Anti-inflammatory pain reliever"
            },
            "Sertraline": {
                "target": "Brain", 
                "pathway": ["Mouth", "Stomach", "Bloodstream", "Brain"],
                "description": "Antidepressant that affects brain chemistry"
            }
        }
        
        selected_med = st.selectbox(
            "Choose a medicine to see how it flows through your body:",
            list(medicines_flow.keys()),
            key="medicine_flow_selector"
        )
        
        if selected_med != "Select a medicine...":
            med_data = medicines_flow[selected_med]
            
            # Show medicine info
            st.info(f"**{selected_med}**: {med_data['description']}")
            
            # Show pathway flow
            st.markdown("### 🔄 Medicine Flow Path")
            
            pathway = med_data['pathway']
            flow_cols = st.columns(len(pathway))
            
            pathway_icons = {
                "Mouth": "👄",
                "Inhaler": "💨", 
                "Stomach": "🫄",
                "Liver": "🫘",
                "Bloodstream": "🩸",
                "Heart": "❤️",
                "Lungs": "🫁",
                "Brain": "🧠",
                "Kidneys": "🫘"
            }
            
            for i, step in enumerate(pathway):
                with flow_cols[i]:
                    icon = pathway_icons.get(step, "💊")
                    st.markdown(
                        f"""
                        <div style="text-align: center; background: #f0f9ff; border: 2px solid #0891b2; 
                                   border-radius: 15px; padding: 1rem; margin: 0.25rem;">
                            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                            <div style="font-size: 0.9rem; font-weight: 600; color: #0891b2;">
                                Step {i+1}
                            </div>
                            <div style="font-size: 0.8rem; color: #374151;">
                                {step}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # Show target effect
            st.success(f"🎯 **Target Reached**: Medicine affects the **{med_data['target']}** system")
            
            # Simulate medicine effect on digital twin
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"💊 Simulate {selected_med} in Body", key="simulate_flow"):
                    st.session_state.current_medicine_effect = {
                        "medicine": selected_med,
                        "condition": med_data['target'],
                        "effectiveness": "Effective",
                        "timestamp": datetime.now(),
                    }
                    st.success(f"✅ **{selected_med}** simulation activated! Check the Digital Twin above to see the effects.")
                    st.rerun()
            
            with col2:
                if st.button("🔄 Reset Simulation", key="reset_simulation"):
                    if 'current_medicine_effect' in st.session_state:
                        del st.session_state.current_medicine_effect
                    st.success("✅ **Simulation reset!** All organs returned to baseline state.")
                    st.rerun()
        else:
            st.info("👆 Select a medicine above to see its journey through your body")
            
            # Show reset button even when no medicine is selected (if there's an active simulation)
            if medicine_effect:
                if st.button("🔄 Reset Current Simulation", key="reset_current"):
                    if 'current_medicine_effect' in st.session_state:
                        del st.session_state.current_medicine_effect
                    st.success("✅ **Simulation reset!** All organs returned to baseline state.")
                    st.rerun()

def render_mediai_chat():
    st.markdown("### 💬 Ask MediAI")
    st.markdown('<div class="chat-panel">', unsafe_allow_html=True)

    user_question = st.text_input(
        "Ask about symptoms, medicines, or health concerns:",
        placeholder="e.g., What are the side effects of my current medication?",
    )
    if user_question:
        responses = {
            "side effects": "Based on your current medications, common side effects may include mild dizziness and dry mouth. Monitor for any unusual symptoms.",
            "symptoms": "Your symptoms suggest monitoring is needed. Track vitals and consult your doctor if they persist.",
            "medicine": "This medication is generally safe for your condition. Continue as prescribed and monitor effectiveness.",
            "default": "I'm analyzing your health data. Based on your current status, I recommend continuing your treatment plan and monitoring vitals regularly.",
        }
        key = next((k for k in responses if k in user_question.lower()), "default")
        st.markdown(
            f"""
            <div style="background: #f0f9ff; padding: 1rem; border-radius: 8px; margin: 1rem 0;
                        border-left: 4px solid #0891b2;">
                <strong>🤖 MediAI:</strong> {responses[key]}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("**🧪 Scenario Simulation**")
    scenario = st.selectbox(
        "Test scenario:",
        [
            "Select a scenario...",
            "What if I take Ibuprofen with my current medication?",
            "What if my blood pressure increases?",
            "What if I miss a dose?",
            "What if I experience chest pain?",
        ],
        key="scenario_selector"
    )
    
    if scenario != "Select a scenario...":
        if st.button("🔬 Run Simulation", key="run_simulation"):
            responses = {
                "What if I take Ibuprofen with my current medication?": {
                    "status": "warning",
                    "message": "⚠️ Moderate interaction detected. Monitor for increased bleeding risk."
                },
                "What if my blood pressure increases?": {
                    "status": "error", 
                    "message": "🚨 High risk scenario. Immediate medical attention recommended."
                },
                "What if I miss a dose?": {
                    "status": "info",
                    "message": "ℹ️ Take next dose as scheduled. Set reminder for future doses."
                },
                "What if I experience chest pain?": {
                    "status": "error",
                    "message": "🚨 Emergency protocol activated. Call 911 immediately."
                }
            }
            
            response = responses.get(scenario, {"status": "success", "message": "✅ Low risk detected. Continue monitoring."})
            
            if response["status"] == "error":
                st.error(response["message"])
            elif response["status"] == "warning":
                st.warning(response["message"])
            elif response["status"] == "info":
                st.info(response["message"])
            else:
                st.success(response["message"])
    else:
        st.info("👆 Please select a scenario above to run simulation")

    st.markdown("</div>", unsafe_allow_html=True)

def render_enhanced_vitals():
    st.markdown('<div class="section-title">📊 Enhanced Vitals Monitor</div>', unsafe_allow_html=True)
    vitals_agent = VitalsAgent()
    current_vitals = vitals_agent.get_current_vitals()
    current_vitals["timestamp"] = datetime.now()
    st.session_state.vitals_history.append(current_vitals)
    if len(st.session_state.vitals_history) > 20:
        st.session_state.vitals_history = st.session_state.vitals_history[-20:]

    vitals_config = {
        "heart_rate": {
            "icon": "💓", 
            "unit": "bpm", 
            "normal": (60, 100), 
            "class": "heartbeat", 
            "name": "Heart Rate",
            "description": "Beats per minute"
        },
        "blood_pressure_systolic": {
            "icon": "🩸", 
            "unit": "mmHg", 
            "normal": (90, 140), 
            "name": "Blood Pressure",
            "description": "Systolic pressure"
        },
        "temperature": {
            "icon": "🌡️", 
            "unit": "°F", 
            "normal": (97, 99), 
            "name": "Body Temperature",
            "description": "Core body temp"
        },
        "oxygen_saturation": {
            "icon": "🫁", 
            "unit": "%", 
            "normal": (95, 100), 
            "name": "Oxygen Saturation",
            "description": "Blood oxygen level"
        },
    }

    cols = st.columns(4)
    
    for i, (vital, config) in enumerate(vitals_config.items()):
        with cols[i]:
            value = current_vitals[vital]
            low, high = config["normal"]
            
            if low <= value <= high:
                status = "normal"
                color = "#10b981"
                bg_color = "linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)"
                border_color = "#10b981"
                status_text = "Normal"
                status_icon = "✅"
            elif value < low * 0.8 or value > high * 1.2:
                status = "critical"
                color = "#ef4444"
                bg_color = "linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)"
                border_color = "#ef4444"
                status_text = "Critical"
                status_icon = "🚨"
            else:
                status = "warning"
                color = "#f59e0b"
                bg_color = "linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)"
                border_color = "#f59e0b"
                status_text = "Warning"
                status_icon = "⚠️"
            
            animation_class = config.get("class", "")
            
            st.markdown(
                f"""
                <div class="vital-card {status}" style="height: 220px; background: {bg_color}; border: 3px solid {border_color}; border-radius: 20px; padding: 1.5rem; display: flex; flex-direction: column; justify-content: space-between; position: relative; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.1); transition: all 0.3s ease;">
                    <div style="position: absolute; top: 10px; right: 10px; background: {color}; color: white; padding: 0.25rem 0.5rem; border-radius: 15px; font-size: 0.7rem; font-weight: 600;">
                        {status_icon} {status_text}
                    </div>
                    <div class="{animation_class}" style="text-align: center; font-size: 4rem; margin-bottom: 0.5rem; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));">
                        {config['icon']}
                    </div>
                    <div style="text-align: center; flex-grow: 1; display: flex; flex-direction: column; justify-content: center;">
                        <div style="color: {color}; font-size: 2.8rem; font-weight: 900; margin: 0; line-height: 1;">
                            {value}
                        </div>
                        <div style="color: {color}; font-size: 1.1rem; font-weight: 700; margin: 0.25rem 0;">
                            {config['unit']}
                        </div>
                    </div>
                    <div style="text-align: center; margin-top: 0.5rem;">
                        <div style="color: #374151; font-size: 1rem; font-weight: 600; margin-bottom: 0.25rem;">
                            {config['name']}
                        </div>
                        <div style="color: #6b7280; font-size: 0.8rem;">
                            {config['description']}
                        </div>
                        <div style="color: #9ca3af; font-size: 0.75rem; margin-top: 0.25rem;">
                            Normal: {low}-{high} {config['unit']}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if len(st.session_state.vitals_history) > 1:
        st.markdown('<div style="margin-top: 2rem;"><div class="section-title">📈 Real-Time Vital Trends</div></div>', unsafe_allow_html=True)
        
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                       border-left: 4px solid #0891b2; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
                <strong>🔗 Live Data Connection:</strong> Displaying trends from the last {len(st.session_state.vitals_history)} readings
                <br><small>📊 Chart updates automatically with each vital sign measurement above</small>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        df = pd.DataFrame(st.session_state.vitals_history)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df["timestamp"], 
            y=df["heart_rate"], 
            name="💓 Heart Rate",
            line=dict(color="#ef4444", width=4, shape='spline'),
            mode='lines+markers',
            marker=dict(size=10, symbol='circle', line=dict(width=2, color='white')),
            hovertemplate="<b>Heart Rate</b><br>%{y} bpm<br>%{x}<extra></extra>"
        ))
        
        fig.add_trace(go.Scatter(
            x=df["timestamp"], 
            y=df["oxygen_saturation"], 
            name="🫁 Oxygen Saturation",
            line=dict(color="#0891b2", width=4, shape='spline'),
            mode='lines+markers',
            marker=dict(size=8, symbol='circle', line=dict(width=2, color='white')),
            hovertemplate="<b>Oxygen Saturation</b><br>%{y}%<br>%{x}<extra></extra>"
        ))
        
        fig.add_trace(go.Scatter(
            x=df["timestamp"], 
            y=df["temperature"], 
            name="🌡️ Temperature",
            line=dict(color="#f59e0b", width=4, shape='spline'),
            mode='lines+markers',
            marker=dict(size=8, symbol='diamond', line=dict(width=2, color='white')),
            hovertemplate="<b>Temperature</b><br>%{y}°F<br>%{x}<extra></extra>"
        ))
        
        fig.add_trace(go.Scatter(
            x=df["timestamp"], 
            y=df["blood_pressure_systolic"], 
            name="🩸 Blood Pressure",
            line=dict(color="#8b5cf6", width=4, shape='spline'),
            mode='lines+markers',
            marker=dict(size=8, symbol='square', line=dict(width=2, color='white')),
            hovertemplate="<b>Blood Pressure</b><br>%{y} mmHg<br>%{x}<extra></extra>"
        ))
        
        fig.update_layout(
            height=400, 
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(248, 250, 252, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=13),
            title=dict(
                text="📊 Live Vital Signs Monitoring Dashboard",
                x=0.5,
                font=dict(size=16, color="#374151")
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="#e5e7eb",
                borderwidth=1
            ),
            hovermode='x unified'
        )
        
        fig.add_hline(y=60, line_dash="dash", line_color="#10b981", opacity=0.3, annotation_text="HR Min Normal")
        fig.add_hline(y=100, line_dash="dash", line_color="#10b981", opacity=0.3, annotation_text="HR Max Normal")
        fig.add_hline(y=95, line_dash="dash", line_color="#0891b2", opacity=0.3, annotation_text="O2 Min Normal")
        
        fig.update_xaxes(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='rgba(0,0,0,0.1)',
            title="Time",
            title_font=dict(size=14)
        )
        fig.update_yaxes(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='rgba(0,0,0,0.1)',
            title="Values",
            title_font=dict(size=14)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_hr = df["heart_rate"].mean()
            st.metric("💓 Avg Heart Rate", f"{avg_hr:.0f} bpm", f"{df['heart_rate'].iloc[-1] - avg_hr:.0f}")
        
        with col2:
            avg_o2 = df["oxygen_saturation"].mean()
            st.metric("🫁 Avg O2 Sat", f"{avg_o2:.1f}%", f"{df['oxygen_saturation'].iloc[-1] - avg_o2:.1f}")
        
        with col3:
            avg_temp = df["temperature"].mean()
            st.metric("🌡️ Avg Temperature", f"{avg_temp:.1f}°F", f"{df['temperature'].iloc[-1] - avg_temp:.1f}")
        
        with col4:
            avg_bp = df["blood_pressure_systolic"].mean()
            st.metric("🩸 Avg BP", f"{avg_bp:.0f} mmHg", f"{df['blood_pressure_systolic'].iloc[-1] - avg_bp:.0f}")

def render_risk_timeline():
    st.markdown("### ⏱️ Risk Timeline")
    risk_time = st.slider("Time perspective:", -24, 24, 0, help="Hours from now")
    if risk_time < 0:
        st.info(f"📊 {abs(risk_time)} hours ago: Risk was moderate due to medication timing")
    elif risk_time == 0:
        st.success("📍 Current: Low risk - all systems stable")
    else:
        st.warning(f"🔮 {risk_time} hours ahead: Projected moderate risk if medication not taken")
    st.markdown(
        """
        <div class="risk-timeline">
            <div style="position: absolute; left: 50%; top: -5px; width: 10px; height: 30px;
                        background: white; border: 2px solid #0891b2; border-radius: 5px;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748b;">
            <span>Past</span><span>Now</span><span>Future</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_drug_interaction_heatmap():
    st.markdown('<div class="section-title">🔥 Medicine Effectiveness & Interaction Analysis</div>', unsafe_allow_html=True)

    # Step 1: Select Health Problem
    st.markdown("**Step 1: Select Your Health Condition**")
    health_conditions = {
        "Select a condition...": [],
        "Hypertension (High Blood Pressure)": ["Lisinopril", "Metoprolol", "Amlodipine", "Hydrochlorothiazide"],
        "Diabetes Type 2": ["Metformin", "Glipizide", "Insulin", "Januvia"],
        "Heart Disease": ["Aspirin", "Metoprolol", "Lisinopril", "Atorvastatin"],
        "Depression/Anxiety": ["Sertraline", "Fluoxetine", "Lorazepam", "Escitalopram"],
        "Asthma/COPD": ["Albuterol", "Prednisone", "Montelukast", "Budesonide"],
        "Arthritis/Pain": ["Ibuprofen", "Naproxen", "Acetaminophen", "Celecoxib"],
        "Blood Clotting Issues": ["Warfarin", "Aspirin", "Clopidogrel", "Rivaroxaban"],
        "Epilepsy/Seizures": ["Gabapentin", "Phenytoin", "Carbamazepine", "Levetiracetam"]
    }
    
    selected_condition = st.selectbox(
        "Choose your health condition:",
        list(health_conditions.keys()),
        key="health_condition_selector"
    )
    
    if selected_condition == "Select a condition...":
        st.info("👆 Please select a health condition to see recommended medicines")
        return
    
    # Step 2: Show recommended medicines for the condition
    recommended_medicines = health_conditions[selected_condition]
    st.markdown(f"**Step 2: Recommended Medicines for {selected_condition}**")
    
    # Allow selection of 2-4 medicines
    selected_medicines = st.multiselect(
        f"Select 2-4 medicines typically used for {selected_condition}:",
        recommended_medicines + ["Other medicines..."],
        key="condition_medicines_selector"
    )
    
    # If "Other medicines..." is selected, show additional options
    if "Other medicines..." in selected_medicines:
        other_medicines = [
            "Digoxin", "Furosemide", "Spironolactone", "Propranolol",
            "Amiodarone", "Diltiazem", "Losartan", "Simvastatin"
        ]
        additional = st.multiselect(
            "Select additional medicines:",
            other_medicines,
            key="additional_medicines_selector"
        )
        selected_medicines = [m for m in selected_medicines if m != "Other medicines..."] + additional
    
    if len(selected_medicines) < 2:
        st.warning("Please select at least **2 medicines** to analyze their effectiveness and interactions.")
        return
    
    if len(selected_medicines) > 4:
        st.info("Using the first 4 medicines selected for better visualization.")
        medicines = selected_medicines[:4]
    else:
        medicines = selected_medicines
    
    # Step 3: Check medicine effectiveness for the condition
    st.markdown(f"**Step 3: Medicine Effectiveness Analysis for {selected_condition}**")
    
    effectiveness_data = {
        "Hypertension (High Blood Pressure)": {
            "Lisinopril": {"effectiveness": 0.9, "description": "Highly effective ACE inhibitor"},
            "Metoprolol": {"effectiveness": 0.85, "description": "Effective beta blocker"},
            "Amlodipine": {"effectiveness": 0.8, "description": "Good calcium channel blocker"},
            "Hydrochlorothiazide": {"effectiveness": 0.75, "description": "Effective diuretic"}
        },
        "Diabetes Type 2": {
            "Metformin": {"effectiveness": 0.9, "description": "First-line treatment, highly effective"},
            "Glipizide": {"effectiveness": 0.7, "description": "Good for blood sugar control"},
            "Insulin": {"effectiveness": 0.95, "description": "Most effective for severe cases"},
            "Januvia": {"effectiveness": 0.75, "description": "Good DPP-4 inhibitor"}
        },
        "Heart Disease": {
            "Aspirin": {"effectiveness": 0.8, "description": "Excellent for prevention"},
            "Metoprolol": {"effectiveness": 0.85, "description": "Reduces heart workload"},
            "Lisinopril": {"effectiveness": 0.8, "description": "Protects heart function"},
            "Atorvastatin": {"effectiveness": 0.9, "description": "Highly effective statin"}
        }
    }
    
    cols = st.columns(len(medicines))
    for i, medicine in enumerate(medicines):
        with cols[i]:
            condition_data = effectiveness_data.get(selected_condition, {})
            med_data = condition_data.get(medicine, {"effectiveness": 0.5, "description": "Effectiveness data not available"})
            
            effectiveness = med_data["effectiveness"]
            description = med_data["description"]
            
            if effectiveness >= 0.8:
                color = "#10b981"
                status = "Highly Effective"
            elif effectiveness >= 0.6:
                color = "#f59e0b"
                status = "Moderately Effective"
            else:
                color = "#ef4444"
                status = "Less Effective"
            
            st.markdown(
                f"""
                <div style="background: white; border: 2px solid {color}; border-radius: 15px; 
                           padding: 1rem; text-align: center; margin-bottom: 1rem;">
                    <h4 style="color: {color}; margin: 0;">{medicine}</h4>
                    <div style="font-size: 1.5rem; font-weight: bold; color: {color}; margin: 0.5rem 0;">
                        {int(effectiveness * 100)}%
                    </div>
                    <div style="font-size: 0.8rem; color: {color}; font-weight: 600;">
                        {status}
                    </div>
                    <div style="font-size: 0.75rem; color: #6b7280; margin-top: 0.5rem;">
                        {description}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("**Step 4: Medicine Interaction & Safety Matrix**")
    
    agent = get_medicine_agent()
    
    n = len(medicines)
    interaction_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    effectiveness_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    hover_text = [["" for _ in range(n)] for _ in range(n)]
    
    severity_to_score = {
        "None": 0.0, "Safe": 0.0, "Low": 0.2, "Minor": 0.2,
        "Medium": 0.6, "Moderate": 0.6, "High": 1.0, "Severe": 1.0
    }
    
    for i in range(n):
        for j in range(n):
            if i == j:
                condition_data = effectiveness_data.get(selected_condition, {})
                med_data = condition_data.get(medicines[i], {"effectiveness": 0.5})
                effectiveness_matrix[i][j] = med_data["effectiveness"]
                interaction_matrix[i][j] = 0.0
                hover_text[i][j] = f"{medicines[i]}<br>Effectiveness: {int(med_data['effectiveness'] * 100)}%<br>For {selected_condition}"
            else:
                try:
                    result = agent.run(medicines[i], medicines[j])
                    severity = result.get("severity", "None")
                    explanation = result.get("explanation", "No interaction data")
                except Exception:
                    severity = "None"
                    explanation = "Unable to check interaction"
                
                score = severity_to_score.get(severity, 0.0)
                interaction_matrix[i][j] = score
                hover_text[i][j] = f"{medicines[i]} + {medicines[j]}<br>Interaction: {severity}<br>{explanation[:100]}..."
    
    fig = go.Figure(
        data=go.Heatmap(
            z=interaction_matrix,
            x=medicines,
            y=medicines,
            text=hover_text,
            hoverinfo="text",
            colorscale=[
                [0.0, "#10b981"],
                [0.3, "#22c55e"],
                [0.6, "#f59e0b"],
                [0.8, "#ef4444"],
                [1.0, "#dc2626"],
            ],
            zmin=0,
            zmax=1,
            showscale=True,
            colorbar=dict(
                title=dict(text="Risk Level", side="right"),
                tickmode="array",
                tickvals=[0, 0.2, 0.6, 1.0],
                ticktext=["Safe", "Low", "Moderate", "High"]
            )
        )
    )
    
    fig.update_layout(
        title=f"Medicine Safety Matrix for {selected_condition}",
        height=400,
        margin=dict(l=50, r=50, t=50, b=50),
        xaxis_title="Medicine",
        yaxis_title="Medicine",
        font=dict(family="Inter", size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("**📋 Analysis Summary**")
    
    total_interactions = 0
    high_risk_interactions = 0
    
    for i in range(n):
        for j in range(n):
            if i != j:
                total_interactions += 1
                if interaction_matrix[i][j] >= 0.6:
                    high_risk_interactions += 1
    
    if total_interactions > 0:
        safety_percentage = int(((total_interactions - high_risk_interactions) / total_interactions) * 100)
    else:
        safety_percentage = 100
    
    if safety_percentage >= 80:
        safety_color = "#10b981"
        safety_status = "✅ Generally Safe Combination"
    elif safety_percentage >= 60:
        safety_color = "#f59e0b"
        safety_status = "⚠️ Use with Caution"
    else:
        safety_color = "#ef4444"
        safety_status = "🚨 High Risk - Consult Doctor"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div style="background: white; border: 2px solid {safety_color}; border-radius: 15px; 
                       padding: 1rem; text-align: center;">
                <h4 style="color: {safety_color}; margin: 0;">Overall Safety</h4>
                <div style="font-size: 2rem; font-weight: bold; color: {safety_color};">
                    {safety_percentage}%
                </div>
                <div style="font-size: 0.8rem; color: {safety_color};">
                    {safety_status}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        avg_effectiveness = sum(effectiveness_data.get(selected_condition, {}).get(med, {"effectiveness": 0.5})["effectiveness"] for med in medicines) / len(medicines)
        eff_percentage = int(avg_effectiveness * 100)
        
        st.markdown(
            f"""
            <div style="background: white; border: 2px solid #0891b2; border-radius: 15px; 
                       padding: 1rem; text-align: center;">
                <h4 style="color: #0891b2; margin: 0;">Treatment Effectiveness</h4>
                <div style="font-size: 2rem; font-weight: bold; color: #0891b2;">
                    {eff_percentage}%
                </div>
                <div style="font-size: 0.8rem; color: #0891b2;">
                    For {selected_condition}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div style="background: white; border: 2px solid #6366f1; border-radius: 15px; 
                       padding: 1rem; text-align: center;">
                <h4 style="color: #6366f1; margin: 0;">Medicines Selected</h4>
                <div style="font-size: 2rem; font-weight: bold; color: #6366f1;">
                    {len(medicines)}
                </div>
                <div style="font-size: 0.8rem; color: #6366f1;">
                    Active Medications
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    if high_risk_interactions > 0:
        st.error(f"⚠️ **Warning**: {high_risk_interactions} high-risk interaction(s) detected. Consult your healthcare provider before combining these medications.")
    else:
        st.success("✅ **Good News**: No high-risk interactions detected among selected medicines.")
    
    st.info("💡 **Recommendation**: Always consult with your healthcare provider before starting, stopping, or changing any medications, especially when combining multiple drugs.")

def render_medicine_simulation():
    st.markdown("### 💊 Medicine Simulation")

    medicines_by_condition = {
        "Heart/Cardiovascular": {
            "Lisinopril": "ACE inhibitor for high blood pressure",
            "Metoprolol": "Beta blocker for heart conditions",
            "Amlodipine": "Calcium channel blocker",
        },
        "Brain/Nervous System": {
            "Sertraline": "Antidepressant affecting neurotransmitters",
            "Gabapentin": "Nerve pain medication",
        },
        "Lungs/Respiratory": {
            "Albuterol": "Bronchodilator for asthma",
            "Prednisone": "Anti-inflammatory for respiratory conditions",
        },
    }

    selected_condition = st.selectbox(
        "Select the body part/condition:",
        ["None"] + list(medicines_by_condition.keys())
    )

    if selected_condition != "None":
        available = medicines_by_condition[selected_condition]
        selected_medicine = st.selectbox(
            f"Choose medicine for {selected_condition}:",
            ["None"] + list(available.keys())
        )

        if selected_medicine != "None":
            st.info(f"**{selected_medicine}**: {available[selected_medicine]}")

            if st.button("💊 Simulate Medicine Intake"):
                effectiveness = "Effective"
                st.session_state.current_medicine_effect = {
                    "medicine": selected_medicine,
                    "condition": selected_condition,
                    "effectiveness": effectiveness,
                    "timestamp": datetime.now(),
                }
                st.session_state.medicine_history.append(
                    {
                        "medicine": selected_medicine,
                        "condition": selected_condition,
                        "effectiveness": effectiveness,
                        "timestamp": datetime.now(),
                        "risk_level": "Low",
                    }
                )
                st.success(f"✅ **Body Response**: Medicine effectively targeting {selected_condition}")
                st.rerun()

    if st.session_state.current_medicine_effect:
        if st.button("🔄 Clear Medicine Effects"):
            st.session_state.current_medicine_effect = None
            st.rerun()

    if st.session_state.medicine_history:
        st.markdown("### 📋 Recent Medicine History")
        history_df = pd.DataFrame(st.session_state.medicine_history)
        history_df["timestamp"] = pd.to_datetime(history_df["timestamp"])
        history_df = history_df.sort_values("timestamp", ascending=False).head(5)
        for _, row in history_df.iterrows():
            icon = "✅" if row["effectiveness"] == "Effective" else "❌"
            with st.expander(f"{icon} {row['medicine']} - {row['timestamp'].strftime('%H:%M:%S')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Medicine:** {row['medicine']}")
                    st.write(f"**Target:** {row['condition']}")
                with col2:
                    st.write(f"**Effectiveness:** {row['effectiveness']}")
                    st.write(f"**Risk Level:** {row['risk_level']}")

# ---------- MAIN ----------

def main():
    render_guardian_mode()

    st.markdown(
        f"""
        <div class="main-header">
            <h1>🧬 MediAI Guardian</h1>
            <p>Advanced Patient Health Dashboard • AI-Powered Digital Twin • Real-Time Monitoring</p>
            <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1.5rem; flex-wrap: wrap;">
                <div style="text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.25rem;">{st.session_state.username}</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">Patient ID</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.25rem;">{st.session_state.life_saved_counter}</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">Lives Protected</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.25rem;">98.5%</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">System Uptime</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.25rem;">24/7</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">Monitoring</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    render_enhanced_vitals()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    render_organ_health_panel()
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        render_enhanced_digital_twin()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        render_mediai_chat()
        st.markdown('</div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        render_health_alerts()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        render_agent_actions_log()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    render_risk_timeline()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    render_drug_interaction_heatmap()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    render_medicine_simulation()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <button class="floating-refresh" onclick="window.location.reload();" title="Refresh Dashboard">
            🔄
        </button>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
