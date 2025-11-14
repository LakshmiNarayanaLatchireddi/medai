"""
Medicine Agent - Analyzes drug interactions using the drug interactions dataset
"""

import pandas as pd
import os

class MedicineAgent:
    def __init__(self):
        self.name = "MedicineAgent"
        self.version = "1.0"
        self.interactions_df = None
        self._load_interactions_data()
    
    def _load_interactions_data(self):
        """Load drug interactions data from CSV"""
        try:
            # Try multiple paths for the CSV file
            possible_paths = [
                'db_drug_interactions.csv',  # Original file in root
                os.path.join('data', 'drug_interactions.csv'),  # Data directory
                'drug_interactions.csv'  # Current directory
            ]
            
            for csv_path in possible_paths:
                if os.path.exists(csv_path):
                    print(f"Loading drug interactions from: {csv_path}")
                    self.interactions_df = pd.read_csv(csv_path)
                    print(f"Loaded {len(self.interactions_df)} drug interactions")
                    return
            
            print("Warning: Drug interactions CSV not found. Using fallback data.")
            self.interactions_df = None
        except Exception as e:
            print(f"Error loading drug interactions data: {e}")
            self.interactions_df = None
    
    def run(self, drug_a, drug_b=None):
        """
        Analyze drug interactions
        
        Args:
            drug_a (str): First drug name
            drug_b (str, optional): Second drug name for interaction check
        
        Returns:
            dict: Interaction analysis results
        """
        try:
            if drug_b is None:
                # Single drug analysis
                return self._analyze_single_drug(drug_a)
            else:
                # Drug-drug interaction analysis
                return self._analyze_drug_interaction(drug_a, drug_b)
        except Exception as e:
            return {
                'severity': 'Error',
                'explanation': f'Failed to analyze drug interaction: {str(e)}',
                'recommendation': 'Please consult healthcare provider',
                'affected_systems': []
            }
    
    def _analyze_single_drug(self, drug_name):
        """Analyze single drug for potential interactions with common medications"""
        if self.interactions_df is None:
            return self._fallback_single_drug_analysis(drug_name)
        
        # Find all interactions involving this drug
        drug_interactions = self.interactions_df[
            (self.interactions_df['Drug 1'].str.contains(drug_name, case=False, na=False)) |
            (self.interactions_df['Drug 2'].str.contains(drug_name, case=False, na=False))
        ]
        
        if drug_interactions.empty:
            return {
                'severity': 'None',
                'explanation': f'No significant interactions found for {drug_name} in our database',
                'recommendation': 'Generally safe, but always inform healthcare providers of all medications',
                'affected_systems': [],
                'interaction_count': 0
            }
        
        # Analyze severity based on interaction descriptions
        interaction_count = len(drug_interactions)
        severity = self._determine_severity_from_descriptions(drug_interactions['Interaction Description'].tolist())
        
        return {
            'severity': severity,
            'explanation': f'{drug_name} has {interaction_count} known interactions in our database',
            'recommendation': 'Review all current medications with healthcare provider',
            'affected_systems': self._extract_affected_systems(drug_interactions['Interaction Description'].tolist()),
            'interaction_count': interaction_count
        }
    
    def _analyze_drug_interaction(self, drug_a, drug_b):
        """Analyze interaction between two specific drugs"""
        if self.interactions_df is None:
            return self._fallback_interaction_analysis(drug_a, drug_b)
        
        # Search for direct interaction
        interaction = self._find_interaction(drug_a, drug_b)
        
        if interaction is not None:
            severity = self._determine_severity_from_description(interaction)
            return {
                'severity': severity,
                'explanation': interaction,
                'recommendation': self._get_recommendation_for_severity(severity),
                'affected_systems': self._extract_affected_systems([interaction])
            }
        else:
            return {
                'severity': 'None',
                'explanation': f'No direct interaction found between {drug_a} and {drug_b} in our database',
                'recommendation': 'No specific precautions needed based on available data',
                'affected_systems': []
            }
    
    def _find_interaction(self, drug_a, drug_b):
        """Find interaction between two drugs in the dataset"""
        print(f"Searching for interaction between: '{drug_a}' and '{drug_b}'")
        
        # First try exact matches
        interaction1 = self.interactions_df[
            (self.interactions_df['Drug 1'].str.lower() == drug_a.lower()) &
            (self.interactions_df['Drug 2'].str.lower() == drug_b.lower())
        ]
        
        interaction2 = self.interactions_df[
            (self.interactions_df['Drug 1'].str.lower() == drug_b.lower()) &
            (self.interactions_df['Drug 2'].str.lower() == drug_a.lower())
        ]
        
        # If no exact match, try partial matches
        if interaction1.empty and interaction2.empty:
            interaction1 = self.interactions_df[
                (self.interactions_df['Drug 1'].str.contains(drug_a, case=False, na=False)) &
                (self.interactions_df['Drug 2'].str.contains(drug_b, case=False, na=False))
            ]
            
            interaction2 = self.interactions_df[
                (self.interactions_df['Drug 1'].str.contains(drug_b, case=False, na=False)) &
                (self.interactions_df['Drug 2'].str.contains(drug_a, case=False, na=False))
            ]
        
        if not interaction1.empty:
            print(f"Found interaction: {interaction1.iloc[0]['Interaction Description'][:100]}...")
            return interaction1.iloc[0]['Interaction Description']
        elif not interaction2.empty:
            print(f"Found interaction: {interaction2.iloc[0]['Interaction Description'][:100]}...")
            return interaction2.iloc[0]['Interaction Description']
        else:
            print("No interaction found in database")
            return None
    
    def _determine_severity_from_description(self, description):
        """Determine interaction severity from description text"""
        description_lower = description.lower()
        
        # High severity keywords
        high_severity_keywords = [
            'contraindicated', 'avoid', 'dangerous', 'severe', 'toxic', 'fatal',
            'life-threatening', 'serious', 'major', 'significant risk'
        ]
        
        # Medium severity keywords
        medium_severity_keywords = [
            'caution', 'monitor', 'adjust', 'reduce', 'increase', 'moderate',
            'may increase', 'may decrease', 'potential', 'consider'
        ]
        
        # Low severity keywords
        low_severity_keywords = [
            'minor', 'slight', 'minimal', 'unlikely', 'rare'
        ]
        
        if any(keyword in description_lower for keyword in high_severity_keywords):
            return 'High'
        elif any(keyword in description_lower for keyword in medium_severity_keywords):
            return 'Medium'
        elif any(keyword in description_lower for keyword in low_severity_keywords):
            return 'Low'
        else:
            return 'Medium'  # Default to medium if unclear
    
    def _determine_severity_from_descriptions(self, descriptions):
        """Determine overall severity from multiple descriptions"""
        severities = [self._determine_severity_from_description(desc) for desc in descriptions]
        
        if 'High' in severities:
            return 'High'
        elif 'Medium' in severities:
            return 'Medium'
        elif 'Low' in severities:
            return 'Low'
        else:
            return 'None'
    
    def _extract_affected_systems(self, descriptions):
        """Extract affected body systems from interaction descriptions"""
        systems = set()
        
        for description in descriptions:
            desc_lower = description.lower()
            
            if any(word in desc_lower for word in ['heart', 'cardiac', 'cardiovascular']):
                systems.add('Cardiovascular')
            if any(word in desc_lower for word in ['liver', 'hepatic']):
                systems.add('Hepatic')
            if any(word in desc_lower for word in ['kidney', 'renal']):
                systems.add('Renal')
            if any(word in desc_lower for word in ['nervous', 'neurological', 'cns']):
                systems.add('Nervous System')
            if any(word in desc_lower for word in ['respiratory', 'lung']):
                systems.add('Respiratory')
            if any(word in desc_lower for word in ['gastrointestinal', 'stomach', 'digestive']):
                systems.add('Gastrointestinal')
            if any(word in desc_lower for word in ['blood', 'hematologic', 'bleeding']):
                systems.add('Hematologic')
            if any(word in desc_lower for word in ['skin', 'dermatologic', 'photosensitizing']):
                systems.add('Dermatologic')
        
        return list(systems)
    
    def _get_recommendation_for_severity(self, severity):
        """Get recommendation based on interaction severity"""
        recommendations = {
            'High': 'AVOID this combination. Consult healthcare provider immediately for alternative medications.',
            'Medium': 'Use with caution. Monitor closely for adverse effects and consider dose adjustments.',
            'Low': 'Generally safe combination. Monitor for mild side effects.',
            'None': 'No specific precautions needed based on available data.'
        }
        return recommendations.get(severity, 'Consult healthcare provider for guidance.')
    
    def _fallback_interaction_analysis(self, drug_a, drug_b):
        """Fallback analysis when CSV data is not available"""
        # Common drug interaction patterns (simplified)
        high_risk_combinations = [
            ('warfarin', 'aspirin'), ('warfarin', 'ibuprofen'),
            ('digoxin', 'furosemide'), ('lithium', 'furosemide')
        ]
        
        medium_risk_combinations = [
            ('lisinopril', 'ibuprofen'), ('metformin', 'furosemide'),
            ('atorvastatin', 'digoxin')
        ]
        
        drug_a_lower = drug_a.lower()
        drug_b_lower = drug_b.lower()
        
        # Check high risk
        for combo in high_risk_combinations:
            if (combo[0] in drug_a_lower and combo[1] in drug_b_lower) or \
               (combo[1] in drug_a_lower and combo[0] in drug_b_lower):
                return {
                    'severity': 'High',
                    'explanation': f'Known high-risk interaction between {drug_a} and {drug_b}',
                    'recommendation': 'AVOID this combination. Consult healthcare provider immediately.',
                    'affected_systems': ['Multiple Systems']
                }
        
        # Check medium risk
        for combo in medium_risk_combinations:
            if (combo[0] in drug_a_lower and combo[1] in drug_b_lower) or \
               (combo[1] in drug_a_lower and combo[0] in drug_b_lower):
                return {
                    'severity': 'Medium',
                    'explanation': f'Potential interaction between {drug_a} and {drug_b}',
                    'recommendation': 'Use with caution and monitor closely.',
                    'affected_systems': ['Cardiovascular']
                }
        
        return {
            'severity': 'None',
            'explanation': f'No known interaction between {drug_a} and {drug_b} in fallback database',
            'recommendation': 'Generally safe, but inform healthcare provider of all medications.',
            'affected_systems': []
        }
    
    def _fallback_single_drug_analysis(self, drug_name):
        """Fallback single drug analysis when CSV data is not available"""
        return {
            'severity': 'Unknown',
            'explanation': f'Drug interaction database not available. Cannot analyze {drug_name}.',
            'recommendation': 'Consult healthcare provider or pharmacist for drug interaction information.',
            'affected_systems': [],
            'interaction_count': 0
        }
    
    def get_drug_list(self):
        """Get list of available drugs in the database"""
        if self.interactions_df is None:
            return []
        
        drug1_list = self.interactions_df['Drug 1'].unique().tolist()
        drug2_list = self.interactions_df['Drug 2'].unique().tolist()
        all_drugs = list(set(drug1_list + drug2_list))
        return sorted(all_drugs)
