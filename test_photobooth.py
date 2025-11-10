#!/usr/bin/env python
"""
Test script for Raspberry Pi Photo Booth

This script allows testing the photo booth functionality
without requiring actual Pi hardware.
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

def test_config_loading():
    """Test configuration file loading"""
    print("Testing configuration loading...")
    try:
        # Import after adding path
        from camera import CONFIG, TOTAL_PICS, PHOTO_W, PHOTO_H
        print(f"✓ Configuration loaded successfully")
        print(f"  - Total pics: {TOTAL_PICS}")
        print(f"  - Photo resolution: {PHOTO_W}x{PHOTO_H}")
        return True
    except Exception as e:
        print(f"✗ Configuration loading failed: {e}")
        return False

def test_folder_creation():
    """Test folder creation functionality"""
    print("\nTesting folder creation...")
    try:
        from camera import health_test_required_folders
        result = health_test_required_folders()
        if result:
            print("✓ Folder creation test passed")
        else:
            print("✗ Folder creation test failed")
        return result
    except Exception as e:
        print(f"✗ Folder creation test error: {e}")
        return False

def test_asset_files():
    """Test presence of required asset files"""
    print("\nTesting asset files...")
    required_assets = [
        'assets/intro_1.png',
        'assets/intro_2.png',
        'assets/processing.png',
        'assets/all_done_delayed_upload.png'
    ]
    
    missing_assets = []
    for asset in required_assets:
        if not os.path.exists(asset):
            missing_assets.append(asset)
    
    if not missing_assets:
        print("✓ All required asset files found")
        return True
    else:
        print("✗ Missing asset files:")
        for asset in missing_assets:
            print(f"    {asset}")
        return False

def test_photo_processor_imports():
    """Test photo processor imports"""
    print("\nTesting photo processor imports...")
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("photo_processor", "photo-processor.py")
        if spec is not None and spec.loader is not None:
            photo_processor = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(photo_processor)
            print("✓ Photo processor imports successful")
            return True
        else:
            print("✗ Could not load photo processor module")
            return False
    except Exception as e:
        print(f"✗ Photo processor import failed: {e}")
        return False

def run_simulation_mode():
    """Run camera in simulation mode"""
    print("\nRunning simulation mode...")
    print("This will test the camera code with TESTMODE_AUTOPRESS_BUTTON enabled")
    
    # Create a temporary config with test mode enabled
    import yaml
    from shutil import copy2
    
    # Backup original config if it exists
    if os.path.exists('camera-config.yaml'):
        copy2('camera-config.yaml', 'camera-config.yaml.backup')
    
    # Load and modify config
    with open('camera-config.example.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    config['TESTMODE_AUTOPRESS_BUTTON'] = True
    config['TOTAL_PICS'] = 2  # Reduce for faster testing
    
    with open('camera-config.yaml', 'w') as f:
        yaml.dump(config, f)
    
    try:
        print("Starting camera simulation...")
        import camera
        camera.main()
        print("✓ Simulation completed successfully")
        return True
    except Exception as e:
        print(f"✗ Simulation failed: {e}")
        return False
    finally:
        # Restore original config if backup exists
        if os.path.exists('camera-config.yaml.backup'):
            copy2('camera-config.yaml.backup', 'camera-config.yaml')
            os.remove('camera-config.yaml.backup')

def main():
    """Run all tests"""
    print("Raspberry Pi Photo Booth Test Suite")
    print("=" * 40)
    
    tests = [
        ("Configuration Loading", test_config_loading),
        ("Folder Creation", test_folder_creation),
        ("Asset Files", test_asset_files),
        ("Photo Processor Imports", test_photo_processor_imports),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All basic tests passed!")
        
        # Ask user if they want to run simulation
        try:
            response = input("\nRun camera simulation? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                run_simulation_mode()
        except KeyboardInterrupt:
            print("\nTest interrupted by user.")
    else:
        print(f"\n✗ {total - passed} tests failed. Please fix these issues before running the photo booth.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())