import streamlit as st
import sys
import os
from datetime import datetime
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.emergency_agent import EmergencyAgent
from agents.digital_twin_agent import DigitalTwinAgent

# Configure page
st.set_page_config(
    page_title="Emergency Assistant - MediAI Guardian 3.0",
    page_icon="🚨",
    layout="wide"
)

# Check authentication
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please login first")
    st.switch_page("app.py")
    st.stop()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #dc2626 0%, #ef4444 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .emergency-button {
        background: linear-gradient(90deg, #dc2626 0%, #ef4444 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 2rem;
        font-size: 1.2rem;
        font-weight: bold;
        width: 100%;
        margin: 1rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .emergency-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(220, 38, 38, 0.4);
    }
    .first-aid-step {
        background: #fef2f2;
        border-left: 4px solid #dc2626;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
    .safety-alert {
        background: linear-gradient(90deg, #dc2626 0%, #ef4444 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    .glb-emergency {
        filter: hue-rotate(0deg) saturate(2) brightness(1.3);
        box-shadow: 0 0 40px rgba(239, 68, 68, 0.9);
        animation: emergency-glow 1.5s ease-in-out infinite alternate;
    }
    @keyframes emergency-glow {
        from { box-shadow: 0 0 40px rgba(239, 68, 68, 0.9); }
        to { box-shadow: 0 0 60px rgba(239, 68, 68, 1); }
    }
    .status-monitoring {
        background: linear-gradient(90deg, #f59e0b 0%, #fbbf24 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .status-stable {
        background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize agents
@st.cache_resource
def get_agents():
    return {
        'emergency': EmergencyAgent(),
        'digital_twin': DigitalTwinAgent()
    }

agents = get_agents()

# Initialize session state
if 'emergency_active' not in st.session_state:
    st.session_state.emergency_active = False

if 'emergency_history' not in st.session_state:
    st.session_state.emergency_history = []

if 'current_emergency' not in st.session_state:
    st.session_state.current_emergency = None

def simulate_emergency(emergency_type):
    """Simulate an emergency scenario"""
    # Get AI response for emergency
    emergency_response = agents['emergency'].run(emergency_type)
    
    # Update digital twin
    twin_update = agents['digital_twin'].run("emergency", {
        'type': emergency_type,
        'severity': 'High',
        'timestamp': datetime.now()
    })
    
    # Store emergency data
    emergency_data = {
        'type': emergency_type,
        'timestamp': datetime.now(),
        'response': emergency_response,
        'status': 'Active',
        'twin_state': twin_update['risk_level']
    }
    
    st.session_state.current_emergency = emergency_data
    st.session_state.emergency_active = True
    st.session_state.emergency_history.append(emergency_data)
    
    return emergency_data

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚨 Emergency Assistant</h1>
        <h3>AI-Powered Emergency Response System</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Emergency status indicator
    if st.session_state.emergency_active:
        st.markdown("""
        <div class="safety-alert">
            🚨 EMERGENCY ACTIVE 🚨<br>
            Follow the first-aid instructions below
        </div>
        """, unsafe_allow_html=True)
    
    # Main layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🚨 Emergency Simulation")
        st.info("Click on an emergency type to simulate the scenario and receive AI-powered first-aid guidance")
        
        # Emergency type buttons
        emergency_types = [
            {"type": "Fainting", "icon": "😵", "description": "Sudden loss of consciousness"},
            {"type": "Chest Pain", "icon": "💔", "description": "Acute chest discomfort or pain"},
            {"type": "Dizziness", "icon": "😵‍💫", "description": "Feeling lightheaded or unsteady"},
            {"type": "Difficulty Breathing", "icon": "🫁", "description": "Shortness of breath or breathing problems"},
            {"type": "Severe Headache", "icon": "🤕", "description": "Intense head pain"},
            {"type": "Allergic Reaction", "icon": "🤧", "description": "Severe allergic response"}
        ]
        
        for emergency in emergency_types:
            if st.button(f"{emergency['icon']} {emergency['type']}", 
                        key=f"emergency_{emergency['type']}", 
                        help=emergency['description'],
                        use_container_width=True):
                emergency_data = simulate_emergency(emergency['type'])
                st.rerun()
        
        # Emergency controls
        st.markdown("---")
        col_control1, col_control2 = st.columns(2)
        
        with col_control1:
            if st.button("📞 Call 911", disabled=not st.session_state.emergency_active):
                st.success("🚑 Emergency services have been notified!")
                st.balloons()
        
        with col_control2:
            if st.button("✅ Mark Resolved", disabled=not st.session_state.emergency_active):
                if st.session_state.current_emergency:
                    st.session_state.current_emergency['status'] = 'Resolved'
                    st.session_state.emergency_active = False
                    
                    # Update digital twin to stable
                    agents['digital_twin'].run("emergency_resolved", {})
                    
                    st.success("✅ Emergency marked as resolved")
                    st.rerun()
        
        # Current emergency details
        if st.session_state.current_emergency and st.session_state.emergency_active:
            emergency = st.session_state.current_emergency
            
            st.markdown("### 🆘 Current Emergency")
            st.error(f"**Type:** {emergency['type']}")
            st.write(f"**Started:** {emergency['timestamp'].strftime('%H:%M:%S')}")
            st.write(f"**Status:** {emergency['status']}")
            
            # First-aid instructions
            st.markdown("### 🏥 AI First-Aid Instructions")
            
            response = emergency['response']
            
            # Safety alert
            if response.get('safety_alert'):
                st.markdown(f"""
                <div class="safety-alert">
                    ⚠️ SAFETY ALERT ⚠️<br>
                    {response['safety_alert']}
                </div>
                """, unsafe_allow_html=True)
            
            # Step-by-step instructions
            if response.get('steps'):
                st.markdown("**Follow these steps:**")
                for i, step in enumerate(response['steps'], 1):
                    st.markdown(f"""
                    <div class="first-aid-step">
                        <strong>Step {i}:</strong> {step}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Additional recommendations
            if response.get('recommendations'):
                st.markdown("### 💡 Additional Recommendations")
                for rec in response['recommendations']:
                    st.info(f"• {rec}")
            
            # When to call emergency services
            if response.get('call_911_if'):
                st.markdown("### 📞 Call 911 Immediately If:")
                for condition in response['call_911_if']:
                    st.error(f"🚨 {condition}")
    
    with col2:
        # 3D Digital Twin with emergency visualization
        st.markdown("### 🧬 Digital Twin - Emergency Status")
        
        if st.session_state.emergency_active:
            # Emergency state with pulsing red glow
            st.markdown("""
            <div style="background: #fef2f2; border-radius: 15px; padding: 1rem; text-align: center;">
                <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
                <model-viewer 
                    src="HumanBody.glb"
                    alt="Digital Twin - Emergency State"
                    camera-controls
                    auto-rotate
                    class="glb-emergency"
                    style="width:100%; height:400px; background-color: #fef2f2;"
                    exposure="1.3"
                    shadow-intensity="2">
                </model-viewer>
                <p style="margin-top: 1rem; color: #dc2626; font-weight: bold; font-size: 1.1rem;">
                    🚨 EMERGENCY STATE ACTIVE 🚨
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Normal state
            st.markdown("""
            <div style="background: #f0fdf4; border-radius: 15px; padding: 1rem; text-align: center;">
                <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
                <model-viewer 
                    src="HumanBody.glb"
                    alt="Digital Twin - Normal State"
                    camera-controls
                    auto-rotate
                    style="width:100%; height:400px; background-color: #f0fdf4; filter: hue-rotate(120deg) saturate(1.1) brightness(1.05);"
                    exposure="1"
                    shadow-intensity="1">
                </model-viewer>
                <p style="margin-top: 1rem; color: #16a34a; font-weight: bold;">
                    ✅ Normal State - No Active Emergencies
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Emergency status panel
        st.markdown("### 📊 Emergency Status")
        
        if st.session_state.emergency_active:
            st.markdown('<div class="status-monitoring">⚠️ MONITORING - Emergency in Progress</div>', 
                       unsafe_allow_html=True)
            
            # Timer since emergency started
            if st.session_state.current_emergency:
                start_time = st.session_state.current_emergency['timestamp']
                elapsed = datetime.now() - start_time
                minutes = int(elapsed.total_seconds() // 60)
                seconds = int(elapsed.total_seconds() % 60)
                st.metric("⏱️ Time Elapsed", f"{minutes:02d}:{seconds:02d}")
        else:
            st.markdown('<div class="status-stable">✅ STABLE - All Systems Normal</div>', 
                       unsafe_allow_html=True)
        
        # Emergency history
        st.markdown("### 📋 Emergency History")
        
        if st.session_state.emergency_history:
            # Show last 5 emergencies
            for emergency in reversed(st.session_state.emergency_history[-5:]):
                status_color = "#dc2626" if emergency['status'] == 'Active' else "#16a34a"
                
                with st.expander(f"🚨 {emergency['type']} - {emergency['timestamp'].strftime('%H:%M:%S')}"):
                    col_hist1, col_hist2 = st.columns(2)
                    
                    with col_hist1:
                        st.write(f"**Type:** {emergency['type']}")
                        st.write(f"**Time:** {emergency['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    with col_hist2:
                        st.write(f"**Status:** {emergency['status']}")
                        st.write(f"**Twin State:** {emergency['twin_state']}")
                    
                    if emergency['response'].get('steps'):
                        st.write("**First Aid Steps Provided:**")
                        for i, step in enumerate(emergency['response']['steps'][:3], 1):
                            st.write(f"{i}. {step}")
        else:
            st.info("No emergency events recorded")
        
        # Emergency contacts (demo)
        st.markdown("### 📞 Emergency Contacts")
        
        contacts = [
            {"name": "Emergency Services", "number": "911", "type": "🚑"},
            {"name": "Primary Care Doctor", "number": "(555) 123-4567", "type": "👨‍⚕️"},
            {"name": "Hospital", "number": "(555) 987-6543", "type": "🏥"},
            {"name": "Emergency Contact", "number": "(555) 456-7890", "type": "👤"}
        ]
        
        for contact in contacts:
            st.markdown(f"""
            <div style="background: white; padding: 0.8rem; border-radius: 8px; border-left: 4px solid #dc2626; margin-bottom: 0.5rem;">
                {contact['type']} <strong>{contact['name']}</strong><br>
                📞 {contact['number']}
            </div>
            """, unsafe_allow_html=True)
    
    # Auto-refresh for active emergencies
    if st.session_state.emergency_active:
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    main()
