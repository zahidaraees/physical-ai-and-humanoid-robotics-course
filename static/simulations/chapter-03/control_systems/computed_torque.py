"""
Computed Torque Controller Implementation
Demonstrates inverse dynamics control for robot manipulators
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


class SimpleRobotModel:
    """
    Simple 2-DOF planar robot model for demonstration purposes
    """
    
    def __init__(self):
        # Robot parameters (for a simple 2-DOF planar manipulator)
        self.l1 = 1.0  # Length of first link
        self.l2 = 0.8  # Length of second link
        self.m1 = 1.0  # Mass of first link
        self.m2 = 0.8  # Mass of second link
        self.I1 = 0.1  # Inertia of first link
        self.I2 = 0.08 # Inertia of second link
        self.g = 9.81   # Gravity constant
    
    def inertia_matrix(self, q: np.ndarray) -> np.ndarray:
        """
        Calculate the inertia matrix for the robot
        
        Args:
            q: Joint positions [q1, q2]
            
        Returns:
            Inertia matrix (2x2)
        """
        q1, q2 = q[0], q[1]
        
        # Common terms
        c2 = np.cos(q2)
        s2 = np.sin(q2)
        
        # Elements of inertia matrix
        h11 = self.m1 * (self.l1/2)**2 + self.I1 + self.m2 * (self.l1**2 + (self.l2/2)**2 + 2*self.l1*(self.l2/2)*c2) + self.I2
        h12 = self.m2 * ((self.l2/2)**2 + self.l1*(self.l2/2)*c2) + self.I2
        h21 = h12
        h22 = self.m2 * (self.l2/2)**2 + self.I2
        
        H = np.array([[h11, h12],
                      [h21, h22]])
        
        return H
    
    def coriolis_matrix(self, q: np.ndarray, qd: np.ndarray) -> np.ndarray:
        """
        Calculate the Coriolis matrix for the robot
        
        Args:
            q: Joint positions [q1, q2]
            qd: Joint velocities [qd1, qd2]
            
        Returns:
            Coriolis matrix (2x2)
        """
        q1, q2 = q[0], q[1]
        qd1, qd2 = qd[0], qd[1]
        
        # Common terms
        s2 = np.sin(q2)
        
        # Elements of Coriolis matrix
        c11 = -self.m2 * self.l1 * (self.l2/2) * s2 * qd2
        c12 = -self.m2 * self.l1 * (self.l2/2) * s2 * (qd1 + qd2)
        c21 = self.m2 * self.l1 * (self.l2/2) * s2 * qd1
        c22 = 0
        
        C = np.array([[c11, c12],
                      [c21, c22]])
        
        return C
    
    def gravity_vector(self, q: np.ndarray) -> np.ndarray:
        """
        Calculate the gravity vector for the robot
        
        Args:
            q: Joint positions [q1, q2]
            
        Returns:
            Gravity vector (2x1)
        """
        q1, q2 = q[0], q[1]
        
        # Common terms
        c1 = np.cos(q1)
        c12 = np.cos(q1 + q2)
        s1 = np.sin(q1)
        s12 = np.sin(q1 + q2)
        
        g1 = self.m1 * self.g * (self.l1/2) * c1 + self.m2 * self.g * (self.l1 * c1 + (self.l2/2) * c12)
        g2 = self.m2 * self.g * (self.l2/2) * c12
        
        G = np.array([g1, g2])
        
        return G


class ComputedTorqueController:
    """
    Computed Torque Controller for robot manipulators
    Implements inverse dynamics control to linearize and decouple system dynamics
    """
    
    def __init__(self, robot_model, kp_diag: list, kd_diag: list):
        """
        Initialize computed torque controller
        
        Args:
            robot_model: Robot model with dynamics functions
            kp_diag: Diagonal elements of position gain matrix
            kd_diag: Diagonal elements of velocity gain matrix
        """
        self.robot_model = robot_model
        self.kp = np.diag(kp_diag)
        self.kd = np.diag(kd_diag)
    
    def control(self, q: np.ndarray, qd: np.ndarray, q_desired: np.ndarray, 
                qd_desired: np.ndarray, qdd_desired: np.ndarray) -> np.ndarray:
        """
        Calculate control torques using computed torque control
        
        Args:
            q: Current joint positions
            qd: Current joint velocities
            q_desired: Desired joint positions
            qd_desired: Desired joint velocities
            qdd_desired: Desired joint accelerations
            
        Returns:
            Control torques
        """
        # Calculate position and velocity errors
        q_error = q_desired - q
        qd_error = qd_desired - qd
        
        # Calculate desired acceleration with feedback
        qdd_cmd = qdd_desired + self.kp @ q_error + self.kd @ qd_error
        
        # Get robot dynamics (M, C, G terms)
        M = self.robot_model.inertia_matrix(q)
        C = self.robot_model.coriolis_matrix(q, qd)
        G = self.robot_model.gravity_vector(q)
        
        # Calculate control torques
        tau = M @ qdd_cmd + C @ qd + G
        
        return tau


def simulate_computed_torque():
    """
    Simulate computed torque control of a 2-DOF planar manipulator
    """
    robot = SimpleRobotModel()
    controller = ComputedTorqueController(robot, [100.0, 100.0], [20.0, 20.0])
    
    # Simulation parameters
    dt = 0.001
    t_max = 5.0
    t = np.arange(0, t_max, dt)
    
    # Number of joints
    n_joints = 2
    
    # Initialize state arrays
    q = np.zeros((len(t), n_joints))
    qd = np.zeros((len(t), n_joints))
    qdd = np.zeros((len(t), n_joints))
    tau = np.zeros((len(t), n_joints))
    
    # Initial conditions
    q[0, :] = [0.1, 0.1]
    qd[0, :] = [0.0, 0.0]
    
    # Trajectory parameters - circular motion in joint space
    freq = 0.5  # Hz
    amp = 0.5   # radians
    
    # Generate desired trajectory
    q_desired = np.zeros((len(t), n_joints))
    qd_desired = np.zeros((len(t), n_joints))
    qdd_desired = np.zeros((len(t), n_joints))
    
    for i in range(len(t)):
        # Desired trajectory: sinusoidal motion
        q_desired[i, 0] = amp * np.sin(2 * np.pi * freq * t[i])
        q_desired[i, 1] = amp * np.cos(2 * np.pi * freq * t[i])
        
        # First derivative (desired velocity)
        qd_desired[i, 0] = amp * 2 * np.pi * freq * np.cos(2 * np.pi * freq * t[i])
        qd_desired[i, 1] = -amp * 2 * np.pi * freq * np.sin(2 * np.pi * freq * t[i])
        
        # Second derivative (desired acceleration)
        qdd_desired[i, 0] = -amp * (2 * np.pi * freq)**2 * np.sin(2 * np.pi * freq * t[i])
        qdd_desired[i, 1] = -amp * (2 * np.pi * freq)**2 * np.cos(2 * np.pi * freq * t[i])
    
    # Simulation loop
    for i in range(1, len(t)):
        # Get current state
        q_curr = q[i-1, :]
        qd_curr = qd[i-1, :]
        
        # Get desired state
        q_des = q_desired[i, :]
        qd_des = qd_desired[i, :]
        qdd_des = qdd_desired[i, :]
        
        # Calculate control torques
        tau[i-1, :] = controller.control(q_curr, qd_curr, q_des, qd_des, qdd_des)
        
        # Update dynamics (forward Euler integration)
        # M*qdd + C*qd + G = tau  =>  qdd = M^(-1) * (tau - C*qd - G)
        M = robot.inertia_matrix(q_curr)
        C = robot.coriolis_matrix(q_curr, qd_curr)
        G = robot.gravity_vector(q_curr)
        
        qdd[i-1, :] = np.linalg.solve(M, tau[i-1, :] - C @ qd_curr - G)
        
        # Integrate to get new state
        q[i, :] = q[i-1, :] + qd_curr * dt
        qd[i, :] = qd[i-1, :] + qdd[i-1, :] * dt
    
    # Plot results
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Joint positions
    plt.subplot(2, 3, 1)
    plt.plot(t, q_desired[:, 0], 'r--', label='Desired q1', linewidth=2)
    plt.plot(t, q[:, 0], 'b-', label='Actual q1')
    plt.plot(t, q_desired[:, 1], 'g--', label='Desired q2', linewidth=2)
    plt.plot(t, q[:, 1], 'm-', label='Actual q2')
    plt.xlabel('Time (s)')
    plt.ylabel('Joint Position (rad)')
    plt.title('Computed Torque Control: Joint Positions')
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Joint velocities
    plt.subplot(2, 3, 2)
    plt.plot(t, qd_desired[:, 0], 'r--', label='Desired qd1', linewidth=2)
    plt.plot(t, qd[:, 0], 'b-', label='Actual qd1')
    plt.plot(t, qd_desired[:, 1], 'g--', label='Desired qd2', linewidth=2)
    plt.plot(t, qd[:, 1], 'm-', label='Actual qd2')
    plt.xlabel('Time (s)')
    plt.ylabel('Joint Velocity (rad/s)')
    plt.title('Computed Torque Control: Joint Velocities')
    plt.legend()
    plt.grid(True)
    
    # Plot 3: Control torques
    plt.subplot(2, 3, 3)
    plt.plot(t[:-1], tau[:, 0], 'b-', label='Tau 1')
    plt.plot(t[:-1], tau[:, 1], 'm-', label='Tau 2')
    plt.xlabel('Time (s)')
    plt.ylabel('Control Torque (Nm)')
    plt.title('Computed Torque Control: Applied Torques')
    plt.legend()
    plt.grid(True)
    
    # Plot 4: Position errors
    plt.subplot(2, 3, 4)
    pos_error_1 = q_desired[:, 0] - q[:, 0]
    pos_error_2 = q_desired[:, 1] - q[:, 1]
    plt.plot(t, pos_error_1, 'b-', label='Error q1')
    plt.plot(t, pos_error_2, 'm-', label='Error q2')
    plt.xlabel('Time (s)')
    plt.ylabel('Position Error (rad)')
    plt.title('Computed Torque Control: Position Errors')
    plt.legend()
    plt.grid(True)
    
    # Plot 5: Trajectory in joint space
    plt.subplot(2, 3, 5)
    plt.plot(q_desired[:, 0], q_desired[:, 1], 'r--', label='Desired Trajectory', linewidth=2)
    plt.plot(q[:, 0], q[:, 1], 'b-', label='Actual Trajectory')
    plt.xlabel('Joint 1 (rad)')
    plt.ylabel('Joint 2 (rad)')
    plt.title('Computed Torque Control: Joint Space Trajectory')
    plt.legend()
    plt.grid(True)
    
    # Plot 6: Control effort
    plt.subplot(2, 3, 6)
    control_effort = np.sqrt(tau[:, 0]**2 + tau[:, 1]**2)
    plt.plot(t[:-1], control_effort, 'k-', label='Control Effort')
    plt.xlabel('Time (s)')
    plt.ylabel('Control Effort (Nm)')
    plt.title('Computed Torque Control: Total Control Effort')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('static/simulations/chapter-03/control_systems/computed_torque_simulation.png', dpi=150)
    plt.show()


if __name__ == "__main__":
    simulate_computed_torque()