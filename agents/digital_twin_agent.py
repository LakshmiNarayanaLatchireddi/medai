"""
Digital Twin Agent - Manages the digital twin state and risk assessment
"""

from datetime import datetime
import json

class DigitalTwinAgent:
    def __init__(self):
        self.name = "DigitalTwinAgent"
        self.version = "1.0"
        
        # Initialize digital twin state
        self.current_state = {
            'risk_level': 'Healthy',
            'last_updated': datetime.now(),
            'risk_factors': [],
            'health_score': 85,
            'active_conditions': [],
            'medication_effects': [],
            'emergency_events': []
        }
        
        # Risk level definitions
        self.risk_levels = {
            'Healthy': {'score_range': (80, 100), 'color': '#10b981'},
            'Mild Risk': {'score_range': (60, 79), 'color': '#f59e0b'},
            'High Risk': {'score_range': (0, 59), 'color': '#ef4444'}
        }
    
    def run(self, event_type, event_data):
        """
        Update digital twin state based on events
        
        Args:
            event_type (str): Type of event (vitals_update, medicine_intake, emergency, etc.)
            event_data (dict): Event-specific data
        
        Returns:
            dict: Updated digital twin state
        """
        try:
            if event_type == "vitals_update":
                return self._handle_vitals_update(event_data)
            elif event_type == "medicine_intake":
                return self._handle_medicine_intake(event_data)
            elif event_type == "drug_interaction":
                return self._handle_drug_interaction(event_data)
            elif event_type == "emergency":
                return self._handle_emergency(event_data)
            elif event_type == "emergency_resolved":
                return self._handle_emergency_resolved()
            else:
                return self._get_current_state()
        except Exception as e:
            return {
                'error': f'Digital twin update failed: {str(e)}',
                'risk_level': self.current_state['risk_level']
            }
    
    def _handle_vitals_update(self, vitals_data):
        """Handle vital signs update"""
        risk_factors = []
        health_impact = 0
        
        # Analyze vital signs impact
        hr = vitals_data.get('heart_rate', 0)
        bp_sys = vitals_data.get('blood_pressure_sys', 0)
        bp_dia = vitals_data.get('blood_pressure_dia', 0)
        temp = vitals_data.get('temperature', 0)
        o2_sat = vitals_data.get('oxygen_saturation', 0)
        
        # Heart rate impact
        if hr > 100:
            risk_factors.append('Tachycardia')
            health_impact -= 10
        elif hr < 60:
            risk_factors.append('Bradycardia')
            health_impact -= 5
        
        # Blood pressure impact
        if bp_sys > 140 or bp_dia > 90:
            risk_factors.append('Hypertension')
            health_impact -= 15
        elif bp_sys < 90 or bp_dia < 60:
            risk_factors.append('Hypotension')
            health_impact -= 10
        
        # Temperature impact
        if temp > 99.5:
            risk_factors.append('Fever')
            health_impact -= 8
        elif temp < 97.0:
            risk_factors.append('Hypothermia')
            health_impact -= 12
        
        # Oxygen saturation impact
        if o2_sat < 95:
            risk_factors.append('Hypoxemia')
            health_impact -= 20
        
        # Update state
        self.current_state['risk_factors'] = list(set(self.current_state['risk_factors'] + risk_factors))
        self.current_state['health_score'] = max(0, min(100, self.current_state['health_score'] + health_impact))
        self.current_state['last_updated'] = datetime.now()
        
        # Update risk level based on health score
        self._update_risk_level()
        
        return self._get_current_state()
    
    def _handle_medicine_intake(self, medicine_data):
        """Handle medicine intake event"""
        medicine = medicine_data.get('medicine', '')
        interaction = medicine_data.get('interaction', {})
        
        # Add to medication effects
        effect = {
            'medicine': medicine,
            'timestamp': datetime.now(),
            'interaction_severity': interaction.get('severity', 'None')
        }
        
        self.current_state['medication_effects'].append(effect)
        
        # Keep only last 10 medication effects
        if len(self.current_state['medication_effects']) > 10:
            self.current_state['medication_effects'] = self.current_state['medication_effects'][-10:]
        
        # Adjust health score based on interaction severity
        severity = interaction.get('severity', 'None')
        if severity == 'High':
            self.current_state['health_score'] = max(0, self.current_state['health_score'] - 25)
            self.current_state['risk_factors'].append('High-Risk Drug Interaction')
        elif severity == 'Medium':
            self.current_state['health_score'] = max(0, self.current_state['health_score'] - 10)
            self.current_state['risk_factors'].append('Moderate Drug Interaction')
        elif severity == 'Low':
            self.current_state['health_score'] = max(0, self.current_state['health_score'] - 3)
        
        self.current_state['last_updated'] = datetime.now()
        self._update_risk_level()
        
        return self._get_current_state()
    
    def _handle_drug_interaction(self, interaction_data):
        """Handle drug-drug interaction analysis"""
        severity = interaction_data.get('severity', 'None')
        
        # Update risk factors based on interaction severity
        if severity == 'High':
            self.current_state['health_score'] = max(0, self.current_state['health_score'] - 30)
            self.current_state['risk_factors'].append('Severe Drug Interaction')
        elif severity == 'Medium':
            self.current_state['health_score'] = max(0, self.current_state['health_score'] - 15)
            self.current_state['risk_factors'].append('Moderate Drug Interaction')
        elif severity == 'Low':
            self.current_state['health_score'] = max(0, self.current_state['health_score'] - 5)
            self.current_state['risk_factors'].append('Minor Drug Interaction')
        
        self.current_state['last_updated'] = datetime.now()
        self._update_risk_level()
        
        return self._get_current_state()
    
    def _handle_emergency(self, emergency_data):
        """Handle emergency event"""
        emergency_type = emergency_data.get('type', 'Unknown')
        severity = emergency_data.get('severity', 'Medium')
        
        # Add emergency event
        emergency_event = {
            'type': emergency_type,
            'severity': severity,
            'timestamp': datetime.now(),
            'status': 'Active'
        }
        
        self.current_state['emergency_events'].append(emergency_event)
        
        # Significant health score impact for emergencies
        severity_impact = {
            'High': -40,
            'Medium': -25,
            'Low': -10
        }
        
        impact = severity_impact.get(severity, -25)
        self.current_state['health_score'] = max(0, self.current_state['health_score'] + impact)
        
        # Add emergency as risk factor
        self.current_state['risk_factors'].append(f'Active Emergency: {emergency_type}')
        
        self.current_state['last_updated'] = datetime.now()
        self._update_risk_level()
        
        return self._get_current_state()
    
    def _handle_emergency_resolved(self):
        """Handle emergency resolution"""
        # Mark recent emergencies as resolved
        for event in self.current_state['emergency_events']:
            if event.get('status') == 'Active':
                event['status'] = 'Resolved'
                event['resolved_at'] = datetime.now()
        
        # Remove active emergency risk factors
        self.current_state['risk_factors'] = [
            rf for rf in self.current_state['risk_factors'] 
            if not rf.startswith('Active Emergency:')
        ]
        
        # Improve health score slightly
        self.current_state['health_score'] = min(100, self.current_state['health_score'] + 15)
        
        self.current_state['last_updated'] = datetime.now()
        self._update_risk_level()
        
        return self._get_current_state()
    
    def _update_risk_level(self):
        """Update risk level based on current health score"""
        score = self.current_state['health_score']
        
        for level, data in self.risk_levels.items():
            min_score, max_score = data['score_range']
            if min_score <= score <= max_score:
                self.current_state['risk_level'] = level
                break
    
    def _get_current_state(self):
        """Get current digital twin state"""
        return {
            'risk_level': self.current_state['risk_level'],
            'health_score': self.current_state['health_score'],
            'risk_factors': self.current_state['risk_factors'],
            'last_updated': self.current_state['last_updated'],
            'active_conditions': self.current_state['active_conditions'],
            'medication_effects': self.current_state['medication_effects'][-5:],  # Last 5 effects
            'emergency_events': self.current_state['emergency_events'][-3:],  # Last 3 events
            'visual_state': self._get_visual_state()
        }
    
    def _get_visual_state(self):
        """Get visual representation state for 3D model"""
        risk_level = self.current_state['risk_level']
        
        visual_states = {
            'Healthy': {
                'glow_color': '#10b981',
                'intensity': 'low',
                'animation': 'gentle_pulse',
                'filter': 'hue-rotate(120deg) saturate(1.1) brightness(1.05)'
            },
            'Mild Risk': {
                'glow_color': '#f59e0b',
                'intensity': 'medium',
                'animation': 'moderate_pulse',
                'filter': 'hue-rotate(45deg) saturate(1.3) brightness(1.1)'
            },
            'High Risk': {
                'glow_color': '#ef4444',
                'intensity': 'high',
                'animation': 'urgent_pulse',
                'filter': 'hue-rotate(0deg) saturate(1.5) brightness(1.2)'
            }
        }
        
        return visual_states.get(risk_level, visual_states['Healthy'])
    
    def get_risk_assessment(self):
        """Get detailed risk assessment"""
        return {
            'current_risk_level': self.current_state['risk_level'],
            'health_score': self.current_state['health_score'],
            'risk_factors': self.current_state['risk_factors'],
            'recommendations': self._get_risk_recommendations(),
            'trend': self._calculate_risk_trend(),
            'next_assessment_due': self._get_next_assessment_time()
        }
    
    def _get_risk_recommendations(self):
        """Get recommendations based on current risk factors"""
        recommendations = []
        
        risk_factors = self.current_state['risk_factors']
        
        if 'Hypertension' in risk_factors:
            recommendations.extend([
                "Monitor blood pressure regularly",
                "Reduce sodium intake",
                "Increase physical activity gradually"
            ])
        
        if 'Tachycardia' in risk_factors:
            recommendations.extend([
                "Avoid caffeine and stimulants",
                "Practice stress reduction techniques",
                "Ensure adequate rest"
            ])
        
        if any('Drug Interaction' in rf for rf in risk_factors):
            recommendations.extend([
                "Review all medications with healthcare provider",
                "Monitor for adverse effects",
                "Consider medication timing adjustments"
            ])
        
        if any('Emergency' in rf for rf in risk_factors):
            recommendations.extend([
                "Follow emergency care instructions",
                "Monitor symptoms closely",
                "Maintain contact with healthcare provider"
            ])
        
        if not recommendations:
            recommendations = [
                "Continue current health maintenance routine",
                "Regular monitoring and check-ups",
                "Maintain healthy lifestyle habits"
            ]
        
        return recommendations
    
    def _calculate_risk_trend(self):
        """Calculate risk trend (simplified)"""
        # In a real implementation, this would analyze historical data
        current_score = self.current_state['health_score']
        
        if current_score >= 80:
            return "Stable - Low Risk"
        elif current_score >= 60:
            return "Stable - Moderate Risk"
        else:
            return "Concerning - High Risk"
    
    def _get_next_assessment_time(self):
        """Get next recommended assessment time"""
        risk_level = self.current_state['risk_level']
        
        if risk_level == 'High Risk':
            return "Within 24 hours"
        elif risk_level == 'Mild Risk':
            return "Within 72 hours"
        else:
            return "Within 1 week"
    
    def reset_state(self):
        """Reset digital twin to healthy state"""
        self.current_state = {
            'risk_level': 'Healthy',
            'last_updated': datetime.now(),
            'risk_factors': [],
            'health_score': 85,
            'active_conditions': [],
            'medication_effects': [],
            'emergency_events': []
        }
        return self._get_current_state()
