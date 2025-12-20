"""
Validation script for Chapter 03 simulations
Ensures all simulation code runs correctly and produces expected results
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for validation
import matplotlib.pyplot as plt
import subprocess
import importlib.util


def validate_basic_control():
    """Validate basic control simulation"""
    print("Validating basic control simulation...")
    
    try:
        # Import the basic control module
        spec = importlib.util.spec_from_file_location(
            "basic_control", 
            "static/simulations/chapter-03/control_systems/basic_control.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Run the simulation function
        module.simulate_pid_control()
        
        # Check if the output file was created
        output_file = "static/simulations/chapter-03/control_systems/pid_simulation.png"
        if os.path.exists(output_file):
            print("✓ Basic control simulation ran successfully")
            return True
        else:
            print("✗ Basic control simulation output not found")
            return False
            
    except Exception as e:
        print(f"✗ Basic control simulation failed: {e}")
        return False


def validate_computed_torque():
    """Validate computed torque control simulation"""
    print("Validating computed torque simulation...")
    
    try:
        # Import the computed torque module
        spec = importlib.util.spec_from_file_location(
            "computed_torque", 
            "static/simulations/chapter-03/control_systems/computed_torque.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Run the simulation function
        module.simulate_computed_torque()
        
        # Check if the output file was created
        output_file = "static/simulations/chapter-03/control_systems/computed_torque_simulation.png"
        if os.path.exists(output_file):
            print("✓ Computed torque simulation ran successfully")
            return True
        else:
            print("✗ Computed torque simulation output not found")
            return False
            
    except Exception as e:
        print(f"✗ Computed torque simulation failed: {e}")
        return False


def validate_impedance_control():
    """Validate impedance control simulation"""
    print("Validating impedance control simulation...")
    
    try:
        # Import the impedance control module
        spec = importlib.util.spec_from_file_location(
            "impedance_control", 
            "static/simulations/chapter-03/control_systems/impedance_control.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Run the simulation functions
        module.simulate_impedance_control()
        module.simulate_multidof_impedance()
        
        # Check if the output files were created
        output_files = [
            "static/simulations/chapter-03/control_systems/impedance_control_simulation.png",
            "static/simulations/chapter-03/control_systems/multidof_impedance_simulation.png"
        ]
        
        all_created = all(os.path.exists(f) for f in output_files)
        if all_created:
            print("✓ Impedance control simulation ran successfully")
            return True
        else:
            print("✗ Some impedance control simulation outputs not found")
            return False
            
    except Exception as e:
        print(f"✗ Impedance control simulation failed: {e}")
        return False


def validate_zmp_control():
    """Validate ZMP control simulation"""
    print("Validating ZMP control simulation...")
    
    try:
        # Import the ZMP control module
        spec = importlib.util.spec_from_file_location(
            "zmp_control", 
            "static/simulations/chapter-03/control_systems/zmp_control.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Run the simulation functions
        module.simple_zmp_example()
        module.simulate_zmp_control()
        
        # Check if the output file was created
        output_file = "static/simulations/chapter-03/control_systems/zmp_control_simulation.png"
        if os.path.exists(output_file):
            print("✓ ZMP control simulation ran successfully")
            return True
        else:
            print("✗ ZMP control simulation output not found")
            return False
            
    except Exception as e:
        print(f"✗ ZMP control simulation failed: {e}")
        return False


def validate_robot_models():
    """Validate robot model implementations"""
    print("Validating robot model implementations...")
    
    try:
        # Import the simplified humanoid module
        spec = importlib.util.spec_from_file_location(
            "simplified_humanoid", 
            "static/simulations/chapter-03/robot_models/simplified_humanoid.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Test the robot models
        walker = module.PlanarWalker()
        hopper = module.ThreeDHopper()
        humanoid = module.SimplifiedHumanoid()
        
        # Test basic functionality
        initial_state = walker.state.copy()
        new_state = walker.step_dynamics(dt=0.01)
        
        # Check that state changed appropriately
        if not np.array_equal(initial_state, new_state):
            print("✓ Robot models are functioning correctly")
            return True
        else:
            print("✗ Robot model state did not update correctly")
            return False
            
    except Exception as e:
        print(f"✗ Robot model validation failed: {e}")
        return False


def validate_dependencies():
    """Validate that all required dependencies are available"""
    print("Validating dependencies...")
    
    required_packages = ['numpy', 'matplotlib', 'scipy']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is available")
        except ImportError:
            print(f"✗ {package} is not available")
            return False
    
    return True


def main():
    """Run all validations"""
    print("Starting validation of Chapter 03 simulations...")
    print("="*50)
    
    # Validate dependencies first
    if not validate_dependencies():
        print("\n✗ Dependency validation failed. Please install required packages.")
        return False
    
    print()
    
    # Validate each component
    results = []
    results.append(validate_basic_control())
    print()
    results.append(validate_computed_torque())
    print()
    results.append(validate_impedance_control())
    print()
    results.append(validate_zmp_control())
    print()
    results.append(validate_robot_models())
    print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("="*50)
    print(f"Validation Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All validations passed! Chapter 03 simulations are ready.")
        return True
    else:
        print("✗ Some validations failed. Please check the simulation implementations.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)