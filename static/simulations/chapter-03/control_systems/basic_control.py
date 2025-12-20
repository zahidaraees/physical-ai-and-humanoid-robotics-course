"""
Basic Control Systems for Humanoid Robotics
Implementation of fundamental control algorithms discussed in Chapter 03
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List


class PIDController:
    """
    Proportional-Integral-Derivative Controller
    A fundamental control algorithm used in many robotic systems
    """
    
    def __init__(self, kp: float, ki: float, kd: float, dt: float = 0.01):
        """
        Initialize PID controller
        
        Args:
            kp: Proportional gain
            ki: Integral gain
            kd: Derivative gain
            dt: Time step for integration
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        
        # Internal state for integral and derivative terms
        self.integral = 0.0
        self.previous_error = 0.0
    
    def update(self, error: float) -> float:
        """
        Update the PID controller with current error
        
        Args:
            error: Current error (desired - actual)
            
        Returns:
            Control output
        """
        # Proportional term
        p_term = self.kp * error
        
        # Integral term
        self.integral += error * self.dt
        i_term = self.ki * self.integral
        
        # Derivative term
        derivative = (error - self.previous_error) / self.dt
        d_term = self.kd * derivative
        
        # Store current error for next derivative calculation
        self.previous_error = error
        
        # Calculate output
        output = p_term + i_term + d_term
        return output


class ComputedTorqueController:
    """
    Computed Torque Controller for robot manipulators
    Implements inverse dynamics control to linearize and decouple system dynamics
    """
    
    def __init__(self, robot_model, kp_diag: List[float], kd_diag: List[float]):
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


class ImpedanceController:
    """
    Impedance Controller
    Creates desired dynamic relationship between robot and environment
    """
    
    def __init__(self, Md: np.ndarray, Bd: np.ndarray, Kd: np.ndarray):
        """
        Initialize impedance controller
        
        Args:
            Md: Desired mass matrix
            Bd: Desired damping matrix
            Kd: Desired stiffness matrix
        """
        self.Md = Md
        self.Bd = Bd
        self.Kd = Kd
    
    def control(self, x: np.ndarray, xd: np.ndarray, x_desired: np.ndarray,
                xd_desired: np.ndarray, xdd_desired: np.ndarray,
                f_ext: np.ndarray = None) -> np.ndarray:
        """
        Calculate control force using impedance control
        
        Args:
            x: Current position
            xd: Current velocity
            x_desired: Desired position
            xd_desired: Desired velocity
            xdd_desired: Desired acceleration
            f_ext: External forces (optional)
            
        Returns:
            Control force
        """
        if f_ext is None:
            f_ext = np.zeros_like(x)
        
        # Calculate position and velocity errors
        x_error = x_desired - x
        xd_error = xd_desired - xd
        
        # Calculate desired acceleration with feedback
        xdd_cmd = xdd_desired + np.linalg.inv(self.Md) @ (
            self.Kd @ x_error + self.Bd @ xd_error - f_ext
        )
        
        return xdd_cmd


def simulate_pid_control():
    """
    Simulate PID control of a simple system
    Demonstrates basic PID control principles
    """
    # System parameters (simulating a simple mass)
    mass = 1.0
    dt = 0.01
    t_max = 10.0
    
    # PID parameters
    kp = 10.0
    ki = 1.0
    kd = 5.0
    
    pid = PIDController(kp, ki, kd, dt)
    
    # Simulation variables
    t = np.arange(0, t_max, dt)
    position = np.zeros_like(t)
    velocity = np.zeros_like(t)
    desired_position = np.ones_like(t) * 1.0  # Step response
    control_output = np.zeros_like(t)
    error = np.zeros_like(t)
    
    # Set initial conditions
    position[0] = 0.0
    velocity[0] = 0.0
    
    # Simulation loop
    for i in range(1, len(t)):
        # Calculate error
        error[i] = desired_position[i-1] - position[i-1]
        
        # Get control output
        control_output[i-1] = pid.update(error[i])
        
        # Apply control to system (simple mass dynamics)
        acceleration = control_output[i-1] / mass
        
        # Update state (Euler integration)
        velocity[i] = velocity[i-1] + acceleration * dt
        position[i] = position[i-1] + velocity[i] * dt
    
    # Plot results
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(t, desired_position, 'r--', label='Desired Position')
    plt.plot(t, position, 'b-', label='Actual Position')
    plt.xlabel('Time (s)')
    plt.ylabel('Position')
    plt.title('PID Control: Position Response')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 2, 2)
    plt.plot(t, control_output)
    plt.xlabel('Time (s)')
    plt.ylabel('Control Output')
    plt.title('PID Control: Control Signal')
    plt.grid(True)
    
    plt.subplot(2, 2, 3)
    plt.plot(t, error)
    plt.xlabel('Time (s)')
    plt.ylabel('Error')
    plt.title('PID Control: Error Response')
    plt.grid(True)
    
    plt.subplot(2, 2, 4)
    plt.plot(t, velocity)
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity')
    plt.title('PID Control: Velocity Response')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('static/simulations/chapter-03/control_systems/pid_simulation.png', dpi=150)
    plt.show()


if __name__ == "__main__":
    simulate_pid_control()