# MediAI Guardian 3.0 - Agentic Medical Twin System

A comprehensive AI-powered healthcare monitoring system with 3D digital twin technology, built with Python, Streamlit, and OpenAI Agents.

## 🚀 Features

- **Role-based Authentication**: Patient and Doctor login portals
- **3D Digital Twin**: Interactive GLB model showing medicine reactions
- **AI Agents**: 5 specialized agents for different medical tasks
- **Drug Interaction Analysis**: Real-time analysis using comprehensive dataset
- **Emergency Response**: AI-powered first-aid guidance
- **Vitals Monitoring**: Real-time health metrics tracking
- **Report Generation**: Downloadable PDF summaries

## 📁 Project Structure

```
medai/
├── app.py                          # Main Streamlit application
├── auth.py                         # Authentication logic
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── pages/                          # Streamlit pages
│   ├── 1_Patient_Dashboard.py      # Patient portal
│   ├── 2_Doctor_Dashboard.py       # Doctor portal
│   ├── 3_Medicine_Reactions.py     # Drug interaction checker
│   ├── 4_Emergency_Assistant.py    # Emergency response system
│   └── 5_Doctor_Summary.py         # Report generation
├── agents/                         # AI Agents
│   ├── vitals_agent.py            # Vital signs analysis
│   ├── medicine_agent.py          # Drug interaction analysis
│   ├── digital_twin_agent.py      # Digital twin state management
│   ├── emergency_agent.py         # Emergency response protocols
│   └── summary_agent.py           # Report generation
├── data/                          # Data files
│   └── drug_interactions.csv      # Drug interaction dataset
├── assets/                        # Static assets
│   └── human_body.glb            # 3D human model
├── HumanBody.glb                  # Main 3D model file
└── db_drug_interactions.csv       # Full drug interaction database
```

## 🛠️ Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Files**:
   - Ensure `HumanBody.glb` is in the root directory
   - Ensure `db_drug_interactions.csv` is in the root directory

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## 🔐 Login Credentials

### Patient Portal
- **Username**: `patient`
- **Password**: `123`

### Doctor Portal
- **Username**: `doctor`
- **Password**: `123`

## 🎯 Key Features by Role

### Patient Dashboard
- Real-time vital signs monitoring
- 3D digital twin visualization
- Medicine intake simulation
- Drug interaction warnings
- Emergency assistance access

### Doctor Dashboard
- Multi-patient monitoring
- Comprehensive analytics
- Emergency event tracking
- Risk assessment overview
- Patient management tools

### Medicine Reactions
- Drug-drug interaction checker
- 3D visualization of affected body systems
- Severity-based color coding
- Real-time database lookup
- Safety recommendations

### Emergency Assistant
- AI-powered first-aid guidance
- Step-by-step emergency protocols
- 3D twin emergency visualization
- Emergency contact information
- Real-time status monitoring

### Doctor Summary
- AI-generated patient reports
- Comprehensive health analytics
- Downloadable PDF reports
- Risk trend analysis
- Treatment recommendations

## 🤖 AI Agents

### 1. VitalsAgent
- Analyzes vital signs in real-time
- Provides health status assessment
- Generates personalized recommendations
- Tracks health trends

### 2. MedicineAgent
- Processes drug interaction database
- Identifies potential conflicts
- Assesses interaction severity
- Provides safety guidelines

### 3. DigitalTwinAgent
- Maintains digital twin state
- Updates risk levels dynamically
- Tracks health score changes
- Manages visual representations

### 4. EmergencyAgent
- Provides emergency protocols
- Offers step-by-step guidance
- Assesses emergency severity
- Delivers first-aid instructions

### 5. SummaryAgent
- Generates comprehensive reports
- Analyzes patient data trends
- Creates actionable insights
- Produces downloadable summaries

## 🎨 3D Digital Twin Features

- **Interactive GLB Model**: Rotate, zoom, and explore
- **Real-time Reactions**: Visual feedback for medicine effects
- **Color-coded States**: 
  - 🟢 Green: Healthy/Safe
  - 🟡 Yellow: Mild Risk/Minor Interaction
  - 🟠 Orange: Moderate Risk/Medium Interaction
  - 🔴 Red: High Risk/Severe Interaction/Emergency
- **Dynamic Animations**: Pulsing effects for active states

## 📊 Data Sources

- **Drug Interactions**: 191,543+ interaction records
- **Vital Signs**: Real-time simulated data
- **Emergency Protocols**: Comprehensive first-aid database
- **Patient Records**: Structured health data

## 🔧 Technical Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: Python with pandas for data processing
- **3D Visualization**: Model-viewer web component
- **Charts**: Plotly for interactive visualizations
- **Reports**: ReportLab for PDF generation
- **Data**: CSV-based drug interaction database

## 🚨 Emergency Features

- **6 Emergency Types**: Fainting, Chest Pain, Dizziness, Breathing Issues, Headache, Allergic Reactions
- **AI Guidance**: Step-by-step first-aid instructions
- **Visual Alerts**: 3D twin emergency state visualization
- **Safety Protocols**: When to call 911 guidelines
- **Real-time Monitoring**: Emergency status tracking

## 📈 Monitoring & Analytics

- **Real-time Vitals**: Heart rate, blood pressure, temperature, oxygen saturation
- **Risk Assessment**: Dynamic health scoring system
- **Trend Analysis**: Historical data visualization
- **Predictive Insights**: AI-powered health predictions

## 🔒 Security & Privacy

- Role-based access control
- Session state management
- Secure authentication system
- Data privacy protection

## 🎯 Demo Scenarios

1. **Patient Login**: Monitor vitals and simulate medicine intake
2. **Drug Interaction**: Check Aspirin + Warfarin interaction
3. **Emergency Simulation**: Trigger chest pain emergency
4. **Doctor Review**: Generate comprehensive patient report
5. **3D Visualization**: Observe digital twin state changes

## 📞 Support & Contact

For technical support or questions about the MediAI Guardian 3.0 system, please refer to the documentation or contact the development team.

---

**⚠️ Disclaimer**: This is a demonstration system for educational purposes. Always consult healthcare professionals for medical decisions.
