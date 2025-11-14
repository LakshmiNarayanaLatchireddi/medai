#!/usr/bin/env python3
"""
Test script to show available drugs from the dataset
"""

import pandas as pd
import os

def test_drug_loading():
    print("🧪 Testing Drug Dataset Loading...")
    print("=" * 50)
    
    # Try to load the CSV file
    possible_paths = [
        'db_drug_interactions.csv',
        'data/drug_interactions.csv', 
        'drug_interactions.csv'
    ]
    
    df = None
    for csv_path in possible_paths:
        if os.path.exists(csv_path):
            print(f"✅ Found CSV file: {csv_path}")
            try:
                df = pd.read_csv(csv_path)
                print(f"✅ Loaded {len(df)} interactions")
                break
            except Exception as e:
                print(f"❌ Error loading {csv_path}: {e}")
    
    if df is None:
        print("❌ No CSV file found!")
        return
    
    # Extract unique drugs
    print("\n📊 Extracting unique drugs...")
    drug1_list = df['Drug 1'].dropna().unique().tolist()
    drug2_list = df['Drug 2'].dropna().unique().tolist()
    all_drugs = sorted(list(set(drug1_list + drug2_list)))
    
    print(f"✅ Found {len(all_drugs)} unique drugs")
    
    # Show sample drugs
    print("\n💊 Sample Drugs (first 50):")
    print("-" * 30)
    for i, drug in enumerate(all_drugs[:50]):
        print(f"{i+1:2d}. {drug}")
    
    # Show some common drugs
    common_drugs = [
        "Aspirin", "Ibuprofen", "Acetaminophen", "Lisinopril", "Metformin",
        "Atorvastatin", "Amlodipine", "Omeprazole", "Levothyroxine", "Warfarin"
    ]
    
    print(f"\n🔍 Checking for common drugs in dataset:")
    print("-" * 40)
    for drug in common_drugs:
        if drug in all_drugs:
            print(f"✅ {drug} - FOUND")
        else:
            print(f"❌ {drug} - NOT FOUND")
    
    # Test some interactions
    print(f"\n🧬 Sample Interactions:")
    print("-" * 25)
    sample_interactions = df.head(10)
    for _, row in sample_interactions.iterrows():
        print(f"• {row['Drug 1']} + {row['Drug 2']}")
        print(f"  → {row['Interaction Description'][:80]}...")
        print()

if __name__ == "__main__":
    test_drug_loading()
