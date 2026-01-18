#!/usr/bin/env python3
"""
Quick test script to verify all components work correctly.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from audio.capture import AudioCapture
        print("✓ AudioCapture imported successfully")
    except Exception as e:
        print(f"✗ AudioCapture import failed: {e}")
        return False
    
    try:
        from audio.processor import AudioProcessor
        print("✓ AudioProcessor imported successfully")
    except Exception as e:
        print(f"✗ AudioProcessor import failed: {e}")
        return False
    
    try:
        from translation.translator import Translator
        print("✓ Translator imported successfully")
    except Exception as e:
        print(f"✗ Translator import failed: {e}")
        return False
    
    try:
        from ui.caption_window import CaptionWindow
        print("✓ CaptionWindow imported successfully")
    except Exception as e:
        print(f"✗ CaptionWindow import failed: {e}")
        return False
    
    try:
        from ui.settings_dialog import SettingsDialog
        print("✓ SettingsDialog imported successfully")
    except Exception as e:
        print(f"✗ SettingsDialog import failed: {e}")
        return False
    
    try:
        from utils.config import Config
        print("✓ Config imported successfully")
    except Exception as e:
        print(f"✗ Config import failed: {e}")
        return False
    
    return True


def test_dependencies():
    """Test that all required dependencies are installed."""
    print("\nTesting dependencies...")
    
    dependencies = [
        'PyQt5',
        'pyaudio',
        'speech_recognition',
        'googletrans',
        'numpy'
    ]
    
    all_ok = True
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep} installed")
        except ImportError:
            print(f"✗ {dep} NOT installed")
            all_ok = False
    
    return all_ok


def test_audio_devices():
    """Test audio device detection."""
    print("\nTesting audio devices...")
    
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        
        print(f"Found {p.get_device_count()} audio devices:")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"  [{i}] {info['name']} (Input channels: {info['maxInputChannels']})")
        
        p.terminate()
        return True
    except Exception as e:
        print(f"✗ Error testing audio devices: {e}")
        return False


def test_translation():
    """Test translation functionality."""
    print("\nTesting translation...")
    
    try:
        from translation.translator import Translator
        translator = Translator(source_lang='en', target_lang='es')
        
        result = translator.translate("Hello, world!")
        print(f"  Test translation: 'Hello, world!' → '{result}'")
        
        if result:
            print("✓ Translation working")
            return True
        else:
            print("✗ Translation returned empty result")
            return False
    except Exception as e:
        print(f"✗ Translation test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("LiveTranslationCaption - Component Test")
    print("="*60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Dependencies", test_dependencies()))
    results.append(("Audio Devices", test_audio_devices()))
    results.append(("Translation", test_translation()))
    
    print("\n" + "="*60)
    print("Test Results:")
    print("="*60)
    
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("✓ All tests passed! The application should work correctly.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        print("\nTo install missing dependencies, run:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
