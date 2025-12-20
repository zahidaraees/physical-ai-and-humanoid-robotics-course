# Chapter 05: Learning and Adaptation - Training Scripts

This repository contains the training scripts that serve as the reproducibility checkpoint for Chapter 05 of the Physical AI and Humanoid Robotics Course. These scripts demonstrate key learning algorithms and their application to humanoid robotics problems.

## Contents

- `environments/`: Simulated environments for training and evaluation
  - `humanoid_control/`: Environments for humanoid control tasks
  - `manipulation_tasks/`: Environments for manipulation learning
  - `locomotion_envs/`: Environments for locomotion learning

- `algorithms/`: Implementation of key learning algorithms
  - `reinforcement_learning/`: RL algorithms for humanoid tasks
    - `model_free/`: Model-free RL methods (PPO, DDPG, SAC, etc.)
    - `model_based/`: Model-based RL methods
    - `safe_rl/`: Safe RL implementations
  - `imitation_learning/`: Imitation learning implementations
  - `adaptive_control/`: Adaptive control implementations

- `configs/`: Configuration files for experiments
  - `rl_configs/`: Configurations for reinforcement learning
  - `il_configs/`: Configurations for imitation learning
  - `ac_configs/`: Configurations for adaptive control

- `notebooks/`: Jupyter notebooks with tutorials
  - `tutorial_1_rl_basics.ipynb`: Introduction to RL in Physical AI
  - `tutorial_2_imitation_learning.ipynb`: Imitation learning for robots
  - `tutorial_3_adaptive_systems.ipynb`: Adaptive systems in robotics

- `experiments/`: Pre-configured experiments for benchmarking
- `results/`: Directory for storing and analyzing results

## Getting Started

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run a basic reinforcement learning example:
```bash
python algorithms/reinforcement_learning/model_free/ppo_example.py
```

3. Try the tutorials in the `notebooks/` directory to understand the implementations.

## Reproducibility

Each script reproduces algorithms and results discussed in Chapter 05. The implementations are designed to be:
- Reproducible: Same results across multiple runs with fixed seeds
- Efficient: Optimized for sample efficiency in physical AI contexts
- Safe: Incorporates safety constraints for physical systems

## Validation

Run the validation script to ensure all components work correctly:
```bash
python run_experiments.py --validate
```

## Experiment Tracking

Results are automatically logged using Weights & Biases. To enable tracking:
```bash
wandb login
```

## Code Quality

All implementations follow:
- Clean, well-documented code
- Standard RL library interfaces
- Efficient PyTorch implementations
- Comprehensive error handling