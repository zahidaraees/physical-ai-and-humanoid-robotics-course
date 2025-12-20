# Chapter 03: Control Systems and Motion Planning - Simulations

This directory contains the Python simulations that serve as the reproducibility checkpoint for Chapter 03 of the Physical AI and Humanoid Robotics Course. These simulations demonstrate key concepts in control systems and motion planning for humanoid robots.

## Contents

- `control_systems/`: Implementations of various control algorithms
  - `basic_control.py`: PID controller implementation
  - `computed_torque.py`: Computed torque control for robot manipulators
  - `impedance_control.py`: Impedance control for interaction tasks
  - `zmp_control.py`: Zero Moment Point control for bipedal locomotion

- `robot_models/`: Simplified robot models for simulation
  - `planar_walker.py`: 2D walking model
  - `3d_hopper.py`: 3D hopping robot model
  - `simplified_humanoid.py`: Simple humanoid model

- `visualization/`: Visualization utilities
  - `plot_utils.py`: Plotting utilities for simulation results
  - `animation.py`: Animation utilities for robot motion

- `logs/`: Simulation logs and output data
  - `simulation_logs/`: Detailed logs from simulation runs

- `notebooks/`: Jupyter notebooks with tutorials
  - `tutorial_1_basic_control.ipynb`: Basic control concepts
  - `tutorial_2_zmp_control.ipynb`: ZMP-based walking control
  - `tutorial_3_mpc_control.ipynb`: Model predictive control concepts

## Requirements

To run these simulations, you'll need Python 3.11+ with the following packages:
- NumPy
- SciPy
- Matplotlib
- Jupyter
- CasADi (for optimization-based control)

Install all requirements using:
```bash
pip install -r requirements.txt
```

## Running Simulations

Each Python file can be run independently to see specific control examples:

1. `python control_systems/basic_control.py` - Demonstrates PID control
2. `python control_systems/computed_torque.py` - Shows computed torque control
3. `python control_systems/impedance_control.py` - Demonstrates impedance control
4. `python control_systems/zmp_control.py` - Shows ZMP-based balance control

## Reproducibility

Each simulation generates plots and saves them in the `control_systems/` directory. These plots can be compared with the examples shown in Chapter 03 to validate the concepts.

The simulation code is thoroughly documented with explanations of the control theory concepts and their implementation.

## Notebooks

For a more interactive learning experience, check out the Jupyter notebooks in the `notebooks/` directory. These provide step-by-step tutorials with explanations of the underlying mathematics and control theory.

## Validation

The `validate_simulations.py` script runs all simulations and checks that the results are within expected parameters, ensuring the reproducibility of the chapter content.