#!/usr/bin/env python3
"""
Startup script for MediAI Guardian 3.0
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    requirements = [
        'streamlit>=1.28.0',
        'pandas>=2.0.0', 
        'plotly>=5.15.0',
        'reportlab>=4.0.0',
        'numpy>=1.24.0'
    ]
    
    print("Installing required packages...")
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', req])
        except subprocess.CalledProcessError:
            print(f"Warning: Could not install {req}")

def start_streamlit():
    """Start the Streamlit application"""
    print("\n" + "="*50)
    print("🏥 MediAI Guardian 3.0 - Starting...")
    print("="*50)
    
    try:
        # Change to the script directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Start Streamlit
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'])
    except KeyboardInterrupt:
        print("\n\nShutting down MediAI Guardian 3.0...")
    except Exception as e:
        print(f"Error starting application: {e}")
        print("\nTry running manually with: streamlit run app.py")

if __name__ == "__main__":
    print("🏥 MediAI Guardian 3.0 - Agentic Medical Twin System")
    print("="*60)
    
    # Install requirements
    install_requirements()
    
    # Start the application
    start_streamlit()
