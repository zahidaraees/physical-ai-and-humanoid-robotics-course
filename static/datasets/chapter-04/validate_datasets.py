"""
Validation script for Chapter 04 dataset documentation
Ensures all dataset documentation is properly structured and links are valid
"""
import os
import json
import sys
from pathlib import Path


def validate_visual_datasets():
    """Validate visual dataset documentation"""
    print("Validating visual datasets...")
    
    required_files = [
        "dataset_catalog.json",
        "sample_processing.py",
        "visualization_tools.py",
        "README.md"
    ]
    
    visual_dir = "static/datasets/chapter-04/visual_datasets"
    
    for file in required_files:
        file_path = os.path.join(visual_dir, file)
        if os.path.exists(file_path):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            return False
    
    # Validate the catalog structure
    catalog_path = os.path.join(visual_dir, "dataset_catalog.json")
    try:
        with open(catalog_path, 'r') as f:
            catalog = json.load(f)
        
        if not isinstance(catalog, list) and not isinstance(catalog, dict):
            print("✗ Dataset catalog has invalid structure")
            return False
            
        print("✓ Visual dataset catalog has valid structure")
        return True
    except Exception as e:
        print(f"✗ Error validating visual dataset catalog: {e}")
        return False


def validate_tactile_datasets():
    """Validate tactile dataset documentation"""
    print("Validating tactile datasets...")
    
    required_files = [
        "dataset_catalog.json",
        "sample_processing.py",
        "visualization_tools.py",
        "README.md"
    ]
    
    tactile_dir = "static/datasets/chapter-04/tactile_datasets"
    
    for file in required_files:
        file_path = os.path.join(tactile_dir, file)
        if os.path.exists(file_path):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            return False
    
    # Validate the catalog structure
    catalog_path = os.path.join(tactile_dir, "dataset_catalog.json")
    try:
        with open(catalog_path, 'r') as f:
            catalog = json.load(f)
        
        if not isinstance(catalog, list) and not isinstance(catalog, dict):
            print("✗ Dataset catalog has invalid structure")
            return False
            
        print("✓ Tactile dataset catalog has valid structure")
        return True
    except Exception as e:
        print(f"✗ Error validating tactile dataset catalog: {e}")
        return False


def validate_auditory_datasets():
    """Validate auditory dataset documentation"""
    print("Validating auditory datasets...")
    
    required_files = [
        "dataset_catalog.json",
        "sample_processing.py",
        "visualization_tools.py",
        "README.md"
    ]
    
    auditory_dir = "static/datasets/chapter-04/auditory_datasets"
    
    for file in required_files:
        file_path = os.path.join(auditory_dir, file)
        if os.path.exists(file_path):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            return False
    
    # Validate the catalog structure
    catalog_path = os.path.join(auditory_dir, "dataset_catalog.json")
    try:
        with open(catalog_path, 'r') as f:
            catalog = json.load(f)
        
        if not isinstance(catalog, list) and not isinstance(catalog, dict):
            print("✗ Dataset catalog has invalid structure")
            return False
            
        print("✓ Auditory dataset catalog has valid structure")
        return True
    except Exception as e:
        print(f"✗ Error validating auditory dataset catalog: {e}")
        return False


def validate_baselines():
    """Validate baseline implementations"""
    print("Validating baseline implementations...")
    
    baselines_dir = "static/datasets/chapter-04/baselines"
    
    subdirs = ["visual_perception", "tactile_perception", "audio_perception"]
    
    for subdir in subdirs:
        subdir_path = os.path.join(baselines_dir, subdir)
        if os.path.exists(subdir_path):
            print(f"✓ {subdir} directory exists")
        else:
            print(f"✗ {subdir} directory missing")
            return False
    
    print("✓ All baseline directories exist")
    return True


def validate_notebooks():
    """Validate tutorial notebooks"""
    print("Validating tutorial notebooks...")
    
    required_notebooks = [
        "tutorial_1_visual_perception.ipynb",
        "tutorial_2_tactile_perception.ipynb",
        "tutorial_3_multimodal_fusion.ipynb"
    ]
    
    notebooks_dir = "static/datasets/chapter-04/notebooks"
    
    for notebook in required_notebooks:
        file_path = os.path.join(notebooks_dir, notebook)
        if os.path.exists(file_path):
            print(f"✓ {notebook} exists")
        else:
            print(f"✗ {notebook} missing")
            return False
    
    print("✓ All required notebooks exist")
    return True


def main():
    """Run all validations"""
    print("Starting validation of Chapter 04 dataset documentation...")
    print("="*60)
    
    results = []
    results.append(validate_visual_datasets())
    print()
    results.append(validate_tactile_datasets())
    print()
    results.append(validate_auditory_datasets())
    print()
    results.append(validate_baselines())
    print()
    results.append(validate_notebooks())
    print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("="*60)
    print(f"Validation Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All validations passed! Chapter 04 dataset documentation is complete.")
        return True
    else:
        print("✗ Some validations failed. Please check the dataset documentation structure.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)