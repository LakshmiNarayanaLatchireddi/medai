"""
Emergency Agent - Provides AI-powered emergency response and first-aid guidance
"""

from datetime import datetime

class EmergencyAgent:
    def __init__(self):
        self.name = "EmergencyAgent"
        self.version = "1.0"
        
        # Emergency protocols database
        self.emergency_protocols = {
            'Fainting': {
                'severity': 'Medium',
                'safety_alert': 'Ensure person is in safe location away from hazards',
                'steps': [
                    'Check if person is responsive by gently tapping shoulders and calling their name',
                    'If unresponsive, check for breathing and pulse',
                    'Position person on their back and elevate legs 8-12 inches',
                    'Loosen tight clothing around neck and waist',
                    'Check for injuries from falling',
                    'Monitor breathing and pulse continuously',
                    'When person regains consciousness, help them sit up slowly',
                    'Offer water if fully alert and able to swallow'
                ],
                'call_911_if': [
                    'Person does not regain consciousness within 1-2 minutes',
                    'Person has difficulty breathing or no pulse',
                    'Person has chest pain or irregular heartbeat',
                    'Person has a head injury from falling',
                    'Person has diabetes, heart disease, or is pregnant'
                ],
                'recommendations': [
                    'Have person rest for at least 10-15 minutes',
                    'Monitor for recurring episodes',
                    'Encourage medical evaluation if first-time fainting',
                    'Check blood sugar if diabetic'
                ]
            },
            
            'Chest Pain': {
                'severity': 'High',
                'safety_alert': 'This could be a heart attack - act quickly but stay calm',
                'steps': [
                    'Call 911 immediately - do not delay',
                    'Help person sit in comfortable position, slightly upright',
                    'Loosen tight clothing around chest and neck',
                    'If person takes heart medication (nitroglycerin), help them take it',
                    'If person is conscious and not allergic, give 1 adult aspirin to chew',
                    'Stay with person and monitor breathing and consciousness',
                    'Be prepared to perform CPR if person becomes unresponsive',
                    'Note time symptoms started and any triggers'
                ],
                'call_911_if': [
                    'Any chest pain lasting more than 5 minutes',
                    'Pain spreads to arm, jaw, neck, or back',
                    'Person has shortness of breath',
                    'Person is sweating, nauseous, or dizzy',
                    'Person has history of heart disease'
                ],
                'recommendations': [
                    'Do not leave person alone',
                    'Do not give food or water',
                    'Keep person calm and reassured',
                    'Have emergency contact information ready'
                ]
            },
            
            'Dizziness': {
                'severity': 'Low',
                'safety_alert': 'Prevent falls by ensuring person is in safe position',
                'steps': [
                    'Help person sit down immediately in a safe location',
                    'Have person put head between knees or lie down with legs elevated',
                    'Ensure adequate ventilation and fresh air',
                    'Loosen tight clothing',
                    'Check if person has eaten recently or is dehydrated',
                    'Monitor for improvement over 5-10 minutes',
                    'Help person stand slowly when dizziness subsides',
                    'Offer water if person is alert and able to swallow'
                ],
                'call_911_if': [
                    'Dizziness is severe and persistent',
                    'Person has chest pain or difficulty breathing',
                    'Person has severe headache or vision changes',
                    'Person has weakness or numbness',
                    'Person has history of heart problems or stroke'
                ],
                'recommendations': [
                    'Encourage slow movements and position changes',
                    'Ensure adequate hydration',
                    'Monitor blood pressure if possible',
                    'Avoid driving until symptoms resolve'
                ]
            },
            
            'Difficulty Breathing': {
                'severity': 'High',
                'safety_alert': 'Breathing problems require immediate attention',
                'steps': [
                    'Call 911 if severe breathing difficulty',
                    'Help person sit upright in comfortable position',
                    'Loosen tight clothing around chest and neck',
                    'Encourage slow, deep breathing',
                    'If person has rescue inhaler, help them use it',
                    'Stay calm and reassure the person',
                    'Monitor breathing rate and effort',
                    'Be prepared to perform rescue breathing if needed'
                ],
                'call_911_if': [
                    'Person cannot speak in full sentences',
                    'Lips or fingernails turn blue',
                    'Person is using accessory muscles to breathe',
                    'Breathing is very rapid or very slow',
                    'Person becomes confused or drowsy'
                ],
                'recommendations': [
                    'Keep person calm to reduce oxygen demand',
                    'Ensure good air circulation',
                    'Do not leave person alone',
                    'Have rescue medications readily available'
                ]
            },
            
            'Severe Headache': {
                'severity': 'Medium',
                'safety_alert': 'Sudden severe headache may indicate serious condition',
                'steps': [
                    'Have person rest in quiet, dark room',
                    'Apply cold compress to forehead or neck',
                    'Encourage person to lie down comfortably',
                    'Monitor for changes in consciousness or behavior',
                    'Check if person has taken any medications',
                    'Note any associated symptoms (nausea, vision changes)',
                    'Encourage gentle neck stretches if no injury suspected',
                    'Offer water if person can swallow normally'
                ],
                'call_911_if': [
                    'Headache is sudden and described as "worst ever"',
                    'Person has fever, stiff neck, or rash',
                    'Person has confusion or altered mental state',
                    'Person has vision changes or weakness',
                    'Headache follows head injury'
                ],
                'recommendations': [
                    'Avoid bright lights and loud noises',
                    'Monitor for worsening symptoms',
                    'Keep record of headache triggers',
                    'Encourage medical evaluation for severe headaches'
                ]
            },
            
            'Allergic Reaction': {
                'severity': 'High',
                'safety_alert': 'Severe allergic reactions can be life-threatening',
                'steps': [
                    'Remove or avoid the allergen if known',
                    'If person has epinephrine auto-injector, help them use it',
                    'Call 911 immediately for severe reactions',
                    'Help person sit upright if breathing is difficult',
                    'Loosen tight clothing',
                    'Monitor breathing and consciousness closely',
                    'Be prepared to perform CPR if needed',
                    'Give antihistamine if available and person is conscious'
                ],
                'call_911_if': [
                    'Person has difficulty breathing or swallowing',
                    'Person has swelling of face, lips, or tongue',
                    'Person has rapid pulse or dizziness',
                    'Person has widespread rash or hives',
                    'Person becomes unconscious'
                ],
                'recommendations': [
                    'Stay with person until help arrives',
                    'Keep person calm and reassured',
                    'Do not give anything by mouth if swallowing is difficult',
                    'Have emergency medications readily available'
                ]
            }
        }
    
    def run(self, emergency_type):
        """
        Provide emergency response guidance
        
        Args:
            emergency_type (str): Type of emergency
        
        Returns:
            dict: Emergency response protocol
        """
        try:
            if emergency_type in self.emergency_protocols:
                protocol = self.emergency_protocols[emergency_type].copy()
                protocol['timestamp'] = datetime.now()
                protocol['emergency_type'] = emergency_type
                return protocol
            else:
                return self._get_general_emergency_response(emergency_type)
        except Exception as e:
            return {
                'error': f'Emergency protocol retrieval failed: {str(e)}',
                'emergency_type': emergency_type,
                'general_advice': 'Call 911 for any serious medical emergency'
            }
    
    def _get_general_emergency_response(self, emergency_type):
        """Provide general emergency response for unknown emergency types"""
        return {
            'emergency_type': emergency_type,
            'severity': 'Medium',
            'safety_alert': 'Ensure scene safety and call for help if needed',
            'steps': [
                'Assess the situation and ensure scene safety',
                'Check if person is conscious and responsive',
                'Call 911 if situation appears serious',
                'Provide comfort and reassurance',
                'Monitor vital signs if trained to do so',
                'Do not move person unless in immediate danger',
                'Stay with person until help arrives',
                'Provide clear information to emergency responders'
            ],
            'call_911_if': [
                'Person is unconscious or unresponsive',
                'Person has difficulty breathing',
                'Person has severe pain or distress',
                'You are unsure about the severity',
                'Situation appears life-threatening'
            ],
            'recommendations': [
                'Stay calm and think clearly',
                'Use universal precautions if contact with bodily fluids',
                'Document what happened for medical personnel',
                'Follow up with healthcare provider'
            ],
            'timestamp': datetime.now()
        }
    
    def get_emergency_contacts(self):
        """Get emergency contact information"""
        return {
            'emergency_services': '911',
            'poison_control': '1-800-222-1222',
            'mental_health_crisis': '988',
            'general_info': {
                'when_to_call_911': [
                    'Life-threatening emergencies',
                    'Severe injuries',
                    'Chest pain or heart attack symptoms',
                    'Difficulty breathing',
                    'Severe allergic reactions',
                    'Loss of consciousness',
                    'Severe bleeding',
                    'Suspected stroke symptoms'
                ],
                'what_to_tell_911': [
                    'Your location and phone number',
                    'Nature of the emergency',
                    'Number of people involved',
                    'Condition of the person(s)',
                    'Any immediate dangers',
                    'First aid being provided'
                ]
            }
        }
    
    def assess_emergency_severity(self, symptoms):
        """
        Assess emergency severity based on symptoms
        
        Args:
            symptoms (list): List of symptoms
        
        Returns:
            dict: Severity assessment
        """
        high_severity_indicators = [
            'unconscious', 'not breathing', 'no pulse', 'severe bleeding',
            'chest pain', 'difficulty breathing', 'severe allergic reaction',
            'stroke symptoms', 'severe burns', 'poisoning'
        ]
        
        medium_severity_indicators = [
            'moderate pain', 'dizziness', 'nausea', 'vomiting',
            'mild breathing difficulty', 'confusion', 'severe headache'
        ]
        
        symptoms_lower = [s.lower() for s in symptoms]
        
        if any(indicator in ' '.join(symptoms_lower) for indicator in high_severity_indicators):
            return {
                'severity': 'High',
                'recommendation': 'Call 911 immediately',
                'urgency': 'Immediate action required'
            }
        elif any(indicator in ' '.join(symptoms_lower) for indicator in medium_severity_indicators):
            return {
                'severity': 'Medium',
                'recommendation': 'Seek medical attention soon',
                'urgency': 'Monitor closely and consider calling healthcare provider'
            }
        else:
            return {
                'severity': 'Low',
                'recommendation': 'Monitor symptoms and seek care if worsening',
                'urgency': 'Non-urgent but should be evaluated'
            }
    
    def get_cpr_instructions(self):
        """Get CPR instructions"""
        return {
            'adult_cpr': {
                'steps': [
                    'Check responsiveness and breathing',
                    'Call 911 and get AED if available',
                    'Place person on firm, flat surface',
                    'Tilt head back, lift chin to open airway',
                    'Place heel of hand on center of chest between nipples',
                    'Place other hand on top, interlace fingers',
                    'Push hard and fast at least 2 inches deep',
                    'Allow complete chest recoil between compressions',
                    'Compress at rate of 100-120 per minute',
                    'Give 30 compressions, then 2 rescue breaths',
                    'Continue cycles until help arrives or person responds'
                ],
                'important_notes': [
                    'Do not be afraid to push hard',
                    'Minimize interruptions',
                    'Switch with another person every 2 minutes if possible',
                    'Continue until emergency services arrive'
                ]
            },
            'aed_use': {
                'steps': [
                    'Turn on AED and follow voice prompts',
                    'Remove clothing from chest and wipe dry',
                    'Attach pads as shown in pictures',
                    'Ensure no one is touching person',
                    'Press analyze button if required',
                    'If shock advised, ensure everyone is clear',
                    'Press shock button when prompted',
                    'Resume CPR immediately after shock'
                ]
            }
        }
    
    def get_first_aid_basics(self):
        """Get basic first aid information"""
        return {
            'bleeding_control': [
                'Apply direct pressure with clean cloth',
                'Elevate injured area above heart if possible',
                'Do not remove embedded objects',
                'Apply pressure points if bleeding continues',
                'Seek medical attention for severe bleeding'
            ],
            'burn_treatment': [
                'Cool burn with cool (not cold) water for 10-20 minutes',
                'Remove jewelry before swelling occurs',
                'Do not break blisters',
                'Cover with sterile, non-adhesive bandage',
                'Seek medical attention for severe burns'
            ],
            'choking_adult': [
                'Encourage coughing if person can speak',
                'Give 5 back blows between shoulder blades',
                'Give 5 abdominal thrusts (Heimlich maneuver)',
                'Alternate back blows and abdominal thrusts',
                'Call 911 if object not dislodged',
                'Be prepared to perform CPR if person becomes unconscious'
            ],
            'shock_treatment': [
                'Have person lie down with legs elevated',
                'Keep person warm with blankets',
                'Do not give food or water',
                'Monitor breathing and pulse',
                'Seek immediate medical attention'
            ]
        }
