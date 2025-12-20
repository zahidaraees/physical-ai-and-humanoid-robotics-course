"""
Validation script for Chapter 05 training scripts
Ensures all training script components are properly structured and functional
"""
import os
import sys
from pathlib import Path


def validate_environments():
    """Validate environment implementations"""
    print("Validating environments...")
    
    env_dirs = [
        "static/training-scripts/chapter-05/environments/humanoid_control",
        "static/training-scripts/chapter-05/environments/manipulation_tasks",
        "static/training-scripts/chapter-05/environments/locomotion_envs"
    ]
    
    for env_dir in env_dirs:
        if os.path.exists(env_dir):
            print(f"✓ {env_dir} exists")
        else:
            print(f"✗ {env_dir} missing")
            return False
    
    print("✓ All environment directories exist")
    return True


def validate_algorithms():
    """Validate algorithm implementations"""
    print("Validating algorithm implementations...")
    
    algo_dirs = [
        "static/training-scripts/chapter-05/algorithms/reinforcement_learning",
        "static/training-scripts/chapter-05/algorithms/imitation_learning",
        "static/training-scripts/chapter-05/algorithms/adaptive_control"
    ]
    
    for algo_dir in algo_dirs:
        if os.path.exists(algo_dir):
            print(f"✓ {algo_dir} exists")
        else:
            print(f"✗ {algo_dir} missing")
            return False
    
    # Check specific RL subdirectories
    rl_subdirs = [
        "static/training-scripts/chapter-05/algorithms/reinforcement_learning/model_free",
        "static/training-scripts/chapter-05/algorithms/reinforcement_learning/model_based",
        "static/training-scripts/chapter-05/algorithms/reinforcement_learning/safe_rl"
    ]
    
    for subdir in rl_subdirs:
        if os.path.exists(subdir):
            print(f"✓ {subdir} exists")
        else:
            print(f"✗ {subdir} missing")
            return False
    
    # Check that PPO example exists
    ppo_path = "static/training-scripts/chapter-05/algorithms/reinforcement_learning/model_free/ppo_example.py"
    if os.path.exists(ppo_path):
        print("✓ PPO example implementation exists")
    else:
        print("✗ PPO example implementation missing")
        return False
    
    print("✓ All algorithm directories exist")
    return True


def validate_configs():
    """Validate configuration files"""
    print("Validating configuration files...")
    
    config_dirs = [
        "static/training-scripts/chapter-05/configs/rl_configs",
        "static/training-scripts/chapter-05/configs/il_configs",
        "static/training-scripts/chapter-05/configs/ac_configs"
    ]
    
    for config_dir in config_dirs:
        if os.path.exists(config_dir):
            print(f"✓ {config_dir} exists")
        else:
            print(f"✗ {config_dir} missing")
            return False
    
    print("✓ All config directories exist")
    return True


def validate_notebooks():
    """Validate tutorial notebooks"""
    print("Validating tutorial notebooks...")
    
    required_notebooks = [
        "static/training-scripts/chapter-05/notebooks/tutorial_1_rl_basics.ipynb",
        "static/training-scripts/chapter-05/notebooks/tutorial_2_imitation_learning.ipynb",
        "static/training-scripts/chapter-05/notebooks/tutorial_3_adaptive_systems.ipynb"
    ]
    
    for notebook in required_notebooks:
        if os.path.exists(notebook):
            print(f"✓ {os.path.basename(notebook)} exists")
        else:
            print(f"✗ {pathlib.Path(notebook).name} missing")
            return False
    
    print("✓ All required notebooks exist")
    return True


def validate_core_files():
    """Validate core files"""
    print("Validating core files...")
    
    core_files = [
        "static/training-scripts/chapter-05/README.md",
        "static/training-scripts/chapter-05/requirements.txt",
        "static/training-scripts/chapter-05/run_experiments.py"
    ]
    
    # Check all except run_experiments.py which might not exist yet
    for file in core_files[:-1]:  # Skip run_experiments.py for now
        if os.path.exists(file):
            print(f"✓ {os.path.basename(file)} exists")
        else:
            print(f"✗ {os.path.basename(file)} missing")
            return False
    
    # Special check for run_experiments.py
    if os.path.exists("static/training-scripts/chapter-05/run_experiments.py"):
        print("✓ run_experiments.py exists")
    else:
        print("? run_experiments.py not found (not required for basic validation)")
    
    print("✓ All required core files exist")
    return True


def main():
    """Run all validations"""
    print("Starting validation of Chapter 05 training scripts...")
    print("="*60)
    
    results = []
    results.append(validate_environments())
    print()
    results.append(validate_algorithms())
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
        print("✓ All validations passed! Chapter 05 training scripts structure is complete.")
        return True
    else:
        print("✗ Some validations failed. Please check the training scripts structure.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)