"""
Validation script for Chapter 06 HRI endpoints
Ensures all API components are properly structured and documented
"""
import os
import sys
from pathlib import Path


def validate_api_structure():
    """Validate API structure and components"""
    print("Validating API structure...")
    
    api_dirs = [
        "static/hri-endpoints/chapter-06/api/endpoints",
        "static/hri-endpoints/chapter-06/api/models", 
        "static/hri-endpoints/chapter-06/api/services"
    ]
    
    for api_dir in api_dirs:
        if os.path.exists(api_dir):
            print(f"✓ {api_dir} exists")
        else:
            print(f"✗ {api_dir} missing")
            return False
    
    # Check specific endpoint files
    endpoint_files = [
        "static/hri-endpoints/chapter-06/api/endpoints/speech.py",
        "static/hri-endpoints/chapter-06/api/endpoints/gestures.py",
        "static/hri-endpoints/chapter-06/api/endpoints/emotions.py",
        "static/hri-endpoints/chapter-06/api/endpoints/multimodal.py"
    ]
    
    for file in endpoint_files:
        if os.path.exists(file):
            print(f"✓ {os.path.basename(file)} exists")
        else:
            print(f"✗ {os.path.basename(file)} missing")
            return False
    
    # Check specific model files
    model_files = [
        "static/hri-endpoints/chapter-06/api/models/hri_requests.py",
        "static/hri-endpoints/chapter-06/api/models/hri_responses.py",
        "static/hri-endpoints/chapter-06/api/models/interaction_models.py"
    ]
    
    for file in model_files:
        if os.path.exists(file):
            print(f"✓ {os.path.basename(file)} exists")
        else:
            print(f"✗ {os.path.basename(file)} missing")
            return False
    
    # Check specific service files
    service_files = [
        "static/hri-endpoints/chapter-06/api/services/speech_recognition.py",
        "static/hri-endpoints/chapter-06/api/services/emotion_analysis.py",
        "static/hri-endpoints/chapter-06/api/services/interaction_manager.py"
    ]
    
    for file in service_files:
        if os.path.exists(file):
            print(f"✓ {os.path.basename(file)} exists")
        else:
            print(f"✗ {os.path.basename(file)} missing")
            return False
    
    print("✓ All API components exist")
    return True


def validate_docs():
    """Validate documentation files"""
    print("Validating documentation...")
    
    doc_files = [
        "static/hri-endpoints/chapter-06/docs/api_spec.yaml",
        "static/hri-endpoints/chapter-06/docs/api_spec.json",
        "static/hri-endpoints/chapter-06/docs/user_guide.md"
    ]
    
    for doc_file in doc_files:
        if os.path.exists(doc_file):
            print(f"✓ {os.path.basename(doc_file)} exists")
        else:
            print(f"✗ {os.path.basename(doc_file)} missing")
            return False
    
    print("✓ All documentation files exist")
    return True


def validate_tests():
    """Validate test files"""
    print("Validating test files...")
    
    test_files = [
        "static/hri-endpoints/chapter-06/tests/test_speech.py",
        "static/hri-endpoints/chapter-06/tests/test_gestures.py",
        "static/hri-endpoints/chapter-06/tests/test_emotions.py",
        "static/hri-endpoints/chapter-06/tests/integration_tests.py"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"✓ {os.path.basename(test_file)} exists")
        else:
            print(f"✗ {os.path.basename(test_file)} missing")
            return False
    
    print("✓ All test files exist")
    return True


def validate_configs():
    """Validate configuration files"""
    print("Validating configuration files...")
    
    config_files = [
        "static/hri-endpoints/chapter-06/config/settings.py"
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✓ {os.path.basename(config_file)} exists")
        else:
            print(f"✗ {os.path.basename(config_file)} missing")
            return False
    
    print("✓ All configuration files exist")
    return True


def validate_notebooks():
    """Validate tutorial notebooks"""
    print("Validating tutorial notebooks...")
    
    required_notebooks = [
        "static/hri-endpoints/chapter-06/notebooks/tutorial_1_speech_interactions.ipynb",
        "static/hri-endpoints/chapter-06/notebooks/tutorial_2_emotion_recognition.ipynb",
        "static/hri-endpoints/chapter-06/notebooks/tutorial_3_multimodal_interaction.ipynb"
    ]
    
    for notebook in required_notebooks:
        if os.path.exists(notebook):
            print(f"✓ {os.path.basename(notebook)} exists")
        else:
            print(f"✗ {os.path.basename(notebook)} missing")
            return False
    
    print("✓ All required notebooks exist")
    return True


def validate_core_files():
    """Validate core files"""
    print("Validating core files...")
    
    core_files = [
        "static/hri-endpoints/chapter-06/README.md",
        "static/hri-endpoints/chapter-06/requirements.txt",
        "static/hri-endpoints/chapter-06/run_server.py"
    ]
    
    # Check all except run_server.py which might not exist yet
    for file in core_files[:-1]:  # Skip run_server.py for now
        if os.path.exists(file):
            print(f"✓ {os.path.basename(file)} exists")
        else:
            print(f"✗ {os.path.basename(file)} missing")
            return False
    
    # Special check for run_server.py
    if os.path.exists("static/hri-endpoints/chapter-06/run_server.py"):
        print("✓ run_server.py exists")
    else:
        print("? run_server.py not found (not required for basic validation)")
    
    print("✓ All required core files exist")
    return True


def main():
    """Run all validations"""
    print("Starting validation of Chapter 06 HRI endpoints...")
    print("="*60)
    
    results = []
    results.append(validate_api_structure())
    print()
    results.append(validate_docs())
    print()
    results.append(validate_tests())
    print()
    results.append(validate_configs())
    print()
    results.append(validate_notebooks())
    print()
    results.append(validate_core_files())
    print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("="*60)
    print(f"Validation Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All validations passed! Chapter 06 HRI endpoints structure is complete.")
        return True
    else:
        print("✗ Some validations failed. Please check the HRI endpoints structure.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)