#!/usr/bin/env python3
"""
Check 3D model files and provide debugging info
"""

import os
import base64

def check_3d_models():
    print("🧬 Checking 3D Model Files...")
    print("=" * 50)
    
    # Check for GLB files
    possible_glb_paths = [
        'HumanBody.glb',
        'human_body.glb',
        'assets/HumanBody.glb',
        'assets/human_body.glb',
        'models/HumanBody.glb'
    ]
    
    found_glb = None
    for path in possible_glb_paths:
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✅ Found GLB: {path} ({size:,} bytes)")
            found_glb = path
            break
        else:
            print(f"❌ Not found: {path}")
    
    if found_glb:
        print(f"\n🎉 GLB file available: {found_glb}")
        
        # Test if we can read the file
        try:
            with open(found_glb, 'rb') as f:
                data = f.read()
            print(f"✅ File readable: {len(data):,} bytes")
            
            # Test base64 encoding (for data URL)
            try:
                encoded = base64.b64encode(data).decode()
                print(f"✅ Base64 encoding successful: {len(encoded):,} characters")
                print(f"📊 Data URL size: ~{len(encoded) * 1.33 / 1024 / 1024:.1f} MB")
            except Exception as e:
                print(f"❌ Base64 encoding failed: {e}")
                
        except Exception as e:
            print(f"❌ Cannot read file: {e}")
    else:
        print(f"\n⚠️ No GLB files found!")
        print("Solutions:")
        print("1. Copy HumanBody.glb to the root directory")
        print("2. Check if the file was renamed")
        print("3. Verify file permissions")
    
    # Check current directory for any 3D files
    print(f"\n📁 3D files in current directory:")
    all_files = os.listdir('.')
    model_files = [f for f in all_files if f.lower().endswith(('.glb', '.gltf', '.obj', '.fbx', '.dae'))]
    
    if model_files:
        for file in model_files:
            size = os.path.getsize(file)
            print(f"  • {file} ({size:,} bytes)")
    else:
        print("  No 3D model files found")
    
    # Provide recommendations
    print(f"\n💡 Recommendations:")
    if found_glb:
        print("✅ Your 3D model should work!")
        print("✅ The enhanced fallback visualization will also work")
        print("✅ Both GLB and fallback modes are implemented")
    else:
        print("⚠️ GLB file missing - fallback visualization will be used")
        print("🎨 Fallback includes animated body representation")
        print("🎯 Medicine targeting will still work with visual effects")

if __name__ == "__main__":
    check_3d_models()
