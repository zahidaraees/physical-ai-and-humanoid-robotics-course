"""
Impedance Control Implementation
Demonstrates interaction control for physical AI systems
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


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
    
    def control(self, x: np.ndarray, xd: np.ndarray, 
                x_desired: np.ndarray, xd_desired: np.ndarray, 
                xdd_desired: np.ndarray,
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
            Control acceleration command
        """
        if f_ext is None:
            f_ext = np.zeros_like(x)
        
        # Calculate position and velocity errors
        x_error = x_desired - x
        xd_error = xd_desired - xd
        
        # Calculate desired acceleration with feedback
        # Md*xdd + Bd*xd + Kd*x = F_ext
        # xdd = Md^(-1) * (F_ext - Bd*xd_error - Kd*x_error)
        xdd_cmd = xdd_desired + np.linalg.inv(self.Md) @ (
            self.Kd @ x_error + self.Bd @ xd_error - f_ext
        )
        
        return xdd_cmd


class SimpleCartModel:
    """
    Simple 1D cart model for impedance control demonstration
    """
    
    def __init__(self, mass: float = 1.0):
        self.mass = mass
    
    def update(self, x: np.ndarray, xd: np.ndarray, 
               xdd: np.ndarray, dt: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Update the cart model with given acceleration
        
        Args:
            x: Current position
            xd: Current velocity
            xdd: Applied acceleration
            dt: Time step
            
        Returns:
            New position and velocity
        """
        # Update velocity and position using Euler integration
        new_xd = xd + xdd * dt
        new_x = x + new_xd * dt
        
        return new_x, new_xd


def simulate_impedance_control():
    """
    Simulate impedance control with a simple 1D system
    Demonstrates how the system responds to external forces
    """
    # System parameters
    dt = 0.001
    t_max = 10.0
    t = np.arange(0, t_max, dt)
    
    # Desired impedance parameters
    # For a 1D system
    Md = np.array([[1.0]])  # Desired mass
    Bd = np.array([[10.0]]) # Desired damping
    Kd = np.array([[50.0]]) # Desired stiffness
    
    # Create controller and plant model
    controller = ImpedanceController(Md, Bd, Kd)
    plant = SimpleCartModel(mass=1.0)
    
    # Initialize state arrays
    n_states = 1  # 1D system
    x = np.zeros((len(t), n_states))
    xd = np.zeros((len(t), n_states))
    xdd = np.zeros((len(t), n_states))
    
    # Initial conditions
    x[0, 0] = 0.0
    xd[0, 0] = 0.0
    
    # Create desired trajectory - a simple step
    x_desired = np.zeros((len(t), n_states))
    x_desired[:, 0] = 1.0  # Move to position 1.0
    
    # Add external force at specific times
    f_ext = np.zeros((len(t), n_states))
    # Apply external force from t=3s to t=4s
    ext_start_idx = int(3.0 / dt)
    ext_end_idx = int(4.0 / dt)
    f_ext[ext_start_idx:ext_end_idx, 0] = 5.0  # Push in positive direction
    
    # Simulation loop
    for i in range(1, len(t)):
        # Get current state
        curr_x = np.array([x[i-1, 0]])
        curr_xd = np.array([xd[i-1, 0]])
        
        # Get desired state
        curr_x_des = np.array([x_desired[i, 0]])
        curr_xd_des = np.array([0.0])  # Zero desired velocity after reaching position
        curr_xdd_des = np.array([0.0])  # Zero desired acceleration
        
        # Get external force
        curr_f_ext = np.array([f_ext[i, 0]])
        
        # Calculate control command using impedance control
        xdd_cmd = controller.control(curr_x, curr_xd, 
                                    curr_x_des, curr_xd_des, 
                                    curr_xdd_des, curr_f_ext)
        
        # Apply the control command to the plant
        x[i, 0], xd[i, 0] = plant.update(x[i-1, 0], xd[i-1, 0], xdd_cmd[0], dt)
        
        # Store the commanded acceleration
        xdd[i-1, 0] = xdd_cmd[0]
    
    # Plot results
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Position
    plt.subplot(2, 3, 1)
    plt.plot(t, x_desired[:, 0], 'r--', label='Desired Position', linewidth=2)
    plt.plot(t, x[:, 0], 'b-', label='Actual Position')
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.title('Impedance Control: Position Response')
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Velocity
    plt.subplot(2, 3, 2)
    plt.plot(t, xd[:, 0], 'b-', label='Actual Velocity')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Impedance Control: Velocity Response')
    plt.legend()
    plt.grid(True)
    
    # Plot 3: Applied acceleration
    plt.subplot(2, 3, 3)
    plt.plot(t[:-1], xdd[:, 0], 'g-', label='Applied Acceleration')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s^2)')
    plt.title('Impedance Control: Applied Acceleration')
    plt.legend()
    plt.grid(True)
    
    # Plot 4: External force
    plt.subplot(2, 3, 4)
    plt.plot(t, f_ext[:, 0], 'r-', label='External Force')
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Applied External Force')
    plt.legend()
    plt.grid(True)
    
    # Plot 5: Position error
    plt.subplot(2, 3, 5)
    pos_error = x_desired[:, 0] - x[:, 0]
    plt.plot(t, pos_error, 'm-', label='Position Error')
    plt.xlabel('Time (s)')
    plt.ylabel('Position Error (m)')
    plt.title('Impedance Control: Position Error')
    plt.legend()
    plt.grid(True)
    
    # Plot 6: Phase plot
    plt.subplot(2, 3, 6)
    plt.plot(x[:, 0], xd[:, 0], 'b-', label='Phase Trajectory')
    plt.xlabel('Position (m)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Impedance Control: Phase Plot')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('static/simulations/chapter-03/control_systems/impedance_control_simulation.png', dpi=150)
    plt.show()


# Advanced impedance control example with multiple DOF
def simulate_multidof_impedance():
    """
    Simulate multi-DOF impedance control
    """
    # System parameters
    dt = 0.001
    t_max = 10.0
    t = np.arange(0, t_max, dt)
    
    # Desired impedance parameters for 2-DOF system
    Md = np.array([[2.0, 0.0],
                   [0.0, 1.5]])  # Desired mass matrix
    
    Bd = np.array([[15.0, 0.0],
                   [0.0, 12.0]])  # Desired damping matrix
    
    Kd = np.array([[80.0, 0.0],
                   [0.0, 60.0]])  # Desired stiffness matrix
    
    # Create controller
    controller = ImpedanceController(Md, Bd, Kd)
    
    # Initialize state arrays (2 DOF system)
    n_dof = 2
    x = np.zeros((len(t), n_dof))
    xd = np.zeros((len(t), n_dof))
    
    # Initial conditions
    x[0, :] = [0.1, 0.05]
    xd[0, :] = [0.0, 0.0]
    
    # Create desired trajectory - circular motion
    radius = 0.5
    freq = 0.2  # Hz
    x_desired = np.zeros((len(t), n_dof))
    x_desired[:, 0] = radius * np.cos(2 * np.pi * freq * t)
    x_desired[:, 1] = radius * np.sin(2 * np.pi * freq * t)
    
    # Zero desired velocity and acceleration
    xd_desired = np.zeros((len(t), n_dof))
    xdd_desired = np.zeros((len(t), n_dof))
    
    # Add external force that varies over time
    f_ext = np.zeros((len(t), n_dof))
    # Apply periodic external force
    f_ext[:, 0] = 0.5 * np.sin(2 * np.pi * 0.5 * t)
    f_ext[:, 1] = 0.3 * np.cos(2 * np.pi * 0.3 * t)
    
    # Simulation loop
    for i in range(1, len(t)):
        # Get current state
        curr_x = x[i-1, :]
        curr_xd = xd[i-1, :]
        
        # Get desired state
        curr_x_des = x_desired[i, :]
        curr_xd_des = xd_desired[i, :]
        curr_xdd_des = xdd_desired[i, :]
        
        # Get external force
        curr_f_ext = f_ext[i, :]
        
        # Calculate control command using impedance control
        xdd_cmd = controller.control(curr_x, curr_xd, 
                                    curr_x_des, curr_xd_des, 
                                    curr_xdd_des, curr_f_ext)
        
        # Simple integration for 2-DOF system
        # In a real system, we'd have more complex dynamics
        xd[i, :] = curr_xd + xdd_cmd * dt
        x[i, :] = curr_x + xd[i, :] * dt
    
    # Plot results
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Trajectory in 2D space
    plt.subplot(2, 3, 1)
    plt.plot(x_desired[:, 0], x_desired[:, 1], 'r--', label='Desired Trajectory', linewidth=2)
    plt.plot(x[:, 0], x[:, 1], 'b-', label='Actual Trajectory')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.title('Multi-DOF Impedance Control: Trajectory')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    
    # Plot 2: X position vs time
    plt.subplot(2, 3, 2)
    plt.plot(t, x_desired[:, 0], 'r--', label='Desired X', linewidth=2)
    plt.plot(t, x[:, 0], 'b-', label='Actual X')
    plt.xlabel('Time (s)')
    plt.ylabel('X Position (m)')
    plt.title('Multi-DOF Impedance Control: X Position')
    plt.legend()
    plt.grid(True)
    
    # Plot 3: Y position vs time
    plt.subplot(2, 3, 3)
    plt.plot(t, x_desired[:, 1], 'r--', label='Desired Y', linewidth=2)
    plt.plot(t, x[:, 1], 'b-', label='Actual Y')
    plt.xlabel('Time (s)')
    plt.ylabel('Y Position (m)')
    plt.title('Multi-DOF Impedance Control: Y Position')
    plt.legend()
    plt.grid(True)
    
    # Plot 4: External force
    plt.subplot(2, 3, 4)
    plt.plot(t, f_ext[:, 0], 'r-', label='F_ext X')
    plt.plot(t, f_ext[:, 1], 'g-', label='F_ext Y')
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Multi-DOF: External Forces')
    plt.legend()
    plt.grid(True)
    
    # Plot 5: Position errors
    plt.subplot(2, 3, 5)
    plt.plot(t, x_desired[:, 0] - x[:, 0], 'r-', label='Error X')
    plt.plot(t, x_desired[:, 1] - x[:, 1], 'b-', label='Error Y')
    plt.xlabel('Time (s)')
    plt.ylabel('Position Error (m)')
    plt.title('Multi-DOF: Position Errors')
    plt.legend()
    plt.grid(True)
    
    # Plot 6: Velocity
    plt.subplot(2, 3, 6)
    plt.plot(t, xd[:, 0], 'r-', label='Velocity X')
    plt.plot(t, xd[:, 1], 'b-', label='Velocity Y')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Multi-DOF: Velocities')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('static/simulations/chapter-03/control_systems/multidof_impedance_simulation.png', dpi=150)
    plt.show()


if __name__ == "__main__":
    print("Simulating basic impedance control...")
    simulate_impedance_control()
    
    print("Simulating multi-DOF impedance control...")
    simulate_multidof_impedance()
    
    print("Simulations complete. Check the output images in static/simulations/chapter-03/control_systems/")