#!/usr/bin/env python3
"""
Test script to check what drugs are available in the system
"""

import pandas as pd
import os

def test_drug_availability():
    print("🔍 Testing Drug Availability...")
    print("=" * 50)
    
    # Load CSV file
    possible_paths = [
        'db_drug_interactions.csv',
        'data/drug_interactions.csv', 
        'drug_interactions.csv'
    ]
    
    df = None
    for csv_path in possible_paths:
        if os.path.exists(csv_path):
            print(f"✅ Loading from: {csv_path}")
            df = pd.read_csv(csv_path)
            break
    
    if df is None:
        print("❌ No CSV file found!")
        return
    
    # Extract all unique drugs
    drug1_list = df['Drug 1'].dropna().unique().tolist()
    drug2_list = df['Drug 2'].dropna().unique().tolist()
    all_drugs = sorted(list(set(drug1_list + drug2_list)))
    
    print(f"📊 Total unique drugs in database: {len(all_drugs)}")
    
    # Test specific drugs you're looking for
    test_drugs = [
        "Insulin", "insulin", "INSULIN",
        "Advil", "advil", "ADVIL", 
        "Ibuprofen", "ibuprofen",
        "Tylenol", "tylenol", "Acetaminophen",
        "Aspirin", "aspirin",
        "Metformin", "metformin"
    ]
    
    print(f"\n🧪 Testing specific drugs:")
    print("-" * 30)
    
    found_drugs = []
    for test_drug in test_drugs:
        matches = [drug for drug in all_drugs if test_drug.lower() in drug.lower()]
        if matches:
            print(f"✅ '{test_drug}' → Found {len(matches)} matches:")
            for match in matches[:5]:  # Show first 5 matches
                print(f"    • {match}")
                found_drugs.append(match)
            if len(matches) > 5:
                print(f"    ... and {len(matches) - 5} more")
        else:
            print(f"❌ '{test_drug}' → No matches found")
    
    # Show sample of available drugs
    print(f"\n📋 Sample of available drugs (first 50):")
    print("-" * 40)
    for i, drug in enumerate(all_drugs[:50]):
        print(f"{i+1:2d}. {drug}")
    
    # Look for common drug patterns
    print(f"\n🔍 Searching for common drug patterns:")
    print("-" * 40)
    
    patterns = ['insulin', 'aspirin', 'ibuprofen', 'acetaminophen', 'metformin', 'lisinopril']
    for pattern in patterns:
        matches = [drug for drug in all_drugs if pattern.lower() in drug.lower()]
        print(f"'{pattern}': {len(matches)} matches")
        if matches:
            print(f"  Examples: {', '.join(matches[:3])}")
    
    return all_drugs

if __name__ == "__main__":
    drugs = test_drug_availability()
    
    if drugs:
        print(f"\n🎯 Summary:")
        print(f"  • Total drugs available: {len(drugs)}")
        print(f"  • Database is loaded successfully")
        print(f"  • Search should work for partial matches")
    else:
        print(f"\n❌ No drugs loaded - check CSV file path")
