import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.medicine_agent import MedicineAgent
from agents.digital_twin_agent import DigitalTwinAgent
from agents.enhanced_ai_coordinator import AgenticAICoordinator

# Configure page
st.set_page_config(
    page_title="Medicine Reactions - MediAI Guardian 3.0",
    page_icon="💊",
    layout="wide"
)

# Check authentication
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please login first")
    st.switch_page("app.py")
    st.stop()

# Enhanced Modern CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
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
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 1rem 0 0 0;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    .step-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(102, 126, 234, 0.1);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .step-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .step-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .step-title {
        color: #1f2937;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .medicine-selector {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .medicine-selector:hover {
        border-color: #667eea;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
    }
    
    .selected-medicine {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 2px solid #3b82f6;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s ease;
    }
    
    .selected-medicine:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.2);
    }
    
    .severity-high {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(220, 38, 38, 0.3);
        animation: pulse-red 2s infinite;
    }
    
    @keyframes pulse-red {
        0%, 100% { box-shadow: 0 10px 25px rgba(220, 38, 38, 0.3); }
        50% { box-shadow: 0 15px 35px rgba(220, 38, 38, 0.5); }
    }
    
    .severity-medium {
        background: linear-gradient(135deg, #ea580c 0%, #f97316 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(234, 88, 12, 0.3);
        animation: pulse-orange 2s infinite;
    }
    
    @keyframes pulse-orange {
        0%, 100% { box-shadow: 0 10px 25px rgba(234, 88, 12, 0.3); }
        50% { box-shadow: 0 15px 35px rgba(234, 88, 12, 0.5); }
    }
    
    .severity-low {
        background: linear-gradient(135deg, #ca8a04 0%, #eab308 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(202, 138, 4, 0.3);
    }
    
    .no-interaction {
        background: linear-gradient(135deg, #16a34a 0%, #22c55e 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(22, 163, 74, 0.3);
    }
    
    .glb-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .glb-container:hover {
        border-color: #667eea;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.15);
    }
    
    .affected-area {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 2px solid #fecaca;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .affected-area:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(254, 202, 202, 0.3);
    }
    
    .interaction-heatmap {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
    }
    
    .digital-twin-panel {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 15px 35px rgba(14, 165, 233, 0.1);
        border: 2px solid #0ea5e9;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .digital-twin-panel::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #0ea5e9, #3b82f6, #6366f1, #8b5cf6);
        border-radius: 20px;
        z-index: -1;
        animation: gradient-border 3s linear infinite;
    }
    
    @keyframes gradient-border {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .history-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .history-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .warning-banner {
        background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
        border: 2px solid #f59e0b;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        animation: gentle-glow 2s infinite alternate;
    }
    
    @keyframes gentle-glow {
        0% { box-shadow: 0 5px 15px rgba(245, 158, 11, 0.2); }
        100% { box-shadow: 0 8px 25px rgba(245, 158, 11, 0.4); }
    }
    
    .success-banner {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 2px solid #10b981;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .info-card {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 2px solid #3b82f6;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .floating-action {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 1.5rem;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    .floating-action:hover {
        transform: scale(1.1) rotate(10deg);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# Initialize agents
@st.cache_resource
def get_agents():
    return {
        'medicine': MedicineAgent(),
        'digital_twin': DigitalTwinAgent()
    }

agents = get_agents()

# Load drug interactions data
@st.cache_data
def load_drug_data():
    try:
        # Try multiple paths for the CSV file
        possible_paths = [
            'db_drug_interactions.csv',  # Original file in root
            'data/drug_interactions.csv',  # Data directory
            'drug_interactions.csv'  # Current directory
        ]
        
        df = None
        for csv_path in possible_paths:
            if os.path.exists(csv_path):
                print(f"Loading drugs from: {csv_path}")
                df = pd.read_csv(csv_path)
                break
        
        if df is not None:
            # Get unique drugs and limit for performance
            drug1_list = df['Drug 1'].dropna().unique().tolist()
            drug2_list = df['Drug 2'].dropna().unique().tolist()
            all_drugs = sorted(list(set(drug1_list + drug2_list)))
            
            # Filter out very long names and prioritize common drugs
            drugs = []
            
            # First, add common/recognizable drug names
            common_patterns = [
                'insulin', 'aspirin', 'ibuprofen', 'acetaminophen', 'advil', 'tylenol',
                'metformin', 'lisinopril', 'atorvastatin', 'amlodipine', 'omeprazole',
                'warfarin', 'digoxin', 'furosemide', 'hydrochlorothiazide', 'losartan',
                'sertraline', 'fluoxetine', 'lorazepam', 'gabapentin', 'prednisone'
            ]
            
            # Add drugs that match common patterns first
            for drug in all_drugs:
                if len(drug) < 50:  # Reasonable length
                    drug_lower = drug.lower()
                    if any(pattern in drug_lower for pattern in common_patterns):
                        drugs.append(drug)
            
            # Then add other drugs up to limit
            for drug in all_drugs:
                if len(drug) < 50 and drug not in drugs:
                    drugs.append(drug)
                    if len(drugs) >= 1000:  # Increase limit
                        break
            
            # Add essential drugs if missing
            essential_drugs = [
                "Insulin", "Aspirin", "Ibuprofen", "Acetaminophen", "Advil", "Tylenol",
                "Metformin", "Lisinopril", "Atorvastatin", "Warfarin", "Digoxin"
            ]
            
            for essential in essential_drugs:
                if essential not in drugs:
                    drugs.append(essential)
            
            drugs = sorted(drugs)
            print(f"Loaded {len(drugs)} unique drugs (prioritized common medications)")
            return df, drugs
        else:
            raise FileNotFoundError("No CSV file found")
            
    except Exception as e:
        print(f"Error loading drug data: {e}")
        # Fallback data if CSV not found
        return None, [
            "Aspirin", "Ibuprofen", "Acetaminophen", "Lisinopril", "Metformin", 
            "Atorvastatin", "Amlodipine", "Omeprazole", "Levothyroxine", "Warfarin",
            "Simvastatin", "Hydrochlorothiazide", "Losartan", "Gabapentin", "Sertraline",
            "Citalopram", "Tramadol", "Prednisone", "Albuterol", "Furosemide",
            "Digoxin", "Verteporfin", "Trioxsalen", "Aminolevulinic acid", "Titanium dioxide"
        ]

def get_affected_body_areas(drug_interaction):
    """Map drug interactions to affected body areas"""
    interaction_text = drug_interaction.lower()
    
    areas = []
    
    # Cardiovascular
    if any(word in interaction_text for word in ['heart', 'cardiac', 'blood pressure', 'circulation']):
        areas.append("❤️ Cardiovascular System")
    
    # Nervous System
    if any(word in interaction_text for word in ['nervous', 'brain', 'seizure', 'depression', 'anxiety']):
        areas.append("🧠 Nervous System")
    
    # Digestive System
    if any(word in interaction_text for word in ['stomach', 'liver', 'digestive', 'nausea', 'gastric']):
        areas.append("🫄 Digestive System")
    
    # Respiratory System
    if any(word in interaction_text for word in ['lung', 'respiratory', 'breathing', 'asthma']):
        areas.append("🫁 Respiratory System")
    
    # Kidney/Urinary
    if any(word in interaction_text for word in ['kidney', 'renal', 'urinary', 'bladder']):
        areas.append("🫘 Kidney/Urinary System")
    
    # Skin
    if any(word in interaction_text for word in ['skin', 'rash', 'photosensitizing', 'dermal']):
        areas.append("🧴 Skin/Integumentary System")
    
    # Blood/Hematologic
    if any(word in interaction_text for word in ['blood', 'bleeding', 'clotting', 'anticoagulant']):
        areas.append("🩸 Blood/Hematologic System")
    
    return areas if areas else ["⚠️ General Systemic Effect"]

def main():
    # Enhanced Header with Animation
    st.markdown('''
    <div class="main-header">
        <h1>🧬 MediAI Guardian 3.0</h1>
        <p>🔬 Advanced Medicine Reactions & Drug Interactions Analysis</p>
        <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
            ⚡ AI-Powered • 🎯 Real-Time Analysis • 🛡️ Safety First
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Load drug data
    interactions_df, available_drugs = load_drug_data()

    # Session state for dynamic medicine selection
    if 'selected_drugs' not in st.session_state:
        st.session_state.selected_drugs = []
    
    # Step 1: Health Condition Selection with Enhanced UI
    st.markdown('''
    <div class="step-card">
        <div class="step-title">🏥 Step 1: Select Your Health Condition</div>
        <p style="color: #6b7280; margin-bottom: 1.5rem;">Choose the medical condition you're currently treating to get personalized medicine recommendations.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    health_conditions = {
        "Hypertension (High Blood Pressure)": {
            "description": "Elevated blood pressure requiring medication",
            "recommended_drugs": ["Lisinopril", "Amlodipine", "Losartan", "Hydrochlorothiazide", "Metoprolol"],
            "body_part": "Heart/Cardiovascular"
        },
        "Diabetes": {
            "description": "Blood sugar regulation disorder",
            "recommended_drugs": ["Metformin", "Insulin", "Glipizide", "Pioglitazone", "Sitagliptin"],
            "body_part": "Pancreas/Liver"
        },
        "High Cholesterol": {
            "description": "Elevated cholesterol levels",
            "recommended_drugs": ["Atorvastatin", "Simvastatin", "Rosuvastatin", "Pravastatin", "Lovastatin"],
            "body_part": "Liver/Cardiovascular"
        },
        "Depression/Anxiety": {
            "description": "Mental health condition requiring medication",
            "recommended_drugs": ["Sertraline", "Fluoxetine", "Escitalopram", "Lorazepam", "Alprazolam"],
            "body_part": "Brain/Nervous System"
        },
        "Pain/Inflammation": {
            "description": "Acute or chronic pain requiring treatment",
            "recommended_drugs": ["Ibuprofen", "Aspirin", "Acetaminophen", "Naproxen", "Diclofenac"],
            "body_part": "Multiple/Systemic"
        },
        "Heart Disease": {
            "description": "Cardiovascular conditions requiring medication",
            "recommended_drugs": ["Warfarin", "Digoxin", "Carvedilol", "Enalapril", "Furosemide"],
            "body_part": "Heart/Cardiovascular"
        }
    }
    
    selected_condition = st.selectbox(
        "What health condition are you treating?",
        ["None"] + list(health_conditions.keys())
    )
    
    if selected_condition != "None":
        condition_info = health_conditions[selected_condition]
        
        # Enhanced condition info display
        st.markdown(f'''
        <div class="info-card">
            <h4 style="margin: 0 0 0.5rem 0; color: #1f2937;">📋 {selected_condition}</h4>
            <p style="margin: 0 0 1rem 0; color: #4b5563;">{condition_info['description']}</p>
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                <span style="background: #dbeafe; color: #1e40af; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; font-weight: 500;">🎯 Target: {condition_info['body_part']}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Show recommended drugs in a modern layout
        st.markdown("### 💊 Recommended Medications")
        
        # Create columns for better layout
        cols = st.columns(2)
        for i, drug in enumerate(condition_info['recommended_drugs']):
            with cols[i % 2]:
                st.markdown(f'''
                <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); 
                           border: 1px solid #bbf7d0; border-radius: 10px; padding: 1rem; margin: 0.5rem 0;
                           transition: all 0.3s ease;" 
                     onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(34, 197, 94, 0.15)';"
                     onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='none';">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 1.2rem;">💊</span>
                        <strong style="color: #166534;">{drug}</strong>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced layout with better proportions
    col1, col2 = st.columns([1.2, 0.8])
    
    with col1:
        # Enhanced Drug Selection Section
        st.markdown('''
        <div class="step-card">
            <div class="step-title">💊 Step 2: Select Your Medications</div>
            <p style="color: #6b7280; margin-bottom: 1.5rem;">Add up to 2 medications to check for potential interactions and safety concerns.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Enhanced drug count display
        st.markdown(f'''
        <div style="background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%); 
                   border: 2px solid #0ea5e9; border-radius: 12px; padding: 1rem; margin: 1rem 0;
                   text-align: center;">
            <div style="font-size: 1.1rem; font-weight: 600; color: #0c4a6e; margin-bottom: 0.5rem;">
                📊 Database Status
            </div>
            <div style="color: #0369a1; font-size: 0.9rem;">
                {len(available_drugs):,} medications available for analysis
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Add common drugs if not in list
        common_drugs_to_add = [
            "Insulin", "Advil", "Tylenol", "Motrin", "Aleve", "Benadryl", 
            "Claritin", "Zyrtec", "Pepcid", "Tums", "Robitussin", "Sudafed"
        ]
        missing_common = [drug for drug in common_drugs_to_add if drug not in available_drugs]
        if missing_common:
            st.warning(f"⚠️ Adding common drugs not found in database: {', '.join(missing_common)}")
            available_drugs.extend(missing_common)
        
        # Deduplicate and sort
        available_drugs = sorted(list(dict.fromkeys(available_drugs)))
        
        # Enhanced medicine selector
        st.markdown('''
        <div class="medicine-selector">
            <h4 style="margin: 0 0 1rem 0; color: #1f2937; display: flex; align-items: center; gap: 0.5rem;">
                <span>🔍</span> Medicine Selector
            </h4>
            <p style="color: #6b7280; margin-bottom: 1rem; font-size: 0.9rem;">
                Search and select medications from our comprehensive database
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        new_drug = st.selectbox(
            "🔍 Select a medicine to add:",
            ["None"] + available_drugs,
            key="medicine_add_select",
            help="Choose from over 1000+ medications in our database"
        )
        
        if st.button("➕ Add Medicine", key="add_medicine_button"):
            if new_drug == "None":
                st.warning("Please select a medicine before adding.")
            else:
                if new_drug in st.session_state.selected_drugs:
                    st.info(f"{new_drug} is already added.")
                elif len(st.session_state.selected_drugs) >= 2:
                    st.warning("You can only compare two medicines at a time.")
                else:
                    st.session_state.selected_drugs.append(new_drug)
                    st.success(f"Added {new_drug} to your list.")
            st.rerun()
        
        # Enhanced selected medicines display
        if st.session_state.selected_drugs:
            st.markdown('''
            <div style="margin: 1.5rem 0;">
                <h4 style="color: #1f2937; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                    <span>💊</span> Selected Medications
                </h4>
            </div>
            ''', unsafe_allow_html=True)
            
            for i, drug in enumerate(list(st.session_state.selected_drugs)):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f'''
                    <div class="selected-medicine">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <span style="background: #3b82f6; color: white; border-radius: 50%; width: 24px; height: 24px; 
                                        display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: 600;">
                                {i+1}
                            </span>
                            <div>
                                <div style="font-weight: 600; color: #1f2937;">{drug}</div>
                                <div style="font-size: 0.8rem; color: #6b7280;">Ready for analysis</div>
                            </div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                with c2:
                    if st.button("🗑️", key=f"remove_{drug}", help=f"Remove {drug}"):
                        st.session_state.selected_drugs.remove(drug)
                        st.rerun()
        else:
            st.markdown('''
            <div class="warning-banner">
                <div style="text-align: center;">
                    <div style="font-size: 1.1rem; font-weight: 600; color: #92400e; margin-bottom: 0.5rem;">
                        🎯 Ready to Start
                    </div>
                    <div style="color: #a16207; font-size: 0.9rem;">
                        Add up to 2 medications to check for potential interactions
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Map to existing variable names for the rest of the code
        selected_drugs = st.session_state.selected_drugs
        drug_a = selected_drugs[0] if len(selected_drugs) >= 1 else "None"
        drug_b = selected_drugs[1] if len(selected_drugs) >= 2 else "None"
        
        # Doctor Prescription Override Feature
        st.markdown("### 👨‍⚕️ Doctor Prescription Override")
        st.markdown("*If your doctor prescribed different medicines, you can check them here*")
        
        with st.expander("🔍 Check Doctor's Prescription", expanded=False):
            st.markdown("**Enter the medicine your doctor prescribed:**")
            doctor_prescribed = st.text_input("Doctor's Prescribed Medicine:", placeholder="Enter medicine name...")
            
            if doctor_prescribed and selected_condition != "None":
                # Check if doctor's prescription is appropriate
                recommended_drugs = health_conditions[selected_condition]['recommended_drugs']
                is_appropriate = doctor_prescribed in recommended_drugs
                
                col_check1, col_check2 = st.columns(2)
                
                with col_check1:
                    if is_appropriate:
                        st.success(f"✅ **CORRECT PRESCRIPTION**")
                        st.success(f"{doctor_prescribed} is appropriate for {selected_condition}")
                        st.info("**Expected Benefits:**")
                        st.write("• Effective treatment for your condition")
                        st.write("• Minimal side effects when used correctly")
                        st.write("• Proven therapeutic benefit")
                    else:
                        st.error(f"⚠️ **POTENTIALLY INCORRECT PRESCRIPTION**")
                        st.error(f"{doctor_prescribed} may not be optimal for {selected_condition}")
                        
                        # Show what could happen with wrong medicine
                        st.warning("**⚠️ Potential Consequences:**")
                        
                        # Define wrong medicine consequences
                        wrong_medicine_effects = {
                            "Hypertension (High Blood Pressure)": {
                                "consequences": [
                                    "Blood pressure may remain uncontrolled",
                                    "Risk of heart attack or stroke increases",
                                    "Kidney damage may progress",
                                    "Cardiovascular complications possible"
                                ],
                                "symptoms": "Headaches, dizziness, chest pain, shortness of breath"
                            },
                            "Diabetes": {
                                "consequences": [
                                    "Blood sugar levels may remain high",
                                    "Risk of diabetic complications increases",
                                    "Nerve damage (neuropathy) may develop",
                                    "Eye and kidney problems possible"
                                ],
                                "symptoms": "Excessive thirst, frequent urination, fatigue, blurred vision"
                            },
                            "High Cholesterol": {
                                "consequences": [
                                    "Cholesterol levels may not improve",
                                    "Increased risk of heart disease",
                                    "Arterial plaque buildup continues",
                                    "Risk of heart attack increases"
                                ],
                                "symptoms": "Usually no symptoms until complications occur"
                            },
                            "Depression/Anxiety": {
                                "consequences": [
                                    "Mental health symptoms may worsen",
                                    "Risk of self-harm may increase",
                                    "Daily functioning may deteriorate",
                                    "Social isolation may worsen"
                                ],
                                "symptoms": "Worsening mood, increased anxiety, sleep problems, loss of interest"
                            },
                            "Pain/Inflammation": {
                                "consequences": [
                                    "Pain may not be adequately controlled",
                                    "Inflammation may persist or worsen",
                                    "Mobility may be further limited",
                                    "Quality of life may decrease"
                                ],
                                "symptoms": "Continued pain, swelling, stiffness, reduced mobility"
                            },
                            "Heart Disease": {
                                "consequences": [
                                    "Heart function may not improve",
                                    "Risk of heart failure increases",
                                    "Arrhythmias may develop",
                                    "Life-threatening complications possible"
                                ],
                                "symptoms": "Chest pain, shortness of breath, fatigue, irregular heartbeat"
                            }
                        }
                        
                        condition_effects = wrong_medicine_effects.get(selected_condition, {
                            "consequences": [
                                "Treatment may be ineffective",
                                "Condition may worsen over time",
                                "Side effects without benefits",
                                "Delayed proper treatment"
                            ],
                            "symptoms": "Condition-specific symptoms may persist or worsen"
                        })
                        
                        for consequence in condition_effects["consequences"]:
                            st.write(f"• {consequence}")
                        
                        st.info(f"**Watch for these symptoms:** {condition_effects['symptoms']}")
                
                with col_check2:
                    st.markdown("**💡 Recommended Alternatives:**")
                    st.write("**Appropriate medicines for your condition:**")
                    for drug in recommended_drugs[:3]:  # Show top 3 alternatives
                        st.write(f"• {drug}")
                    
                    st.markdown("**🏥 Next Steps:**")
                    if not is_appropriate:
                        st.write("1. **Consult your doctor** about the prescription")
                        st.write("2. **Ask about alternatives** from the recommended list")
                        st.write("3. **Don't stop current medication** without doctor approval")
                        st.write("4. **Monitor symptoms** closely")
                        st.write("5. **Seek second opinion** if concerned")
                    else:
                        st.write("1. **Follow doctor's instructions** exactly")
                        st.write("2. **Take medication as prescribed**")
                        st.write("3. **Monitor for side effects**")
                        st.write("4. **Regular follow-up** with doctor")
        
        # Check if selected drugs are appropriate for the condition
        if selected_condition != "None" and drug_a != "None":
            is_drug_a_appropriate = drug_a in health_conditions[selected_condition]['recommended_drugs']
            if is_drug_a_appropriate:
                st.success(f"✅ {drug_a} is recommended for {selected_condition}")
            else:
                st.warning(f"⚠️ {drug_a} may not be optimal for {selected_condition}")
        
        if selected_condition != "None" and drug_b != "None":
            is_drug_b_appropriate = drug_b in health_conditions[selected_condition]['recommended_drugs']
            if is_drug_b_appropriate:
                st.success(f"✅ {drug_b} is recommended for {selected_condition}")
            else:
                st.warning(f"⚠️ {drug_b} may not be optimal for {selected_condition}")
        
        # Enhanced submit button
        button_disabled = len(selected_drugs) != 2
        button_text = "🧪 Analyze Drug Interaction" if not button_disabled else f"Add {2-len(selected_drugs)} more medicine(s) to analyze"
        
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
        
        if st.button(
            button_text, 
            disabled=button_disabled,
            help="Analyze potential interactions between your selected medications" if not button_disabled else "You need exactly 2 medications to perform analysis",
            type="primary" if not button_disabled else "secondary"
        ):
            if len(selected_drugs) == 2:
                interaction_result = agents['medicine'].run(drug_a, drug_b)
                
                # Store result in session state with condition context
                st.session_state.current_interaction = {
                    'drug_a': drug_a,
                    'drug_b': drug_b,
                    'condition': selected_condition,
                    'result': interaction_result,
                    'timestamp': datetime.now()
                }
                
                # Add to interaction history
                if 'interaction_history' not in st.session_state:
                    st.session_state.interaction_history = []
                
                st.session_state.interaction_history.append(st.session_state.current_interaction)
                
                # Update digital twin
                new_state = agents['digital_twin'].run("drug_interaction", {
                    'drug_a': drug_a,
                    'drug_b': drug_b,
                    'condition': selected_condition,
                    'interaction': interaction_result
                })
                
                st.rerun()
        
        # Enhanced interaction results display
        if 'current_interaction' in st.session_state:
            interaction = st.session_state.current_interaction
            result = interaction['result']
            
            # Modern results header
            st.markdown('''
            <div class="step-card" style="margin-top: 2rem;">
                <div class="step-title">📊 Interaction Analysis Results</div>
                <p style="color: #6b7280; margin-bottom: 1rem;">Comprehensive analysis of drug interactions and safety profile</p>
            </div>
            ''', unsafe_allow_html=True)
            
            # Enhanced drug combination display
            st.markdown(f'''
            <div style="background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
                       border: 2px solid #d1d5db; border-radius: 15px; padding: 1.5rem; margin: 1rem 0;
                       text-align: center;">
                <div style="font-size: 1.2rem; font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">
                    🔬 Analyzing Drug Combination
                </div>
                <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                    <span style="background: #3b82f6; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 500;">
                        {interaction['drug_a']}
                    </span>
                    <span style="font-size: 1.5rem; color: #6b7280;">+</span>
                    <span style="background: #8b5cf6; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 500;">
                        {interaction['drug_b']}
                    </span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Severity indicator
            severity = result['severity']
            if severity == "High" or severity == "Severe":
                st.markdown(f'<div class="severity-high">🚨 HIGH SEVERITY INTERACTION</div>', 
                           unsafe_allow_html=True)
            elif severity == "Medium" or severity == "Moderate":
                st.markdown(f'<div class="severity-medium">⚠️ MODERATE INTERACTION</div>', 
                           unsafe_allow_html=True)
            elif severity == "Low" or severity == "Minor":
                st.markdown(f'<div class="severity-low">⚡ MINOR INTERACTION</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="no-interaction">✅ NO SIGNIFICANT INTERACTION</div>', 
                           unsafe_allow_html=True)

            # Enhanced Interaction Heatmap
            st.markdown('''
            <div class="interaction-heatmap">
                <h4 style="margin: 0 0 1rem 0; color: #1f2937; display: flex; align-items: center; gap: 0.5rem;">
                    <span>🌡️</span> Interaction Risk Matrix
                </h4>
                <p style="color: #6b7280; margin-bottom: 1rem; font-size: 0.9rem;">
                    Visual representation of interaction severity between medications
                </p>
            </div>
            ''', unsafe_allow_html=True)
            
            severity_scores = {
                'High': 3, 'Severe': 3,
                'Medium': 2, 'Moderate': 2,
                'Low': 1, 'Minor': 1,
                'None': 0
            }
            score = severity_scores.get(severity, 0)
            z = [[0, score], [score, 0]]
            labels = [interaction['drug_a'], interaction['drug_b']]
            
            fig = go.Figure(data=go.Heatmap(
                z=z,
                x=labels,
                y=labels,
                colorscale=[
                    [0.0, '#10b981'],   # green (safe)
                    [0.33, '#f59e0b'],  # yellow (low)
                    [0.66, '#f97316'],  # orange (medium)
                    [1.0, '#ef4444']    # red (high)
                ],
                zmin=0,
                zmax=3,
                showscale=True,
                colorbar=dict(
                    title="Risk Level",
                    tickvals=[0, 1, 2, 3],
                    ticktext=["Safe", "Low", "Medium", "High"]
                )
            ))
            
            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, b=40, t=40),
                xaxis_title="Medicine",
                yaxis_title="Medicine",
                font=dict(size=12),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed explanation
            if result['explanation']:
                st.markdown("### 📝 Detailed Explanation")
                st.write(result['explanation'])
                
                # Affected body areas
                affected_areas = get_affected_body_areas(result['explanation'])
                if affected_areas:
                    st.markdown("### 🎯 Affected Body Systems")
                    for area in affected_areas:
                        st.markdown(f'<div class="affected-area">{area}</div>', 
                                   unsafe_allow_html=True)
                
                # Update digital twin
                twin_update = agents['digital_twin'].run("drug_interaction", {
                    'drug_a': interaction['drug_a'],
                    'drug_b': interaction['drug_b'],
                    'severity': severity,
                    'explanation': result['explanation']
                })
                
                # Recommendations
                st.markdown("### 💡 AI Recommendations")
                if severity in ["High", "Severe"]:
                    st.error("🚨 **AVOID THIS COMBINATION** - Consult healthcare provider immediately")
                    st.write("• Consider alternative medications")
                    st.write("• Monitor for adverse effects if combination is necessary")
                    st.write("• Adjust dosages under medical supervision")
                elif severity in ["Medium", "Moderate"]:
                    st.warning("⚠️ **USE WITH CAUTION** - Monitor closely")
                    st.write("• Regular monitoring recommended")
                    st.write("• Watch for side effects")
                    st.write("• Consider timing of administration")
                elif severity in ["Low", "Minor"]:
                    st.info("⚡ **MINOR INTERACTION** - Generally safe")
                    st.write("• Monitor for mild side effects")
                    st.write("• No major precautions needed")
                else:
                    st.success("✅ **SAFE COMBINATION** - No significant interactions")
                    st.write("• No special precautions needed")
                    st.write("• Continue as prescribed")
        
        # Quick drug search and browser
        st.markdown("### 🔍 Drug Search & Browser")
        
        # Show sample of available drugs
        with st.expander("📋 Browse Available Drugs (Sample)", expanded=False):
            st.write("**Common medications available:**")
            sample_drugs = [drug for drug in available_drugs if any(common in drug.lower() 
                          for common in ['insulin', 'aspirin', 'ibuprofen', 'acetaminophen', 'metformin', 
                                       'lisinopril', 'atorvastatin', 'warfarin', 'digoxin', 'omeprazole'])][:20]
            
            if sample_drugs:
                for i, drug in enumerate(sample_drugs):
                    bc1, bc2 = st.columns([3, 1])
                    with bc1:
                        st.write(f"• {drug}")
                    with bc2:
                        if st.button("Select", key=f"browse_{drug}_{i}"):
                            # Add drug into selected list (up to 2)
                            if drug in st.session_state.selected_drugs:
                                st.info(f"{drug} already selected.")
                            elif len(st.session_state.selected_drugs) >= 2:
                                st.warning("You can only compare two medicines at a time.")
                            else:
                                st.session_state.selected_drugs.append(drug)
                            st.rerun()
            else:
                st.write("Loading drugs from database...")
        
        # Search functionality
        search_term = st.text_input("🔍 Search for a specific drug:", placeholder="Type: insulin, advil, tylenol, etc...")
        
        if search_term and len(search_term) >= 2:
            matching_drugs = [drug for drug in available_drugs if search_term.lower() in drug.lower()]
            if matching_drugs:
                st.success(f"**Found {len(matching_drugs)} matching drugs:**")
                
                # Show first 15 matches in a more organized way
                for i, drug in enumerate(matching_drugs[:15]):
                    sc1, sc2 = st.columns([3, 1])
                    with sc1:
                        st.write(f"• {drug}")
                    with sc2:
                        if st.button("Select", key=f"search_{drug}_{i}"):
                            if drug in st.session_state.selected_drugs:
                                st.info(f"{drug} already selected.")
                            elif len(st.session_state.selected_drugs) >= 2:
                                st.warning("You can only compare two medicines at a time.")
                            else:
                                st.session_state.selected_drugs.append(drug)
                            st.rerun()
                            
                if len(matching_drugs) > 15:
                    st.info(f"Showing first 15 of {len(matching_drugs)} matches. Type more characters to narrow down.")
            else:
                st.error(f"❌ No drugs found matching '{search_term}'")
                st.info("💡 Try searching for: insulin, aspirin, ibuprofen, advil, tylenol, metformin")
        elif search_term and len(search_term) < 2:
            st.info("Type at least 2 characters to search.")
        
        # Show what's actually in the database
        if st.button("🔍 Debug: Show First 20 Drugs in Database"):
            st.write("**First 20 drugs loaded from database:**")
            for i, drug in enumerate(available_drugs[:20]):
                st.write(f"{i+1}. {drug}")
    
    with col2:
        # Enhanced 3D Digital Twin Section
        st.markdown('''
        <div class="digital-twin-panel">
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <h3 style="margin: 0; color: #0c4a6e; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                    <span>🧬</span> 3D Digital Twin
                </h3>
                <p style="color: #0369a1; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                    Real-time visualization of medicine effects on the human body
                </p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Show medicine entering body animation
        if 'current_interaction' in st.session_state:
            interaction = st.session_state.current_interaction
            result = interaction['result']
            condition = interaction.get('condition', 'None')
            
            # Determine body part affected based on condition
            body_part_effects = {
                "Hypertension (High Blood Pressure)": {
                    "target": "Heart/Cardiovascular System",
                    "color": "#ef4444",  # Red for heart
                    "animation": "heartbeat"
                },
                "Diabetes": {
                    "target": "Pancreas/Liver",
                    "color": "#f59e0b",  # Orange for liver/pancreas
                    "animation": "glow"
                },
                "High Cholesterol": {
                    "target": "Liver/Blood Vessels",
                    "color": "#8b5cf6",  # Purple for liver
                    "animation": "pulse"
                },
                "Depression/Anxiety": {
                    "target": "Brain/Nervous System",
                    "color": "#06b6d4",  # Cyan for brain
                    "animation": "spark"
                },
                "Pain/Inflammation": {
                    "target": "Multiple Body Areas",
                    "color": "#10b981",  # Green for systemic
                    "animation": "wave"
                },
                "Heart Disease": {
                    "target": "Heart/Cardiovascular System",
                    "color": "#dc2626",  # Dark red for heart
                    "animation": "heartbeat"
                }
            }
            
            # Get effect info
            effect_info = body_part_effects.get(condition, {
                "target": "General Body",
                "color": "#6b7280",
                "animation": "glow"
            })
            
            # Determine interaction severity color overlay
            severity = result.get('severity', 'Low')  # Default to 'Low'
            if severity == 'High':
                interaction_color = "rgba(239, 68, 68, 0.8)"  # Red
                warning_text = "🚨 HIGH RISK INTERACTION"
                bg_color = "#fef2f2"
            elif severity == 'Medium':
                interaction_color = "rgba(249, 115, 22, 0.7)"  # Orange
                warning_text = "⚠️ MODERATE INTERACTION"
                bg_color = "#fff7ed"
            elif severity == 'Low':
                interaction_color = "rgba(234, 179, 8, 0.6)"  # Yellow
                warning_text = "⚡ MINOR INTERACTION"
                bg_color = "#fefce8"
            else:
                interaction_color = "rgba(16, 185, 129, 0.6)"  # Green
                warning_text = "✅ SAFE COMBINATION"
                bg_color = "#f0fdf4"
            
            # Show medicine pathway animation
            st.markdown(f"""
            <div style="background: {bg_color}; border-radius: 15px; padding: 1rem; margin-bottom: 1rem;">
                <h4 style="color: #374151; margin: 0;">💊 Medicine Pathway</h4>
                <p style="margin: 0.5rem 0; color: #6b7280;">
                    <strong>Target:</strong> {effect_info['target']}<br>
                    <strong>Drugs:</strong> {interaction['drug_a']} + {interaction['drug_b']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Try GLB model
            glb_file_path = "HumanBody.glb"
            if os.path.exists(glb_file_path):
                import base64
                with open(glb_file_path, 'rb') as f:
                    glb_data = f.read()
                glb_base64 = base64.b64encode(glb_data).decode()
                glb_data_url = f"data:model/gltf-binary;base64,{glb_base64}"
                
                st.markdown(f"""
                <div class="glb-container" style="border: 2px solid {interaction_color}; border-radius: 15px; padding: 1rem; position: relative;">
                    <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
                    <model-viewer 
                        src="{glb_data_url}"
                        alt="Digital Twin - Medicine Effects"
                        camera-controls
                        auto-rotate
                        loading="eager"
                        reveal="auto"
                        style="width:100%; height:450px; background-color: {bg_color}; 
                               filter: hue-rotate({0 if severity == 'High' else 30 if severity == 'Medium' else 60 if severity == 'Low' else 120}deg) 
                               saturate(1.3) brightness(1.1); 
                               box-shadow: inset 0 0 30px {interaction_color}; 
                               animation: medicine-effect 3s ease-in-out infinite;
                               border-radius: 10px;"
                        exposure="1.2"
                        shadow-intensity="2"
                        camera-orbit="0deg 75deg 2m"
                        field-of-view="30deg">
                        <div slot="progress-bar" style="
                            position: absolute;
                            top: 50%;
                            left: 50%;
                            transform: translate(-50%, -50%);
                            color: {interaction_color};
                            font-size: 1.2rem;
                        ">Loading 3D Model...</div>
                    </model-viewer>
                    
                    <div style="
                        position: absolute;
                        top: 20px;
                        left: 20px;
                        background: rgba(255,255,255,0.9);
                        padding: 0.5rem;
                        border-radius: 8px;
                        font-size: 0.9rem;
                        color: #374151;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    ">
                        🎯 Targeting: {effect_info['target']}
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Fallback visualization
                st.markdown(f"""
                <div class="glb-container" style="border: 2px solid {interaction_color}; border-radius: 15px; padding: 1rem; position: relative;">
                    <div style="
                        width: 100%;
                        height: 450px;
                        background: linear-gradient(135deg, {bg_color} 0%, #ffffff 100%);
                        border-radius: 10px;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        position: relative;
                        overflow: hidden;
                        animation: medicine-effect 3s ease-in-out infinite;
                        box-shadow: inset 0 0 30px {interaction_color};
                    ">
                        <div style="
                            font-size: 12rem;
                            animation: body-pulse 2s ease-in-out infinite;
                            filter: hue-rotate({0 if severity == 'High' else 30 if severity == 'Medium' else 60 if severity == 'Low' else 120}deg);
                        ">🧬</div>
                        
                        <div style="
                            position: absolute;
                            top: 20%;
                            left: 50%;
                            transform: translateX(-50%);
                            font-size: 2rem;
                            animation: organ-pulse 1.5s ease-in-out infinite;
                        ">
                            {'❤️' if 'Heart' in effect_info['target'] else 
                             '🫘' if 'Liver' in effect_info['target'] or 'Kidney' in effect_info['target'] else
                             '🧠' if 'Brain' in effect_info['target'] else
                             '🫁' if 'Lung' in effect_info['target'] else
                             '🫄' if 'Stomach' in effect_info['target'] else '⚕️'}
                        </div>
                        
                        <div class="medicine-particles">
                            <div style="
                                position: absolute;
                                width: 8px;
                                height: 8px;
                                background: {interaction_color};
                                border-radius: 50%;
                                animation: particle-1 3s ease-in-out infinite;
                                box-shadow: 0 0 10px {interaction_color};
                            "></div>
                            <div style="
                                position: absolute;
                                width: 6px;
                                height: 6px;
                                background: {interaction_color};
                                border-radius: 50%;
                                animation: particle-2 3.5s ease-in-out infinite 0.5s;
                                box-shadow: 0 0 8px {interaction_color};
                            "></div>
                            <div style="
                                position: absolute;
                                width: 10px;
                                height: 10px;
                                background: {interaction_color};
                                border-radius: 50%;
                                animation: particle-3 4s ease-in-out infinite 1s;
                                box-shadow: 0 0 12px {interaction_color};
                            "></div>
                        </div>
                        
                        <div style="
                            position: absolute;
                            bottom: 20px;
                            left: 50%;
                            transform: translateX(-50%);
                            background: rgba(255,255,255,0.9);
                            padding: 0.5rem 1rem;
                            border-radius: 20px;
                            font-size: 0.9rem;
                            color: #374151;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        ">
                            🎯 Medicine targeting: {effect_info['target']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # CSS animations
            st.markdown(f"""
            <style>
            @keyframes medicine-effect {{
                0%, 100% {{ 
                    box-shadow: inset 0 0 30px {interaction_color}, 0 0 20px {interaction_color}; 
                    transform: scale(1);
                }}
                50% {{ 
                    box-shadow: inset 0 0 50px {interaction_color}, 0 0 40px {interaction_color}; 
                    transform: scale(1.02);
                }}
            }}
            @keyframes body-pulse {{
                0%, 100% {{ transform: scale(1); opacity: 0.8; }}
                50% {{ transform: scale(1.1); opacity: 1; }}
            }}
            @keyframes organ-pulse {{
                0%, 100% {{ transform: translateX(-50%) scale(1); opacity: 0.7; }}
                50% {{ transform: translateX(-50%) scale(1.2); opacity: 1; }}
            }}
            @keyframes particle-1 {{
                0% {{ top: 10%; left: 20%; opacity: 0; }}
                50% {{ top: 50%; left: 80%; opacity: 1; }}
                100% {{ top: 90%; left: 30%; opacity: 0; }}
            }}
            @keyframes particle-2 {{
                0% {{ top: 20%; left: 80%; opacity: 0; }}
                50% {{ top: 60%; left: 20%; opacity: 1; }}
                100% {{ top: 80%; left: 70%; opacity: 0; }}
            }}
            @keyframes particle-3 {{
                0% {{ top: 30%; left: 50%; opacity: 0; }}
                50% {{ top: 70%; left: 60%; opacity: 1; }}
                100% {{ top: 90%; left: 40%; opacity: 0; }}
            }}
            </style>
            """, unsafe_allow_html=True)
            
            # Interaction summary
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <p style="font-weight: bold; font-size: 1.1rem; color: {'#dc2626' if severity == 'High' else '#ea580c' if severity == 'Medium' else '#ca8a04' if severity == 'Low' else '#16a34a'};">
                    {warning_text}
                </p>
                <div style="color: #6b7280; margin-top: 0.5rem;">
                    <strong>🎯 Target: {effect_info['target']}</strong><br>
                    <small>💊 {interaction['drug_a']} + {interaction['drug_b']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Default state - no interaction checked yet
            st.markdown("""
            <div class="glb-container" style="border: 2px solid #e5e7eb; border-radius: 15px; padding: 1rem;">
                <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
                <model-viewer 
                    src="HumanBody.glb"
                    alt="Digital Twin"
                    camera-controls
                    auto-rotate
                    loading="eager"
                    reveal="auto"
                    style="width:100%; height:450px; background-color: #f8fafc; border-radius: 10px;"
                    exposure="1"
                    shadow-intensity="1"
                    environment-image="neutral">
                    <div slot="progress-bar" style="display: none;"></div>
                </model-viewer>
                <p style="margin-top: 1rem; color: #64748b; text-align: center; font-weight: 500;">
                    🧬 Select condition and medicines on the left to see interaction effects on the 3D body
                </p>
                <div style="text-align: center; margin-top: 0.5rem; color: #9ca3af;">
                    <small>💡 The 3D model will show visual effects based on drug interactions</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced interaction history
        if 'interaction_history' not in st.session_state:
            st.session_state.interaction_history = []
        
        # Enhanced history display
        if st.session_state.interaction_history:
            st.markdown('''
            <div style="margin-top: 2rem;">
                <h4 style="color: #1f2937; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                    <span>📋</span> Recent Analysis History
                </h4>
            </div>
            ''', unsafe_allow_html=True)
            
            for i, interaction in enumerate(reversed(st.session_state.interaction_history[-5:])):
                severity = interaction['result']['severity'] if 'result' in interaction else interaction.get('severity', 'None')
                severity_colors = {
                    'High': {'bg': '#fef2f2', 'border': '#dc2626', 'text': '#991b1b'},
                    'Severe': {'bg': '#fef2f2', 'border': '#dc2626', 'text': '#991b1b'},
                    'Medium': {'bg': '#fff7ed', 'border': '#ea580c', 'text': '#9a3412'},
                    'Moderate': {'bg': '#fff7ed', 'border': '#ea580c', 'text': '#9a3412'},
                    'Low': {'bg': '#fefce8', 'border': '#ca8a04', 'text': '#a16207'},
                    'Minor': {'bg': '#fefce8', 'border': '#ca8a04', 'text': '#a16207'},
                    'None': {'bg': '#f0fdf4', 'border': '#16a34a', 'text': '#166534'}
                }
                
                colors = severity_colors.get(severity, {'bg': '#f9fafb', 'border': '#64748b', 'text': '#374151'})
                
                ts = interaction['timestamp']
                if isinstance(ts, pd.Timestamp):
                    ts_str = ts.strftime('%H:%M:%S')
                else:
                    ts_str = str(ts)
                
                st.markdown(f'''
                <div class="history-card" style="background: {colors['bg']}; border-left-color: {colors['border']};">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                        <div style="font-weight: 600; color: #1f2937; font-size: 0.9rem;">
                            {interaction['drug_a']} + {interaction['drug_b']}
                        </div>
                        <div style="font-size: 0.75rem; color: #6b7280;">{ts_str}</div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="background: {colors['border']}; color: white; padding: 0.125rem 0.5rem; 
                                    border-radius: 12px; font-size: 0.75rem; font-weight: 500;">
                            {severity}
                        </span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Enhanced clear history button
        if st.session_state.interaction_history:
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            if st.button("🗑️ Clear Analysis History", help="Clear all previous interaction analyses"):
                st.session_state.interaction_history = []
                if 'current_interaction' in st.session_state:
                    del st.session_state.current_interaction
                st.rerun()
    
    # Add floating action button for quick access
    st.markdown('''
    <button class="floating-action" onclick="window.scrollTo({top: 0, behavior: 'smooth'});" title="Back to Top">
        ↑
    </button>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
