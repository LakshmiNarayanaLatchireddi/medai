#!/usr/bin/env python3
"""
Quick script to extract a sample drug list from your dataset
"""

import pandas as pd

# Load your drug dataset
try:
    df = pd.read_csv('db_drug_interactions.csv')
    
    # Get unique drugs
    drug1_list = df['Drug 1'].dropna().unique().tolist()
    drug2_list = df['Drug 2'].dropna().unique().tolist()
    all_drugs = sorted(list(set(drug1_list + drug2_list)))
    
    # Filter for common/recognizable drug names (shorter names, likely real drugs)
    common_drugs = []
    for drug in all_drugs:
        if len(drug) < 25 and not any(char in drug for char in ['(', ')', '[', ']']):
            common_drugs.append(drug)
    
    print("Sample of 100 common drugs from your dataset:")
    print("=" * 50)
    
    for i, drug in enumerate(common_drugs[:100]):
        print(f'"{drug}",')
    
    print(f"\nTotal drugs available: {len(all_drugs)}")
    print(f"Filtered common drugs: {len(common_drugs)}")
    
except Exception as e:
    print(f"Error: {e}")
    print("Make sure db_drug_interactions.csv is in the current directory")
