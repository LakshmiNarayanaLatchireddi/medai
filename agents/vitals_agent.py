"""
Vitals Agent - Analyzes patient vital signs and provides health status assessment
"""

import random
from datetime import datetime

class VitalsAgent:
    def __init__(self):
        self.name = "VitalsAgent"
        self.version = "1.0"
        
        # Normal ranges for vital signs
        self.normal_ranges = {
            'heart_rate': {'min': 60, 'max': 100},
            'blood_pressure_sys': {'min': 90, 'max': 120},
            'blood_pressure_dia': {'min': 60, 'max': 80},
            'temperature': {'min': 97.0, 'max': 99.5},
            'oxygen_saturation': {'min': 95, 'max': 100}
        }
    
    def run(self, vitals_data):
        """
        Analyze vital signs and return health status assessment
        
        Args:
            vitals_data (dict): Dictionary containing vital signs
                - heart_rate: int
                - blood_pressure_sys: int
                - blood_pressure_dia: int
                - temperature: float
                - oxygen_saturation: int
        
        Returns:
            dict: Analysis results with status, reason, and suggestions
        """
        try:
            analysis = self._analyze_vitals(vitals_data)
            return analysis
        except Exception as e:
            return {
                'status': 'Error',
                'reason': f'Failed to analyze vitals: {str(e)}',
                'suggestion': 'Please check vital signs data and try again',
                'risk_level': 'Unknown'
            }
    
    def _analyze_vitals(self, vitals):
        """Internal method to analyze vital signs"""
        issues = []
        risk_factors = []
        
        # Analyze heart rate
        hr = vitals.get('heart_rate', 0)
        if hr < self.normal_ranges['heart_rate']['min']:
            issues.append(f"Low heart rate ({hr} bpm)")
            risk_factors.append('bradycardia')
        elif hr > self.normal_ranges['heart_rate']['max']:
            issues.append(f"High heart rate ({hr} bpm)")
            risk_factors.append('tachycardia')
        
        # Analyze blood pressure
        bp_sys = vitals.get('blood_pressure_sys', 0)
        bp_dia = vitals.get('blood_pressure_dia', 0)
        
        if bp_sys > 140 or bp_dia > 90:
            issues.append(f"High blood pressure ({bp_sys}/{bp_dia})")
            risk_factors.append('hypertension')
        elif bp_sys < 90 or bp_dia < 60:
            issues.append(f"Low blood pressure ({bp_sys}/{bp_dia})")
            risk_factors.append('hypotension')
        
        # Analyze temperature
        temp = vitals.get('temperature', 0)
        if temp > self.normal_ranges['temperature']['max']:
            issues.append(f"Elevated temperature ({temp}°F)")
            risk_factors.append('fever')
        elif temp < self.normal_ranges['temperature']['min']:
            issues.append(f"Low temperature ({temp}°F)")
            risk_factors.append('hypothermia')
        
        # Analyze oxygen saturation
        o2_sat = vitals.get('oxygen_saturation', 0)
        if o2_sat < self.normal_ranges['oxygen_saturation']['min']:
            issues.append(f"Low oxygen saturation ({o2_sat}%)")
            risk_factors.append('hypoxemia')
        
        # Determine overall status
        if not issues:
            return {
                'status': 'Normal',
                'reason': 'All vital signs are within normal ranges',
                'suggestion': 'Continue regular monitoring and maintain healthy lifestyle',
                'risk_level': 'Low',
                'risk_factors': []
            }
        elif len(issues) == 1 and not any(rf in ['hypertension', 'tachycardia', 'hypoxemia'] for rf in risk_factors):
            return {
                'status': 'Mild Concern',
                'reason': f'Minor deviation detected: {issues[0]}',
                'suggestion': 'Monitor closely and consider consulting healthcare provider if symptoms persist',
                'risk_level': 'Mild',
                'risk_factors': risk_factors
            }
        else:
            return {
                'status': 'Attention Required',
                'reason': f'Multiple abnormal readings: {", ".join(issues)}',
                'suggestion': 'Recommend immediate consultation with healthcare provider',
                'risk_level': 'High',
                'risk_factors': risk_factors
            }
    
    def get_recommendations(self, vitals_data):
        """Get specific recommendations based on vital signs"""
        recommendations = []
        
        hr = vitals_data.get('heart_rate', 0)
        bp_sys = vitals_data.get('blood_pressure_sys', 0)
        bp_dia = vitals_data.get('blood_pressure_dia', 0)
        temp = vitals_data.get('temperature', 0)
        o2_sat = vitals_data.get('oxygen_saturation', 0)
        
        # Heart rate recommendations
        if hr > 100:
            recommendations.extend([
                "Avoid caffeine and stimulants",
                "Practice deep breathing exercises",
                "Ensure adequate rest and sleep"
            ])
        elif hr < 60:
            recommendations.extend([
                "Monitor for dizziness or fatigue",
                "Consider light physical activity if cleared by doctor"
            ])
        
        # Blood pressure recommendations
        if bp_sys > 140 or bp_dia > 90:
            recommendations.extend([
                "Reduce sodium intake",
                "Increase physical activity gradually",
                "Monitor blood pressure regularly",
                "Consider stress reduction techniques"
            ])
        
        # Temperature recommendations
        if temp > 99.5:
            recommendations.extend([
                "Stay hydrated with plenty of fluids",
                "Rest and avoid strenuous activity",
                "Monitor temperature regularly"
            ])
        
        # Oxygen saturation recommendations
        if o2_sat < 95:
            recommendations.extend([
                "Ensure proper posture for breathing",
                "Avoid smoking and secondhand smoke",
                "Seek immediate medical attention if breathing difficulty occurs"
            ])
        
        return recommendations if recommendations else ["Continue current health maintenance routine"]
    
    def predict_risk_trend(self, historical_vitals):
        """Predict risk trend based on historical data"""
        if not historical_vitals or len(historical_vitals) < 2:
            return "Insufficient data for trend analysis"
        
        # Simple trend analysis (in real implementation, use ML models)
        recent_risks = []
        for vitals in historical_vitals[-5:]:  # Last 5 readings
            analysis = self._analyze_vitals(vitals)
            risk_score = {'Low': 1, 'Mild': 2, 'High': 3}.get(analysis['risk_level'], 1)
            recent_risks.append(risk_score)
        
        if len(recent_risks) >= 2:
            trend = recent_risks[-1] - recent_risks[0]
            if trend > 0:
                return "Increasing risk trend - closer monitoring recommended"
            elif trend < 0:
                return "Improving trend - continue current care plan"
            else:
                return "Stable trend - maintain current monitoring"
        
        return "Stable condition"
    
    def get_current_vitals(self):
        """Generate realistic current vital signs with some variation"""
        # Generate realistic vital signs with small random variations
        return {
            'heart_rate': random.randint(65, 95),
            'blood_pressure_systolic': random.randint(110, 135),
            'blood_pressure_diastolic': random.randint(65, 85),
            'temperature': round(random.uniform(97.5, 99.2), 1),
            'oxygen_saturation': random.randint(96, 100),
            'timestamp': datetime.now()
        }
