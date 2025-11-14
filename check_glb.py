#!/usr/bin/env python3
"""
Check if GLB file exists and provide alternatives
"""

import os

def check_glb_files():
    print("🔍 Checking for GLB files...")
    print("=" * 40)
    
    possible_paths = [
        'HumanBody.glb',
        'human_body.glb',
        'assets/human_body.glb',
        'assets/HumanBody.glb'
    ]
    
    found_files = []
    for path in possible_paths:
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✅ Found: {path} ({size:,} bytes)")
            found_files.append(path)
        else:
            print(f"❌ Not found: {path}")
    
    if found_files:
        print(f"\n🎉 GLB files available: {len(found_files)}")
        print("Your 3D viewer should work!")
    else:
        print("\n⚠️ No GLB files found!")
        print("Solutions:")
        print("1. Make sure HumanBody.glb is in the root directory")
        print("2. Check if the file was renamed")
        print("3. The system will show a placeholder if GLB is missing")
    
    # Check current directory contents
    print(f"\n📁 Current directory contents:")
    files = [f for f in os.listdir('.') if f.lower().endswith(('.glb', '.gltf'))]
    if files:
        for file in files:
            print(f"  • {file}")
    else:
        print("  No 3D model files found")

if __name__ == "__main__":
    check_glb_files()
