import streamlit as st
import os
from auth import authenticate_user

# Configure page
st.set_page_config(
    page_title="MediAI Guardian 3.0",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar on login page
)

# Custom CSS for modern teal theme
st.markdown("""
<style>
    /* Hide sidebar on login page */
    .css-1d391kg {display: none;}
    
    /* Full screen login layout - 100% fit */
    html, body, [data-testid="stAppViewContainer"] {
        height: 100vh;
        margin: 0;
        padding: 0;
    }
    
    .main .block-container {
        padding: 1rem;
        max-width: 100%;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0891b2 0%, #06b6d4 50%, #22d3ee 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(8, 145, 178, 0.3);
        width: 100%;
    }
    
    .main-header h1 {
        font-size: clamp(2.5rem, 5vw, 4rem);
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header h3 {
        font-size: clamp(1rem, 2.5vw, 1.5rem);
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
    
    .login-container {
        max-width: 600px;
        width: 100%;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #0891b2 0%, #06b6d4 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        width: 100%;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #0e7490 0%, #0891b2 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(8, 145, 178, 0.4);
    }
    
    .role-card {
        background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%);
        border: 2px solid #5eead4;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .role-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(94, 234, 212, 0.3);
        border-color: #2dd4bf;
    }
    
    .role-card h4 {
        font-size: 1.5rem;
        margin: 0;
        color: #0f766e;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #06b6d4;
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem;
        }
        
        .main-header {
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        .login-container {
            padding: 1.5rem;
        }
        
        .role-card {
            height: 80px;
            padding: 1rem;
        }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove default padding */
    .css-18e3th9 {
        padding: 0;
    }
    
    .css-1d391kg {
        padding: 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Check if user is already logged in
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_dashboard()

def show_login_page():
    # Full screen header with attractive name
    st.markdown("""
    <div class="main-header">
        <h1>🧬 MediAI Guardian</h1>
        <h3>Agentic AI-Driven Digital Twin for Real-Time Health & Personal Safety</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Full width login container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    st.markdown("### 🔐 Login to Continue")
    st.markdown("**Select Your Role:**")
    
    # Simplified role cards without descriptions
    col_patient, col_doctor = st.columns(2)
    
    with col_patient:
        st.markdown("""
        <div class="role-card">
            <h4>👤 Patient</h4>
        </div>
        """, unsafe_allow_html=True)
    
    with col_doctor:
        st.markdown("""
        <div class="role-card">
            <h4>👨‍⚕️ Doctor</h4>
        </div>
        """, unsafe_allow_html=True)
    
    # Login form without demo credentials
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            
            submitted = st.form_submit_button("🚀 Login")
            
            if submitted:
                role = authenticate_user(username, password)
                if role:
                    st.session_state.authenticated = True
                    st.session_state.role = role
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    # Show sidebar after login
    st.markdown("""
    <style>
        .css-1d391kg {display: block !important;}
        .css-1lcbmhc {display: block !important;}
        .css-1y4p8pa {display: block !important;}
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation for authenticated users
    st.sidebar.title("🏥 MediAI Guardian 3.0")
    st.sidebar.markdown(f"**Welcome, {st.session_state.username}!**")
    st.sidebar.markdown(f"**Role:** {st.session_state.role.title()}")
    
    # Navigation based on role
    if st.session_state.role == "patient":
        page = st.sidebar.selectbox("Navigate to:", [
            "🏠 Dashboard",
            "🧬 Enhanced Dashboard", 
            "💊 Medicine Reactions", 
            "🚨 Emergency Assistant"
        ])
        
        if page == "🏠 Dashboard":
            st.switch_page("pages/1_Enhanced_Patient_Dashboard.py")
        elif page == "🧬 Enhanced Dashboard":
            st.switch_page("pages/1_Enhanced_Patient_Dashboard.py")
        elif page == "💊 Medicine Reactions":
            st.switch_page("pages/3_Medicine_Reactions.py")
        elif page == "🚨 Emergency Assistant":
            st.switch_page("pages/4_Emergency_Assistant.py")
    
    elif st.session_state.role == "doctor":
        st.markdown("### 👨‍⚕️ Doctor Portal")
        if st.button("🏠 Dashboard", use_container_width=True):
            st.switch_page("pages/2_Doctor_Dashboard.py")
        if st.button("💊 Medicine Reactions", use_container_width=True):
            st.switch_page("pages/3_Medicine_Reactions.py")
        if st.button("🚨 Emergency Assistant", use_container_width=True):
            st.switch_page("pages/4_Emergency_Assistant.py")
        if st.button("📋 Doctor Summary", use_container_width=True):
            st.switch_page("pages/5_Doctor_Summary.py")
            if st.button("💊 Medicine Reactions", use_container_width=True):
                st.switch_page("pages/3_Medicine_Reactions.py")
            if st.button("🚨 Emergency Assistant", use_container_width=True):
                st.switch_page("pages/4_Emergency_Assistant.py")
            if st.button("📋 Doctor Summary", use_container_width=True):
                st.switch_page("pages/5_Doctor_Summary.py")
    
    # Main content
    st.markdown("""
    <div class="main-header">
        <h1>🧬 MediAI Guardian</h1>
        <h3>Welcome to your Medical AI Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.role == "patient":
        st.markdown("### 👤 Patient Portal")
        st.info("Navigate using the sidebar to access your dashboard, medicine reactions, and emergency assistance.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🏠 Go to Dashboard", use_container_width=True):
                st.switch_page("pages/1_Patient_Dashboard.py")
        with col2:
            if st.button("💊 Medicine Reactions", use_container_width=True):
                st.switch_page("pages/3_Medicine_Reactions.py")
        with col3:
            if st.button("🚨 Emergency Assistant", use_container_width=True):
                st.switch_page("pages/4_Emergency_Assistant.py")
    
    elif st.session_state.role == "doctor":
        st.markdown("### 👨‍⚕️ Doctor Portal")
        st.info("Access patient data, generate reports, and monitor emergency situations.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Go to Dashboard", use_container_width=True):
                st.switch_page("pages/2_Doctor_Dashboard.py")
            if st.button("💊 Medicine Reactions", use_container_width=True):
                st.switch_page("pages/3_Medicine_Reactions.py")
        with col2:
            if st.button("🚨 Emergency Assistant", use_container_width=True):
                st.switch_page("pages/4_Emergency_Assistant.py")
            if st.button("📋 Generate Summary", use_container_width=True):
                st.switch_page("pages/5_Doctor_Summary.py")

if __name__ == "__main__":
    main()
