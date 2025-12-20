"""
ZMP (Zero Moment Point) Control Implementation
Demonstrates balance control for bipedal locomotion in humanoid robots
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


class ZMPController:
    """
    Zero Moment Point (ZMP) Controller for bipedal locomotion
    Keeps the ZMP within the support polygon for dynamic balance
    """
    
    def __init__(self, com_height: float, dt: float = 0.01):
        """
        Initialize ZMP controller
        
        Args:
            com_height: Height of center of mass above ground (m)
            dt: Time step for control updates
        """
        self.com_height = com_height
        self.dt = dt
        self.g = 9.81  # Gravity constant
        
        # For storing state
        self.com_pos = np.array([0.0, 0.0])  # x, y position of CoM
        self.com_vel = np.array([0.0, 0.0])  # x, y velocity of CoM
        self.com_acc = np.array([0.0, 0.0])  # x, y acceleration of CoM
        
    def compute_zmp(self, com_pos: np.ndarray, com_acc: np.ndarray) -> np.ndarray:
        """
        Compute Zero Moment Point from CoM position and acceleration
        
        Args:
            com_pos: Center of mass position [x, y]
            com_acc: Center of mass acceleration [x, y]
            
        Returns:
            ZMP position [x, y]
        """
        zmp = com_pos - (self.com_height / self.g) * com_acc
        return zmp
    
    def compute_com_trajectory(self, zmp_desired: np.ndarray, 
                               t_step: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute CoM trajectory to achieve desired ZMP using the inverted pendulum model
        
        Args:
            zmp_desired: Desired ZMP position [x, y]
            t_step: Time for this step
            
        Returns:
            Tuple of (new_com_pos, new_com_vel, new_com_acc)
        """
        # Using the inverted pendulum model: zmp = com - (h/g) * com_ddot
        # So: com_ddot = (g/h) * (com - zmp)
        
        # Calculate required CoM acceleration to achieve desired ZMP
        com_acc = (self.g / self.com_height) * (self.com_pos - zmp_desired)
        
        # Update velocity and position using integration
        new_com_vel = self.com_vel + com_acc * self.dt
        new_com_pos = self.com_pos + new_com_vel * self.dt
        
        return new_com_pos, new_com_vel, com_acc


class SimpleWalkingPatternGenerator:
    """
    Simple walking pattern generator that creates ZMP reference trajectories
    """
    
    def __init__(self, step_length: float = 0.3, step_width: float = 0.2, 
                 step_height: float = 0.1, step_period: float = 1.0):
        """
        Initialize walking pattern generator
        
        Args:
            step_length: Forward step length (m)
            step_width: Lateral distance between feet (m)
            step_height: Maximum foot lift height (m)
            step_period: Time for each step (s)
        """
        self.step_length = step_length
        self.step_width = step_width
        self.step_height = step_height
        self.step_period = step_period
        self.dt = 0.01  # Simulation time step
    
    def generate_zmp_trajectory(self, n_steps: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate ZMP reference trajectory for n steps
        
        Args:
            n_steps: Number of steps to generate
            
        Returns:
            Tuple of (zmp_x, zmp_y, time) arrays
        """
        # Calculate number of time steps
        n_time_steps = int(n_steps * self.step_period / self.dt)
        
        # Initialize arrays
        t = np.arange(0, n_steps * self.step_period, self.dt)
        zmp_x = np.zeros(n_time_steps)
        zmp_y = np.zeros(n_time_steps)
        
        # Generate ZMP trajectory for walking
        # ZMP should be under the supporting foot during single support phase
        for i in range(n_steps):
            # Time range for this step
            start_idx = int(i * self.step_period / self.dt)
            end_idx = int((i + 1) * self.step_period / self.dt)
            
            # Set ZMP to be under the supporting foot
            # For simplicity, alternating between left and right foot
            foot_y = self.step_width / 2 if i % 2 == 0 else -self.step_width / 2
            foot_x = i * self.step_length
            
            # During double support phase at the beginning and end of each step
            # We can smooth the transition between ZMP positions
            ds_duration = 0.2 * self.step_period  # 20% of step period for double support
            ds_start = int(start_idx + (ds_duration / 2) / self.dt)
            ds_end = int(start_idx + ds_duration / self.dt)
            
            # Single support phase
            for j in range(start_idx, end_idx):
                if j < ds_start or j >= end_idx - ds_duration / self.dt:
                    # Single support - ZMP under supporting foot
                    zmp_x[j] = foot_x + self.step_length / 2  # Midpoint of step
                    zmp_y[j] = foot_y
                else:
                    # Double support - smooth transition between feet
                    # Simplified transition for this example
                    zmp_x[j] = foot_x + self.step_length / 2
                    if i > 0:
                        prev_foot_y = self.step_width / 2 if (i-1) % 2 == 0 else -self.step_width / 2
                        alpha = (j - ds_start) / (ds_end - ds_start)
                        zmp_y[j] = prev_foot_y * (1 - alpha) + foot_y * alpha
                    else:
                        zmp_y[j] = foot_y
        
        return zmp_x[:len(t)], zmp_y[:len(t)], t


def simulate_zmp_control():
    """
    Simulate ZMP-based balance control for humanoid walking
    """
    # Initialize ZMP controller
    zmp_controller = ZMPController(com_height=0.8, dt=0.01)  # 80cm CoM height
    
    # Initialize walking pattern generator
    walker = SimpleWalkingPatternGenerator(step_length=0.3, step_width=0.2, step_period=1.0)
    
    # Generate ZMP reference for 5 steps
    zmp_ref_x, zmp_ref_y, t = walker.generate_zmp_trajectory(5)
    
    # Initialize state arrays
    n_steps = len(t)
    com_x = np.zeros(n_steps)
    com_y = np.zeros(n_steps)
    com_x_vel = np.zeros(n_steps)
    com_y_vel = np.zeros(n_steps)
    com_x_acc = np.zeros(n_steps)
    com_y_acc = np.zeros(n_steps)
    actual_zmp_x = np.zeros(n_steps)
    actual_zmp_y = np.zeros(n_steps)
    
    # Set initial conditions
    zmp_controller.com_pos = np.array([0.0, 0.0])
    zmp_controller.com_vel = np.array([0.0, 0.0])
    com_x[0] = 0.0
    com_y[0] = 0.0
    com_x_vel[0] = 0.0
    com_y_vel[0] = 0.0
    
    # Simulation loop
    for i in range(1, n_steps):
        # Current desired ZMP
        zmp_desired = np.array([zmp_ref_x[i-1], zmp_ref_y[i-1]])
        
        # Compute CoM trajectory to achieve desired ZMP
        new_com_pos, new_com_vel, com_acc = zmp_controller.compute_com_trajectory(
            zmp_desired, t[i] - t[i-1])
        
        # Update controller state
        zmp_controller.com_pos = new_com_pos
        zmp_controller.com_vel = new_com_vel
        zmp_controller.com_acc = com_acc
        
        # Store results
        com_x[i] = new_com_pos[0]
        com_y[i] = new_com_pos[1]
        com_x_vel[i] = new_com_vel[0]
        com_y_vel[i] = new_com_vel[1]
        com_x_acc[i-1] = com_acc[0]
        com_y_acc[i-1] = com_acc[1]
        
        # Compute actual ZMP from achieved CoM state
        actual_zmp = zmp_controller.compute_zmp(new_com_pos, com_acc)
        actual_zmp_x[i-1] = actual_zmp[0]
        actual_zmp_y[i-1] = actual_zmp[1]
    
    # Plot results
    plt.figure(figsize=(18, 12))
    
    # Plot 1: ZMP trajectory (X)
    plt.subplot(3, 3, 1)
    plt.plot(t, zmp_ref_x, 'r--', label='Desired ZMP X', linewidth=2)
    plt.plot(t[:-1], actual_zmp_x[:-1], 'b-', label='Actual ZMP X')
    plt.xlabel('Time (s)')
    plt.ylabel('ZMP X (m)')
    plt.title('ZMP Control: X Direction')
    plt.legend()
    plt.grid(True)
    
    # Plot 2: ZMP trajectory (Y)
    plt.subplot(3, 3, 2)
    plt.plot(t, zmp_ref_y, 'r--', label='Desired ZMP Y', linewidth=2)
    plt.plot(t[:-1], actual_zmp_y[:-1], 'b-', label='Actual ZMP Y')
    plt.xlabel('Time (s)')
    plt.ylabel('ZMP Y (m)')
    plt.title('ZMP Control: Y Direction')
    plt.legend()
    plt.grid(True)
    
    # Plot 3: CoM trajectory (X)
    plt.subplot(3, 3, 3)
    plt.plot(t, com_x, 'b-', label='CoM X')
    plt.xlabel('Time (s)')
    plt.ylabel('CoM X (m)')
    plt.title('Center of Mass: X Direction')
    plt.legend()
    plt.grid(True)
    
    # Plot 4: CoM trajectory (Y)
    plt.subplot(3, 3, 4)
    plt.plot(t, com_y, 'b-', label='CoM Y')
    plt.xlabel('Time (s)')
    plt.ylabel('CoM Y (m)')
    plt.title('Center of Mass: Y Direction')
    plt.legend()
    plt.grid(True)
    
    # Plot 5: Phase portrait (X)
    plt.subplot(3, 3, 5)
    plt.plot(com_x, com_x_vel, 'b-', label='CoM X Phase Portrait')
    plt.xlabel('CoM Position X (m)')
    plt.ylabel('CoM Velocity X (m/s)')
    plt.title('CoM Phase Portrait: X Direction')
    plt.legend()
    plt.grid(True)
    
    # Plot 6: Phase portrait (Y)
    plt.subplot(3, 3, 6)
    plt.plot(com_y, com_y_vel, 'b-', label='CoM Y Phase Portrait')
    plt.xlabel('CoM Position Y (m)')
    plt.ylabel('CoM Velocity Y (m/s)')
    plt.title('CoM Phase Portrait: Y Direction')
    plt.legend()
    plt.grid(True)
    
    # Plot 7: CoM trajectory in 2D space
    plt.subplot(3, 3, 7)
    plt.plot(com_x, com_y, 'b-', label='CoM 2D Trajectory')
    plt.plot(actual_zmp_x[::10], actual_zmp_y[::10], 'ro', markersize=3, label='Actual ZMP')
    plt.plot(zmp_ref_x[::10], zmp_ref_y[::10], 'gs', markersize=3, label='Desired ZMP')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.title('CoM and ZMP Trajectories in 2D')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    
    # Plot 8: CoM acceleration
    plt.subplot(3, 3, 8)
    plt.plot(t[:-1], com_x_acc, 'r-', label='CoM Acc X')
    plt.plot(t[:-1], com_y_acc, 'b-', label='CoM Acc Y')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s^2)')
    plt.title('CoM Acceleration')
    plt.legend()
    plt.grid(True)
    
    # Plot 9: ZMP error
    plt.subplot(3, 3, 9)
    zmp_error_x = zmp_ref_x - actual_zmp_x
    zmp_error_y = zmp_ref_y - actual_zmp_y
    plt.plot(t[:-1], zmp_error_x[:-1], 'r-', label='ZMP Error X')
    plt.plot(t[:-1], zmp_error_y[:-1], 'b-', label='ZMP Error Y')
    plt.xlabel('Time (s)')
    plt.ylabel('ZMP Error (m)')
    plt.title('ZMP Tracking Error')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('static/simulations/chapter-03/control_systems/zmp_control_simulation.png', dpi=150)
    plt.show()


def simple_zmp_example():
    """
    Simple example showing ZMP calculation and basic control
    """
    print("Simple ZMP Example:")
    print("Calculating ZMP for a stationary robot...")
    
    # Robot parameters
    com_height = 0.8  # 80 cm CoM height
    com_pos = np.array([0.0, 0.0])  # CoM at origin
    com_acc = np.array([0.1, -0.05])  # Small acceleration
    
    # Calculate ZMP
    g = 9.81
    zmp = com_pos - (com_height / g) * com_acc
    
    print(f"CoM position: {com_pos}")
    print(f"CoM acceleration: {com_acc}")
    print(f"Calculated ZMP: {zmp}")
    
    # Show how ZMP changes with CoM acceleration
    print("\nEffect of CoM acceleration on ZMP:")
    test_accels = [
        np.array([0.0, 0.0]),    # No acceleration
        np.array([0.2, 0.0]),    # Forward acceleration
        np.array([-0.2, 0.0]),   # Backward acceleration
        np.array([0.0, 0.1]),    # Lateral acceleration
    ]
    
    for i, acc in enumerate(test_accels):
        zmp_new = com_pos - (com_height / g) * acc
        print(f"Acceleration {acc} -> ZMP: {zmp_new}")


if __name__ == "__main__":
    # Run simple example
    simple_zmp_example()
    
    # Run full simulation
    print("\nRunning full ZMP control simulation...")
    simulate_zmp_control()
    
    print("Simulation complete. Check the output images in static/simulations/chapter-03/control_systems/")