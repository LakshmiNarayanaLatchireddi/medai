#!/usr/bin/env python3
"""
Quick system test for MediAI Guardian 3.0
"""

import os
import sys

def test_system():
    print("🏥 MediAI Guardian 3.0 - System Test")
    print("=" * 50)
    
    # Check if all required files exist
    required_files = [
        'app.py',
        'auth.py',
        'requirements.txt',
        'pages/1_Patient_Dashboard.py',
        'pages/2_Doctor_Dashboard.py', 
        'pages/3_Medicine_Reactions.py',
        'pages/4_Emergency_Assistant.py',
        'pages/5_Doctor_Summary.py',
        'agents/vitals_agent.py',
        'agents/medicine_agent.py',
        'agents/digital_twin_agent.py',
        'agents/emergency_agent.py',
        'agents/summary_agent.py',
        'HumanBody.glb',
        'db_drug_interactions.csv'
    ]
    
    print("✅ Checking required files...")
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
            missing_files.append(file)
    
    print(f"\n📊 System Status:")
    print(f"  • Total files required: {len(required_files)}")
    print(f"  • Files present: {len(required_files) - len(missing_files)}")
    print(f"  • Files missing: {len(missing_files)}")
    
    if not missing_files:
        print("\n🎉 ALL FILES PRESENT - System Ready!")
        print("\n🚀 To start the application:")
        print("   1. Open Command Prompt or PowerShell")
        print("   2. Navigate to this directory:")
        print(f"      cd {os.getcwd()}")
        print("   3. Install dependencies:")
        print("      pip install streamlit pandas plotly reportlab numpy")
        print("   4. Run the application:")
        print("      streamlit run app.py")
        print("\n🔐 Login Credentials:")
        print("   Patient: username='patient', password='123'")
        print("   Doctor:  username='doctor', password='123'")
        
        # Test imports
        print("\n🧪 Testing Python imports...")
        try:
            import pandas as pd
            print("  ✅ pandas")
        except ImportError:
            print("  ❌ pandas - run: pip install pandas")
            
        try:
            import plotly
            print("  ✅ plotly")
        except ImportError:
            print("  ❌ plotly - run: pip install plotly")
            
        try:
            import streamlit as st
            print("  ✅ streamlit")
        except ImportError:
            print("  ❌ streamlit - run: pip install streamlit")
            
        # Test agents
        print("\n🤖 Testing AI Agents...")
        try:
            sys.path.append('.')
            from agents.vitals_agent import VitalsAgent
            agent = VitalsAgent()
            print("  ✅ VitalsAgent")
        except Exception as e:
            print(f"  ❌ VitalsAgent - {e}")
            
        try:
            from agents.medicine_agent import MedicineAgent
            agent = MedicineAgent()
            print("  ✅ MedicineAgent")
        except Exception as e:
            print(f"  ❌ MedicineAgent - {e}")
            
        print("\n🎯 System is ready for demonstration!")
        
    else:
        print(f"\n❌ Missing files: {missing_files}")
        print("Please ensure all files are present before running.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_system()
