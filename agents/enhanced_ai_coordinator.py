"""
Enhanced AI Coordinator for MediAI Guardian 3.0
Manages all agentic AI interactions and decision-making
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random

class AgenticAICoordinator:
    def __init__(self):
        self.agents = {
            "ddi_agent": DDIAgent(),
            "digital_twin_agent": DigitalTwinAgent(),
            "safety_agent": SafetyAgent(),
            "first_aid_agent": FirstAidAgent(),
            "doctor_support_agent": DoctorSupportAgent(),
            "mediai_chat_agent": MediAIChatAgent()
        }
        self.decision_log = []
        self.collaboration_history = []
        
    def coordinate_decision(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate decision-making across all agents"""
        decision_id = f"decision_{int(time.time())}"
        
        # Gather input from all relevant agents
        agent_inputs = {}
        for agent_name, agent in self.agents.items():
            try:
                agent_input = agent.analyze(context)
                agent_inputs[agent_name] = agent_input
            except Exception as e:
                agent_inputs[agent_name] = {"error": str(e), "status": "failed"}
        
        # Synthesize final decision
        final_decision = self._synthesize_decision(agent_inputs, context)
        
        # Log the decision process
        decision_record = {
            "id": decision_id,
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "agent_inputs": agent_inputs,
            "final_decision": final_decision,
            "collaboration_score": self._calculate_collaboration_score(agent_inputs)
        }
        
        self.decision_log.append(decision_record)
        return final_decision
    
    def _synthesize_decision(self, agent_inputs: Dict, context: Dict) -> Dict:
        """Synthesize inputs from all agents into final decision"""
        risk_scores = []
        recommendations = []
        warnings = []
        
        for agent_name, input_data in agent_inputs.items():
            if "error" not in input_data:
                risk_scores.append(input_data.get("risk_score", 0))
                recommendations.extend(input_data.get("recommendations", []))
                warnings.extend(input_data.get("warnings", []))
        
        # Calculate overall risk
        overall_risk = max(risk_scores) if risk_scores else 0
        
        # Determine risk level
        if overall_risk >= 8:
            risk_level = "CRITICAL"
            action_urgency = "IMMEDIATE"
        elif overall_risk >= 6:
            risk_level = "HIGH"
            action_urgency = "URGENT"
        elif overall_risk >= 4:
            risk_level = "MODERATE"
            action_urgency = "MONITOR"
        else:
            risk_level = "LOW"
            action_urgency = "ROUTINE"
        
        return {
            "overall_risk_score": overall_risk,
            "risk_level": risk_level,
            "action_urgency": action_urgency,
            "recommendations": recommendations[:5],  # Top 5 recommendations
            "warnings": warnings,
            "explanation": self._generate_explanation(agent_inputs, overall_risk),
            "next_steps": self._generate_next_steps(risk_level, recommendations)
        }
    
    def _generate_explanation(self, agent_inputs: Dict, risk_score: float) -> str:
        """Generate human-readable explanation of the decision"""
        explanations = []
        
        for agent_name, input_data in agent_inputs.items():
            if "error" not in input_data and input_data.get("explanation"):
                explanations.append(f"{agent_name}: {input_data['explanation']}")
        
        base_explanation = f"Overall risk assessment: {risk_score}/10. "
        agent_explanations = " | ".join(explanations)
        
        return base_explanation + agent_explanations
    
    def _generate_next_steps(self, risk_level: str, recommendations: List[str]) -> List[str]:
        """Generate actionable next steps based on risk level"""
        if risk_level == "CRITICAL":
            return [
                "🚨 Seek immediate medical attention",
                "📞 Contact emergency services if needed",
                "💊 Stop current medication if advised",
                "📋 Prepare medical history for healthcare providers"
            ]
        elif risk_level == "HIGH":
            return [
                "⚠️ Contact your doctor within 24 hours",
                "📊 Monitor vital signs closely",
                "💊 Review medication timing and dosage",
                "📝 Document any new symptoms"
            ]
        elif risk_level == "MODERATE":
            return [
                "📅 Schedule follow-up appointment",
                "📈 Continue monitoring trends",
                "💊 Maintain current medication schedule",
                "🏃‍♂️ Consider lifestyle modifications"
            ]
        else:
            return [
                "✅ Continue current treatment plan",
                "📊 Regular monitoring as scheduled",
                "💊 Take medications as prescribed",
                "🌟 Maintain healthy lifestyle"
            ]
    
    def _calculate_collaboration_score(self, agent_inputs: Dict) -> float:
        """Calculate how well agents collaborated"""
        successful_agents = sum(1 for input_data in agent_inputs.values() if "error" not in input_data)
        total_agents = len(agent_inputs)
        
        return (successful_agents / total_agents) * 100 if total_agents > 0 else 0
    
    def get_recent_decisions(self, limit: int = 10) -> List[Dict]:
        """Get recent decision records"""
        return self.decision_log[-limit:] if self.decision_log else []
    
    def get_agent_performance(self) -> Dict[str, Any]:
        """Get performance metrics for each agent"""
        performance = {}
        
        for agent_name in self.agents.keys():
            successful_calls = sum(1 for record in self.decision_log 
                                 if "error" not in record["agent_inputs"].get(agent_name, {}))
            total_calls = len(self.decision_log)
            
            performance[agent_name] = {
                "success_rate": (successful_calls / total_calls * 100) if total_calls > 0 else 0,
                "total_calls": total_calls,
                "successful_calls": successful_calls
            }
        
        return performance

class DDIAgent:
    """Drug-Drug Interaction Agent"""
    
    def analyze(self, context: Dict) -> Dict:
        """Analyze drug interactions"""
        medications = context.get("medications", [])
        
        if len(medications) < 2:
            return {
                "risk_score": 1,
                "recommendations": ["Continue single medication as prescribed"],
                "warnings": [],
                "explanation": "Single medication - no interaction risk"
            }
        
        # Simulate interaction analysis
        interaction_risk = self._calculate_interaction_risk(medications)
        
        return {
            "risk_score": interaction_risk,
            "recommendations": self._get_interaction_recommendations(interaction_risk),
            "warnings": self._get_interaction_warnings(medications, interaction_risk),
            "explanation": f"Analyzed {len(medications)} medications for interactions"
        }
    
    def _calculate_interaction_risk(self, medications: List[str]) -> int:
        """Calculate interaction risk score"""
        high_risk_combinations = [
            ("warfarin", "aspirin"),
            ("lisinopril", "potassium"),
            ("metformin", "alcohol")
        ]
        
        risk_score = 2  # Base risk
        
        for med1 in medications:
            for med2 in medications:
                if med1 != med2:
                    for combo in high_risk_combinations:
                        if (med1.lower() in combo[0] and med2.lower() in combo[1]) or \
                           (med1.lower() in combo[1] and med2.lower() in combo[0]):
                            risk_score += 4
        
        return min(risk_score, 10)
    
    def _get_interaction_recommendations(self, risk_score: int) -> List[str]:
        """Get recommendations based on interaction risk"""
        if risk_score >= 7:
            return [
                "Consult pharmacist immediately",
                "Consider alternative medications",
                "Monitor for adverse effects closely"
            ]
        elif risk_score >= 4:
            return [
                "Space medication timing",
                "Monitor for side effects",
                "Regular follow-up recommended"
            ]
        else:
            return [
                "Continue as prescribed",
                "Standard monitoring sufficient"
            ]
    
    def _get_interaction_warnings(self, medications: List[str], risk_score: int) -> List[str]:
        """Get specific warnings for medication combinations"""
        warnings = []
        
        if risk_score >= 6:
            warnings.append("⚠️ High interaction risk detected")
        
        if "warfarin" in [med.lower() for med in medications]:
            warnings.append("🩸 Monitor bleeding risk with blood thinners")
        
        return warnings

class DigitalTwinAgent:
    """Digital Twin Agent for physiological modeling"""
    
    def analyze(self, context: Dict) -> Dict:
        """Analyze physiological state and predict outcomes"""
        vitals = context.get("vitals", {})
        medications = context.get("medications", [])
        medical_history = context.get("medical_history", [])
        
        # Simulate digital twin analysis
        physiological_risk = self._assess_physiological_state(vitals)
        medication_impact = self._predict_medication_impact(medications, vitals)
        
        overall_risk = max(physiological_risk, medication_impact)
        
        return {
            "risk_score": overall_risk,
            "recommendations": self._get_physiological_recommendations(overall_risk),
            "warnings": self._get_physiological_warnings(vitals),
            "explanation": f"Digital twin model shows {self._get_risk_description(overall_risk)} physiological state",
            "predicted_outcomes": self._predict_outcomes(vitals, medications)
        }
    
    def _assess_physiological_state(self, vitals: Dict) -> int:
        """Assess current physiological state"""
        risk_factors = 0
        
        # Blood pressure assessment
        bp_sys = vitals.get("blood_pressure_systolic", 120)
        if bp_sys > 140 or bp_sys < 90:
            risk_factors += 2
        
        # Heart rate assessment
        hr = vitals.get("heart_rate", 70)
        if hr > 100 or hr < 60:
            risk_factors += 1
        
        # Temperature assessment
        temp = vitals.get("temperature", 98.6)
        if temp > 100.4 or temp < 96:
            risk_factors += 2
        
        # Oxygen saturation
        o2_sat = vitals.get("oxygen_saturation", 98)
        if o2_sat < 95:
            risk_factors += 3
        
        return min(risk_factors, 10)
    
    def _predict_medication_impact(self, medications: List[str], vitals: Dict) -> int:
        """Predict how medications will impact physiology"""
        impact_score = 1
        
        # Simulate medication impact prediction
        for med in medications:
            if "blood pressure" in med.lower() or "lisinopril" in med.lower():
                bp = vitals.get("blood_pressure_systolic", 120)
                if bp > 140:
                    impact_score += 1  # Positive impact
                else:
                    impact_score += 2  # May cause hypotension
        
        return min(impact_score, 10)
    
    def _get_physiological_recommendations(self, risk_score: int) -> List[str]:
        """Get recommendations based on physiological assessment"""
        if risk_score >= 7:
            return [
                "Immediate medical evaluation needed",
                "Continuous vital sign monitoring",
                "Consider hospitalization"
            ]
        elif risk_score >= 4:
            return [
                "Increase monitoring frequency",
                "Adjust medication timing",
                "Lifestyle modifications recommended"
            ]
        else:
            return [
                "Continue current regimen",
                "Regular monitoring sufficient",
                "Maintain healthy lifestyle"
            ]
    
    def _get_physiological_warnings(self, vitals: Dict) -> List[str]:
        """Get warnings based on vital signs"""
        warnings = []
        
        if vitals.get("blood_pressure_systolic", 120) > 160:
            warnings.append("🩸 Severe hypertension detected")
        
        if vitals.get("heart_rate", 70) > 120:
            warnings.append("❤️ Tachycardia detected")
        
        if vitals.get("oxygen_saturation", 98) < 90:
            warnings.append("🫁 Severe hypoxemia detected")
        
        return warnings
    
    def _get_risk_description(self, risk_score: int) -> str:
        """Get human-readable risk description"""
        if risk_score >= 8:
            return "critical"
        elif risk_score >= 6:
            return "high-risk"
        elif risk_score >= 4:
            return "moderate-risk"
        else:
            return "stable"
    
    def _predict_outcomes(self, vitals: Dict, medications: List[str]) -> Dict:
        """Predict likely outcomes based on current state"""
        return {
            "24_hour_outlook": "Stable with current treatment",
            "medication_effectiveness": "85% expected effectiveness",
            "risk_trajectory": "Improving with treatment compliance"
        }

class SafetyAgent:
    """Safety monitoring and alert agent"""
    
    def analyze(self, context: Dict) -> Dict:
        """Analyze safety concerns and generate alerts"""
        vitals = context.get("vitals", {})
        medications = context.get("medications", [])
        symptoms = context.get("symptoms", [])
        
        safety_risk = self._assess_safety_risk(vitals, medications, symptoms)
        
        return {
            "risk_score": safety_risk,
            "recommendations": self._get_safety_recommendations(safety_risk),
            "warnings": self._get_safety_warnings(vitals, symptoms),
            "explanation": f"Safety assessment indicates {self._get_safety_level(safety_risk)} risk level",
            "immediate_actions": self._get_immediate_actions(safety_risk)
        }
    
    def _assess_safety_risk(self, vitals: Dict, medications: List[str], symptoms: List[str]) -> int:
        """Assess overall safety risk"""
        risk_score = 1
        
        # Critical vital signs
        if vitals.get("blood_pressure_systolic", 120) > 180:
            risk_score += 4
        if vitals.get("heart_rate", 70) > 150 or vitals.get("heart_rate", 70) < 40:
            risk_score += 4
        if vitals.get("oxygen_saturation", 98) < 85:
            risk_score += 5
        
        # Dangerous symptoms
        dangerous_symptoms = ["chest pain", "difficulty breathing", "severe headache", "confusion"]
        for symptom in symptoms:
            if any(danger in symptom.lower() for danger in dangerous_symptoms):
                risk_score += 3
        
        return min(risk_score, 10)
    
    def _get_safety_recommendations(self, risk_score: int) -> List[str]:
        """Get safety-focused recommendations"""
        if risk_score >= 8:
            return [
                "Call emergency services immediately",
                "Do not drive or operate machinery",
                "Have someone stay with patient"
            ]
        elif risk_score >= 5:
            return [
                "Seek immediate medical attention",
                "Monitor continuously",
                "Prepare for potential emergency"
            ]
        else:
            return [
                "Continue monitoring",
                "Follow standard safety precautions",
                "Report any changes immediately"
            ]
    
    def _get_safety_warnings(self, vitals: Dict, symptoms: List[str]) -> List[str]:
        """Get specific safety warnings"""
        warnings = []
        
        if vitals.get("blood_pressure_systolic", 120) > 200:
            warnings.append("🚨 HYPERTENSIVE CRISIS - Emergency care needed")
        
        if "chest pain" in [s.lower() for s in symptoms]:
            warnings.append("💔 CHEST PAIN - Possible cardiac event")
        
        if vitals.get("oxygen_saturation", 98) < 88:
            warnings.append("🫁 CRITICAL HYPOXEMIA - Oxygen therapy needed")
        
        return warnings
    
    def _get_safety_level(self, risk_score: int) -> str:
        """Get safety level description"""
        if risk_score >= 8:
            return "CRITICAL"
        elif risk_score >= 5:
            return "HIGH"
        elif risk_score >= 3:
            return "MODERATE"
        else:
            return "LOW"
    
    def _get_immediate_actions(self, risk_score: int) -> List[str]:
        """Get immediate actions to take"""
        if risk_score >= 8:
            return [
                "Call 911 immediately",
                "Position patient safely",
                "Prepare medical information"
            ]
        elif risk_score >= 5:
            return [
                "Contact healthcare provider",
                "Increase monitoring frequency",
                "Prepare for medical visit"
            ]
        else:
            return [
                "Continue current monitoring",
                "Document any changes",
                "Follow routine care plan"
            ]

class FirstAidAgent:
    """First aid and emergency response agent"""
    
    def analyze(self, context: Dict) -> Dict:
        """Analyze emergency situation and provide first aid guidance"""
        symptoms = context.get("symptoms", [])
        vitals = context.get("vitals", {})
        emergency_type = self._classify_emergency(symptoms, vitals)
        
        return {
            "risk_score": self._get_emergency_risk_score(emergency_type),
            "recommendations": self._get_first_aid_steps(emergency_type),
            "warnings": self._get_emergency_warnings(emergency_type),
            "explanation": f"Emergency classification: {emergency_type}",
            "emergency_contacts": self._get_emergency_contacts(),
            "first_aid_steps": self._get_detailed_first_aid(emergency_type)
        }
    
    def _classify_emergency(self, symptoms: List[str], vitals: Dict) -> str:
        """Classify type of emergency"""
        symptom_text = " ".join(symptoms).lower()
        
        if "chest pain" in symptom_text or "heart attack" in symptom_text:
            return "CARDIAC_EMERGENCY"
        elif "difficulty breathing" in symptom_text or vitals.get("oxygen_saturation", 98) < 85:
            return "RESPIRATORY_EMERGENCY"
        elif "stroke" in symptom_text or "confusion" in symptom_text:
            return "NEUROLOGICAL_EMERGENCY"
        elif vitals.get("blood_pressure_systolic", 120) > 200:
            return "HYPERTENSIVE_CRISIS"
        elif "severe bleeding" in symptom_text:
            return "HEMORRHAGE"
        else:
            return "GENERAL_EMERGENCY"
    
    def _get_emergency_risk_score(self, emergency_type: str) -> int:
        """Get risk score based on emergency type"""
        risk_scores = {
            "CARDIAC_EMERGENCY": 10,
            "RESPIRATORY_EMERGENCY": 9,
            "NEUROLOGICAL_EMERGENCY": 9,
            "HYPERTENSIVE_CRISIS": 8,
            "HEMORRHAGE": 8,
            "GENERAL_EMERGENCY": 5
        }
        return risk_scores.get(emergency_type, 5)
    
    def _get_first_aid_steps(self, emergency_type: str) -> List[str]:
        """Get first aid recommendations"""
        steps = {
            "CARDIAC_EMERGENCY": [
                "Call 911 immediately",
                "Give aspirin if not allergic",
                "Position patient comfortably",
                "Monitor breathing and pulse"
            ],
            "RESPIRATORY_EMERGENCY": [
                "Call 911 immediately",
                "Help patient sit upright",
                "Loosen tight clothing",
                "Use rescue inhaler if available"
            ],
            "HYPERTENSIVE_CRISIS": [
                "Call 911 immediately",
                "Keep patient calm and seated",
                "Do not give medications",
                "Monitor vital signs"
            ]
        }
        return steps.get(emergency_type, ["Call 911", "Keep patient safe", "Monitor vital signs"])
    
    def _get_emergency_warnings(self, emergency_type: str) -> List[str]:
        """Get emergency-specific warnings"""
        warnings = {
            "CARDIAC_EMERGENCY": ["🚨 HEART ATTACK SUSPECTED - Time is critical"],
            "RESPIRATORY_EMERGENCY": ["🫁 BREATHING DIFFICULTY - Oxygen needed"],
            "HYPERTENSIVE_CRISIS": ["🩸 BLOOD PRESSURE CRISIS - Stroke risk"]
        }
        return warnings.get(emergency_type, ["⚠️ Emergency situation detected"])
    
    def _get_emergency_contacts(self) -> Dict[str, str]:
        """Get emergency contact information"""
        return {
            "Emergency Services": "911",
            "Poison Control": "1-800-222-1222",
            "Crisis Hotline": "988",
            "Local Hospital": "Call directory assistance"
        }
    
    def _get_detailed_first_aid(self, emergency_type: str) -> List[Dict[str, str]]:
        """Get detailed first aid instructions"""
        if emergency_type == "CARDIAC_EMERGENCY":
            return [
                {"step": 1, "action": "Call 911", "details": "Tell them you suspect a heart attack"},
                {"step": 2, "action": "Give aspirin", "details": "325mg if not allergic, have them chew it"},
                {"step": 3, "action": "Position patient", "details": "Sitting up or lying down, whatever is comfortable"},
                {"step": 4, "action": "Monitor", "details": "Watch breathing, be ready for CPR"}
            ]
        else:
            return [
                {"step": 1, "action": "Assess situation", "details": "Check responsiveness and breathing"},
                {"step": 2, "action": "Call for help", "details": "911 for emergencies"},
                {"step": 3, "action": "Provide comfort", "details": "Keep patient calm and safe"}
            ]

class DoctorSupportAgent:
    """Doctor support and clinical decision support agent"""
    
    def analyze(self, context: Dict) -> Dict:
        """Provide clinical decision support"""
        vitals = context.get("vitals", {})
        medications = context.get("medications", [])
        medical_history = context.get("medical_history", [])
        
        clinical_assessment = self._perform_clinical_assessment(vitals, medications, medical_history)
        
        return {
            "risk_score": clinical_assessment["risk_score"],
            "recommendations": clinical_assessment["recommendations"],
            "warnings": clinical_assessment["warnings"],
            "explanation": clinical_assessment["explanation"],
            "clinical_notes": clinical_assessment["clinical_notes"],
            "suggested_tests": clinical_assessment["suggested_tests"]
        }
    
    def _perform_clinical_assessment(self, vitals: Dict, medications: List[str], history: List[str]) -> Dict:
        """Perform comprehensive clinical assessment"""
        risk_score = 2  # Base risk
        recommendations = []
        warnings = []
        clinical_notes = []
        suggested_tests = []
        
        # Assess vital signs
        bp_sys = vitals.get("blood_pressure_systolic", 120)
        if bp_sys > 140:
            risk_score += 2
            recommendations.append("Consider antihypertensive therapy adjustment")
            clinical_notes.append(f"Hypertension noted: {bp_sys} mmHg")
            
        hr = vitals.get("heart_rate", 70)
        if hr > 100:
            risk_score += 1
            recommendations.append("Investigate cause of tachycardia")
            suggested_tests.append("ECG")
        
        # Assess medication regimen
        if len(medications) > 5:
            risk_score += 1
            recommendations.append("Review polypharmacy - consider deprescribing")
            clinical_notes.append("Polypharmacy noted - medication review indicated")
        
        # Risk stratification
        explanation = f"Clinical assessment shows {self._get_clinical_risk_level(risk_score)} risk patient"
        
        return {
            "risk_score": min(risk_score, 10),
            "recommendations": recommendations,
            "warnings": warnings,
            "explanation": explanation,
            "clinical_notes": clinical_notes,
            "suggested_tests": suggested_tests
        }
    
    def _get_clinical_risk_level(self, risk_score: int) -> str:
        """Get clinical risk level"""
        if risk_score >= 7:
            return "high"
        elif risk_score >= 4:
            return "moderate"
        else:
            return "low"

class MediAIChatAgent:
    """Conversational AI agent for health questions"""
    
    def analyze(self, context: Dict) -> Dict:
        """Analyze user query and provide intelligent response"""
        query = context.get("query", "")
        user_data = context.get("user_data", {})
        
        response = self._generate_response(query, user_data)
        
        return {
            "risk_score": response["risk_score"],
            "recommendations": response["recommendations"],
            "warnings": response.get("warnings", []),
            "explanation": response["response"],
            "follow_up_questions": response.get("follow_up_questions", [])
        }
    
    def _generate_response(self, query: str, user_data: Dict) -> Dict:
        """Generate intelligent response to user query"""
        query_lower = query.lower()
        
        # Symptom-related queries
        if any(word in query_lower for word in ["pain", "hurt", "ache", "symptom"]):
            return {
                "response": "I understand you're experiencing symptoms. Based on your current health data, I recommend monitoring closely and consulting your healthcare provider if symptoms persist or worsen.",
                "risk_score": 4,
                "recommendations": ["Monitor symptoms", "Document onset and severity", "Contact healthcare provider if worsening"],
                "follow_up_questions": ["When did the symptoms start?", "How severe are they on a scale of 1-10?"]
            }
        
        # Medication-related queries
        elif any(word in query_lower for word in ["medication", "medicine", "drug", "pill"]):
            return {
                "response": "For medication questions, I can help you understand interactions and timing. Always consult your pharmacist or doctor before making changes to your medication regimen.",
                "risk_score": 2,
                "recommendations": ["Follow prescribed dosing", "Check for interactions", "Consult pharmacist for questions"],
                "follow_up_questions": ["Are you taking your medications as prescribed?", "Have you noticed any side effects?"]
            }
        
        # General health queries
        else:
            return {
                "response": "I'm here to help with your health questions. Based on your current health status, continue following your treatment plan and maintain regular monitoring.",
                "risk_score": 1,
                "recommendations": ["Continue current care plan", "Regular monitoring", "Healthy lifestyle maintenance"],
                "follow_up_questions": ["How are you feeling today?", "Any concerns about your current treatment?"]
            }
