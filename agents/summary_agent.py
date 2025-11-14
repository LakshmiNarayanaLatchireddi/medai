"""
Summary Agent - Generates comprehensive patient summaries and reports
"""

from datetime import datetime, timedelta
import json

class SummaryAgent:
    def __init__(self):
        self.name = "SummaryAgent"
        self.version = "1.0"
    
    def run(self, patient_data):
        """
        Generate comprehensive patient summary
        
        Args:
            patient_data (dict): Complete patient data including vitals, medications, etc.
        
        Returns:
            dict: Generated summary with analysis and recommendations
        """
        try:
            summary = self._generate_comprehensive_summary(patient_data)
            return summary
        except Exception as e:
            return {
                'error': f'Summary generation failed: {str(e)}',
                'summary': 'Unable to generate patient summary at this time',
                'recommendations': ['Consult healthcare provider for manual review']
            }
    
    def _generate_comprehensive_summary(self, patient_data):
        """Generate detailed patient summary"""
        
        # Extract patient information
        patient_info = patient_data.get('patient_info', {})
        vitals_history = patient_data.get('vitals_history', [])
        medications = patient_data.get('medications', [])
        drug_interactions = patient_data.get('drug_interactions', [])
        emergency_events = patient_data.get('emergency_events', [])
        digital_twin_risk = patient_data.get('digital_twin_risk', {})
        
        # Generate summary sections
        summary_text = self._create_summary_text(
            patient_info, vitals_history, medications, 
            drug_interactions, emergency_events, digital_twin_risk
        )
        
        recommendations = self._generate_recommendations(
            vitals_history, medications, drug_interactions, 
            emergency_events, digital_twin_risk
        )
        
        risk_assessment = self._assess_overall_risk(
            vitals_history, medications, drug_interactions, 
            emergency_events, digital_twin_risk
        )
        
        return {
            'summary': summary_text,
            'recommendations': recommendations,
            'risk_assessment': risk_assessment,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'key_metrics': self._extract_key_metrics(vitals_history),
            'medication_analysis': self._analyze_medications(medications, drug_interactions),
            'emergency_summary': self._summarize_emergencies(emergency_events)
        }
    
    def _create_summary_text(self, patient_info, vitals_history, medications, 
                           drug_interactions, emergency_events, digital_twin_risk):
        """Create comprehensive summary text"""
        
        name = patient_info.get('name', 'Patient')
        age = patient_info.get('age', 'Unknown')
        condition = patient_info.get('primary_condition', 'Not specified')
        
        # Vitals analysis
        if vitals_history:
            latest_vitals = vitals_history[0]
            vitals_trend = self._analyze_vitals_trend(vitals_history)
        else:
            latest_vitals = {}
            vitals_trend = "No vital signs data available"
        
        # Medication summary
        med_count = len(medications)
        interaction_count = len([i for i in drug_interactions if i.get('severity') != 'None'])
        
        # Emergency summary
        recent_emergencies = len([e for e in emergency_events if not e.get('resolved', True)])
        
        # Digital twin status
        current_risk = digital_twin_risk.get('current_state', 'Unknown')
        
        summary = f"""
PATIENT SUMMARY REPORT

Patient: {name}, Age {age}
Primary Condition: {condition}
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CURRENT STATUS:
The patient's digital twin indicates a {current_risk} status. {vitals_trend}

VITAL SIGNS ANALYSIS:
"""
        
        if latest_vitals:
            summary += f"""Current vital signs show:
- Heart Rate: {latest_vitals.get('heart_rate', 'N/A')} bpm
- Blood Pressure: {latest_vitals.get('bp_sys', 'N/A')}/{latest_vitals.get('bp_dia', 'N/A')} mmHg
- Temperature: {latest_vitals.get('temp', 'N/A')}°F
- Oxygen Saturation: {latest_vitals.get('o2_sat', 'N/A')}%

"""
        
        summary += f"""MEDICATION MANAGEMENT:
The patient is currently taking {med_count} medications. """
        
        if interaction_count > 0:
            summary += f"There are {interaction_count} potential drug interactions that require monitoring. "
        else:
            summary += "No significant drug interactions detected. "
        
        if emergency_events:
            if recent_emergencies > 0:
                summary += f"\n\nEMERGENCY EVENTS:\nThere are {recent_emergencies} active emergency situations requiring attention. "
            else:
                summary += f"\n\nEMERGENCY HISTORY:\nPatient has had {len(emergency_events)} emergency events, all resolved. "
        
        summary += f"\n\nOVERALL ASSESSMENT:\n{self._generate_overall_assessment(digital_twin_risk, vitals_history, medications, emergency_events)}"
        
        return summary.strip()
    
    def _analyze_vitals_trend(self, vitals_history):
        """Analyze trend in vital signs"""
        if len(vitals_history) < 2:
            return "Insufficient data for trend analysis."
        
        # Compare latest with previous readings
        latest = vitals_history[0]
        previous = vitals_history[1]
        
        trends = []
        
        # Heart rate trend
        hr_change = latest.get('heart_rate', 0) - previous.get('heart_rate', 0)
        if abs(hr_change) > 5:
            direction = "increased" if hr_change > 0 else "decreased"
            trends.append(f"Heart rate has {direction} by {abs(hr_change)} bpm")
        
        # Blood pressure trend
        bp_sys_change = latest.get('bp_sys', 0) - previous.get('bp_sys', 0)
        if abs(bp_sys_change) > 10:
            direction = "increased" if bp_sys_change > 0 else "decreased"
            trends.append(f"Systolic BP has {direction} by {abs(bp_sys_change)} mmHg")
        
        if trends:
            return "Recent trends show: " + ", ".join(trends) + "."
        else:
            return "Vital signs remain stable with minimal variation."
    
    def _generate_recommendations(self, vitals_history, medications, drug_interactions, 
                                emergency_events, digital_twin_risk):
        """Generate AI recommendations"""
        recommendations = []
        
        # Risk-based recommendations
        risk_level = digital_twin_risk.get('current_state', 'Unknown')
        
        if risk_level == 'High Risk':
            recommendations.extend([
                "Immediate medical evaluation recommended",
                "Increase monitoring frequency to every 4-6 hours",
                "Consider hospitalization or intensive outpatient monitoring",
                "Review and optimize current treatment plan"
            ])
        elif risk_level == 'Mild Risk':
            recommendations.extend([
                "Schedule follow-up appointment within 48-72 hours",
                "Monitor vital signs twice daily",
                "Review medication compliance and effectiveness"
            ])
        else:
            recommendations.extend([
                "Continue current monitoring schedule",
                "Maintain healthy lifestyle habits",
                "Regular check-ups as scheduled"
            ])
        
        # Medication recommendations
        high_risk_interactions = [i for i in drug_interactions if i.get('severity') == 'High']
        if high_risk_interactions:
            recommendations.append("URGENT: Review high-risk drug interactions with pharmacist")
        
        medium_risk_interactions = [i for i in drug_interactions if i.get('severity') == 'Medium']
        if medium_risk_interactions:
            recommendations.append("Monitor for side effects from moderate drug interactions")
        
        # Vitals-based recommendations
        if vitals_history:
            latest_vitals = vitals_history[0]
            
            if latest_vitals.get('bp_sys', 0) > 140:
                recommendations.append("Blood pressure management: reduce sodium, increase activity")
            
            if latest_vitals.get('heart_rate', 0) > 100:
                recommendations.append("Evaluate causes of elevated heart rate")
            
            if latest_vitals.get('o2_sat', 100) < 95:
                recommendations.append("Respiratory assessment recommended")
        
        # Emergency-based recommendations
        active_emergencies = [e for e in emergency_events if not e.get('resolved', True)]
        if active_emergencies:
            recommendations.append("Follow emergency protocols for active situations")
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def _assess_overall_risk(self, vitals_history, medications, drug_interactions, 
                           emergency_events, digital_twin_risk):
        """Assess overall patient risk"""
        risk_factors = []
        risk_score = 0
        
        # Digital twin risk
        current_risk = digital_twin_risk.get('current_state', 'Healthy')
        if current_risk == 'High Risk':
            risk_score += 30
            risk_factors.append('High digital twin risk level')
        elif current_risk == 'Mild Risk':
            risk_score += 15
            risk_factors.append('Moderate digital twin risk level')
        
        # Vitals risk
        if vitals_history:
            latest_vitals = vitals_history[0]
            
            if latest_vitals.get('bp_sys', 0) > 140:
                risk_score += 10
                risk_factors.append('Hypertension')
            
            if latest_vitals.get('heart_rate', 0) > 100:
                risk_score += 8
                risk_factors.append('Tachycardia')
            
            if latest_vitals.get('o2_sat', 100) < 95:
                risk_score += 15
                risk_factors.append('Low oxygen saturation')
        
        # Medication risk
        high_risk_interactions = len([i for i in drug_interactions if i.get('severity') == 'High'])
        if high_risk_interactions > 0:
            risk_score += high_risk_interactions * 12
            risk_factors.append(f'{high_risk_interactions} high-risk drug interactions')
        
        # Emergency risk
        active_emergencies = len([e for e in emergency_events if not e.get('resolved', True)])
        if active_emergencies > 0:
            risk_score += active_emergencies * 20
            risk_factors.append(f'{active_emergencies} active emergency situations')
        
        # Determine overall risk level
        if risk_score >= 50:
            overall_risk = 'High'
        elif risk_score >= 25:
            overall_risk = 'Moderate'
        else:
            overall_risk = 'Low'
        
        return {
            'overall_risk_level': overall_risk,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'assessment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _extract_key_metrics(self, vitals_history):
        """Extract key metrics from vitals history"""
        if not vitals_history:
            return {}
        
        # Calculate averages and ranges
        heart_rates = [v.get('heart_rate', 0) for v in vitals_history if v.get('heart_rate')]
        bp_sys_values = [v.get('bp_sys', 0) for v in vitals_history if v.get('bp_sys')]
        
        metrics = {}
        
        if heart_rates:
            metrics['avg_heart_rate'] = sum(heart_rates) / len(heart_rates)
            metrics['hr_range'] = f"{min(heart_rates)}-{max(heart_rates)}"
        
        if bp_sys_values:
            metrics['avg_systolic_bp'] = sum(bp_sys_values) / len(bp_sys_values)
            metrics['bp_range'] = f"{min(bp_sys_values)}-{max(bp_sys_values)}"
        
        return metrics
    
    def _analyze_medications(self, medications, drug_interactions):
        """Analyze medication regimen"""
        analysis = {
            'total_medications': len(medications),
            'medication_classes': [],
            'interaction_summary': {
                'high_risk': len([i for i in drug_interactions if i.get('severity') == 'High']),
                'medium_risk': len([i for i in drug_interactions if i.get('severity') == 'Medium']),
                'low_risk': len([i for i in drug_interactions if i.get('severity') == 'Low'])
            }
        }
        
        # Classify medications (simplified)
        for med in medications:
            med_name = med.get('name', '').lower()
            if any(word in med_name for word in ['lisinopril', 'amlodipine', 'losartan']):
                analysis['medication_classes'].append('Antihypertensive')
            elif any(word in med_name for word in ['metformin', 'insulin']):
                analysis['medication_classes'].append('Antidiabetic')
            elif any(word in med_name for word in ['atorvastatin', 'simvastatin']):
                analysis['medication_classes'].append('Statin')
        
        analysis['medication_classes'] = list(set(analysis['medication_classes']))
        
        return analysis
    
    def _summarize_emergencies(self, emergency_events):
        """Summarize emergency events"""
        if not emergency_events:
            return {'total_events': 0, 'active_events': 0, 'resolved_events': 0}
        
        active_events = len([e for e in emergency_events if not e.get('resolved', True)])
        resolved_events = len([e for e in emergency_events if e.get('resolved', True)])
        
        return {
            'total_events': len(emergency_events),
            'active_events': active_events,
            'resolved_events': resolved_events,
            'most_recent': emergency_events[0] if emergency_events else None
        }
    
    def _generate_overall_assessment(self, digital_twin_risk, vitals_history, medications, emergency_events):
        """Generate overall clinical assessment"""
        risk_level = digital_twin_risk.get('current_state', 'Unknown')
        
        if risk_level == 'High Risk':
            assessment = "Patient requires immediate attention and close monitoring. Multiple risk factors present."
        elif risk_level == 'Mild Risk':
            assessment = "Patient shows some concerning indicators that warrant increased monitoring and possible intervention."
        else:
            assessment = "Patient appears stable with manageable health indicators."
        
        # Add specific concerns
        concerns = []
        
        if vitals_history and vitals_history[0].get('bp_sys', 0) > 140:
            concerns.append("elevated blood pressure")
        
        if len([e for e in emergency_events if not e.get('resolved', True)]) > 0:
            concerns.append("active emergency situations")
        
        if len(medications) > 5:
            concerns.append("complex medication regimen")
        
        if concerns:
            assessment += f" Key areas of concern include: {', '.join(concerns)}."
        
        assessment += " Continued monitoring and adherence to treatment plan recommended."
        
        return assessment
