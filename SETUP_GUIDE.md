# 🚀 MediAI Guardian 3.0 - Setup Guide

## 📋 Quick Start Instructions

### Step 1: Open Command Prompt or PowerShell
- Press `Win + R`, type `cmd`, press Enter
- Or press `Win + X`, select "Windows PowerShell"

### Step 2: Navigate to Project Directory
```bash
cd "C:\Users\saipr\Downloads\medai"
```

### Step 3: Install Dependencies
```bash
pip install streamlit pandas plotly reportlab numpy
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

### Step 5: Open in Browser
- Streamlit will automatically open your browser
- If not, go to: `http://localhost:8501`

## 🔐 Login Credentials

### Patient Portal
- **Username**: `patient`
- **Password**: `123`

### Doctor Portal  
- **Username**: `doctor`
- **password**: `123`

## 🎯 Demo Flow

1. **Login Page** → Select Patient or Doctor role
2. **Patient Dashboard** → Monitor vitals, simulate medicine intake
3. **Medicine Reactions** → Check drug interactions (try "Aspirin" + "Warfarin")
4. **Emergency Assistant** → Simulate emergency (try "Chest Pain")
5. **Doctor Summary** → Generate AI reports

## 🧪 Test the System

Run the system test first:
```bash
python test_system.py
```

## 🎨 Key Features to Demonstrate

### 3D Digital Twin
- Interactive GLB model viewer
- Real-time color changes based on medicine reactions
- Emergency state visualization

### Drug Interactions
- Real data from 191K+ interaction database
- Severity-based visual feedback on 3D model
- No AI hallucinations - only real CSV data

### Emergency Response
- 6 emergency types with AI guidance
- Step-by-step first-aid instructions
- 3D twin emergency visualization

### AI Agents
- 5 specialized medical AI agents
- Real-time analysis and recommendations
- Comprehensive patient summaries

## 🔧 Troubleshooting

### If Streamlit doesn't start:
```bash
python -m streamlit run app.py
```

### If dependencies are missing:
```bash
pip install --upgrade streamlit pandas plotly reportlab numpy
```

### If GLB model doesn't load:
- Ensure `HumanBody.glb` is in the root directory
- Check browser console for errors

### If drug interactions don't work:
- Ensure `db_drug_interactions.csv` is in the root directory
- Check file permissions

## 📊 System Requirements

- Python 3.7+
- Modern web browser (Chrome, Firefox, Edge)
- Internet connection (for model-viewer component)
- ~500MB free space

## 🎉 You're Ready!

Your MediAI Guardian 3.0 system is complete and ready for the hackathon demonstration!

---

**Need help? Check the README.md or PROJECT_OVERVIEW.md files for more details.**
