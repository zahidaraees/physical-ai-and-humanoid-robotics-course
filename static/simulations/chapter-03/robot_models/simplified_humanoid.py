"""
Simplified Robot Models for Control System Simulations
Used in Chapter 03 of the Physical AI and Humanoid Robotics Course
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional


class PlanarWalker:
    """
    Simplified 2D bipedal walker model for demonstrating walking control concepts
    """
    
    def __init__(self, hip_height: float = 0.8, leg_length: float = 0.9):
        """
        Initialize planar walker model
        
        Args:
            hip_height: Height of hip joint from ground at rest (m)
            leg_length: Length of leg (m)
        """
        self.hip_height = hip_height
        self.leg_length = leg_length
        
        # State: [x, z, theta, x_dot, z_dot, theta_dot] 
        # where x is forward position, z is vertical position, theta is body angle
        self.state = np.array([0.0, hip_height, 0.0, 0.0, 0.0, 0.0])
        
        # Mass parameters
        self.body_mass = 50.0  # kg
        self.leg_mass = 5.0    # kg each
        
        # Control parameters
        self.g = 9.81  # gravity constant
    
    def step_dynamics(self, dt: float, control_torques: np.ndarray = None) -> np.ndarray:
        """
        Update walker state based on dynamics
        
        Args:
            dt: Time step
            control_torques: Optional torques for hip and leg joints
            
        Returns:
            Updated state vector
        """
        x, z, theta, x_dot, z_dot, theta_dot = self.state
        
        # Simplified dynamics - in a real model this would be more complex
        # For demonstration we'll use a simplified inverted pendulum model
        
        # Calculate accelerations based on gravity and control inputs
        if control_torques is None:
            # Default walking motion - simplified
            theta_ddot = -(self.g / self.hip_height) * np.sin(theta)  # Pendulum model
        else:
            # Include control torques - simplified model
            theta_ddot = -(self.g / self.hip_height) * np.sin(theta) + control_torques[0] / (self.body_mass * self.hip_height)
        
        # Apply external forces (e.g., ground reaction forces when in contact)
        # This is a very simplified model of contact
        if z <= self.leg_length and z_dot < 0:
            # Ground contact - simplified impact model
            z_ddot = 0  # Assume perfectly rigid ground contact
            z_dot = -0.8 * z_dot  # Bounce with restitution coefficient
        else:
            # In flight - only gravity affects vertical acceleration
            z_ddot = -self.g + (control_torques[1] if control_torques is not None else 0) / self.body_mass
        
        # Forward acceleration could be influenced by control torques
        x_ddot = (control_torques[2] if control_torques is not None else 0) / self.body_mass
        
        # Update state using Euler integration
        self.state[0] += x_dot * dt  # x position
        self.state[1] += z_dot * dt  # z position
        self.state[2] += theta_dot * dt  # theta angle
        self.state[3] += x_ddot * dt  # x velocity
        self.state[4] += z_ddot * dt  # z velocity
        self.state[5] += theta_ddot * dt  # theta velocity
        
        return self.state
    
    def get_foot_positions(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        Get current positions of left and right feet based on state
        
        Returns:
            Tuple of (left_foot_pos, right_foot_pos) as (x, z) coordinates
        """
        x, z, theta, x_dot, z_dot, theta_dot = self.state
        
        # Simplified: feet positions based on body position and angle
        # In a real model, we'd have separate leg dynamics
        foot_offset_x = 0.1  # Small offset to simulate walking
        foot_offset_z = -self.leg_length  # Feet below the body
        
        left_foot_x = x - foot_offset_x * np.cos(theta)
        left_foot_z = z + foot_offset_z * np.sin(theta)
        
        right_foot_x = x + foot_offset_x * np.cos(theta)
        right_foot_z = z + foot_offset_z * np.sin(theta)
        
        return (left_foot_x, left_foot_z), (right_foot_x, right_foot_z)
    
    def is_in_support_polygon(self, zmp_pos: Tuple[float, float]) -> bool:
        """
        Check if the ZMP is within the support polygon (between feet)
        
        Args:
            zmp_pos: ZMP position as (x, z) coordinates
            
        Returns:
            True if ZMP is in support polygon, False otherwise
        """
        left_foot, right_foot = self.get_foot_positions()
        
        # For a 2D model, the support polygon is between the feet in the x direction
        min_x = min(left_foot[0], right_foot[0])
        max_x = max(left_foot[0], right_foot[0])
        
        return min_x <= zmp_pos[0] <= max_x


class ThreeDHopper:
    """
    Simplified 3D one-legged hopping robot model
    """
    
    def __init__(self, body_height: float = 0.8, leg_length: float = 0.9):
        """
        Initialize 3D hopper model
        
        Args:
            body_height: Height of body COM when leg is fully extended (m)
            leg_length: Length of leg (m)
        """
        self.body_height = body_height
        self.leg_length = leg_length
        
        # State: [x, y, z, x_dot, y_dot, z_dot]
        self.state = np.array([0.0, 0.0, body_height, 0.0, 0.0, 0.0])
        
        # Mass and inertia
        self.mass = 10.0
        self.inertia = np.eye(3) * 0.5  # Simplified inertia matrix
        
        # Control parameters
        self.g = 9.81
    
    def get_stance_dynamics(self, contact_force: np.ndarray) -> np.ndarray:
        """
        Dynamics during stance phase (when leg is in contact with ground)
        
        Args:
            contact_force: Force applied by ground contact
            
        Returns:
            State derivatives [dx, dy, dz, dvx, dvy, dvz]
        """
        x, y, z, vx, vy, vz = self.state
        
        # Accelerations due to gravity and contact force
        ax = contact_force[0] / self.mass
        ay = contact_force[1] / self.mass
        az = contact_force[2] / self.mass - self.g
        
        return np.array([vx, vy, vz, ax, ay, az])
    
    def get_flight_dynamics(self) -> np.ndarray:
        """
        Dynamics during flight phase (when not in contact with ground)
        
        Returns:
            State derivatives [dx, dy, dz, dvx, dvy, dvz]
        """
        x, y, z, vx, vy, vz = self.state
        
        # Only gravity affects motion during flight
        return np.array([vx, vy, vz, 0.0, 0.0, -self.g])
    
    def update(self, dt: float, leg_force: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Update hopper state based on dynamics
        
        Args:
            dt: Time step
            leg_force: Optional force applied by leg (in body frame)
            
        Returns:
            Updated state
        """
        if leg_force is None:
            leg_force = np.array([0.0, 0.0, 0.0])
        
        # Check if in contact with ground
        if self.state[2] <= self.leg_length and self.state[5] < 0:
            # Stance phase - in contact with ground
            state_dot = self.get_stance_dynamics(leg_force)
        else:
            # Flight phase - only gravity affects motion
            state_dot = self.get_flight_dynamics()
        
        # Update state using Euler integration
        self.state += state_dot * dt
        
        # If position goes below ground, enforce constraint
        if self.state[2] < 0:
            self.state[2] = 0  # Position on ground
            self.state[5] = 0  # Zero vertical velocity
            
        return self.state


class SimplifiedHumanoid:
    """
    Simplified model of a humanoid robot for basic control demonstrations
    """
    
    def __init__(self, n_joints: int = 12):
        """
        Initialize simplified humanoid model
        
        Args:
            n_joints: Number of joints in the model (12 for simple model)
        """
        self.n_joints = n_joints
        
        # Configuration: [left_hip, left_knee, left_ankle, 
        #                 right_hip, right_knee, right_ankle,
        #                 left_shoulder, left_elbow, 
        #                 right_shoulder, right_elbow,
        #                 torso_yaw, torso_pitch]
        self.q = np.zeros(n_joints)  # Joint positions
        self.qd = np.zeros(n_joints)  # Joint velocities
        self.qdd = np.zeros(n_joints)  # Joint accelerations
        
        # Simplified mass properties
        self.mass = 60.0  # Total mass in kg
        self.com_pos = np.array([0.0, 0.0, 0.8])  # Center of mass position
        self.com_vel = np.zeros(3)  # Center of mass velocity
        self.com_acc = np.zeros(3)  # Center of mass acceleration
        
        # Robot dimensions
        self.height = 1.7  # Total height in meters
        self.leg_length = 0.9  # Length of legs
        self.torso_height = 0.6  # Height of torso (excluding legs)
        
        # Control parameters
        self.g = 9.81
    
    def update_dynamics(self, tau: np.ndarray, dt: float) -> None:
        """
        Update robot dynamics based on applied torques (simplified)
        
        Args:
            tau: Applied joint torques
            dt: Time step
        """
        # This is a highly simplified dynamics model
        # In reality, this would involve complex multibody dynamics
        
        # Update joint accelerations (simplified - ignoring coupling)
        joint_inertia = 1.0  # Simplified average joint inertia
        self.qdd = tau / joint_inertia
        
        # Update joint velocities and positions
        self.qd += self.qdd * dt
        self.q += self.qd * dt
        
        # Update center of mass dynamics based on simplified model
        # This is a very rough approximation
        # In reality, CoM dynamics depend on all joint positions and velocities
        avg_force_x = np.sum(tau[0:6]) * 0.01  # Rough mapping from joint torques to CoM force
        avg_force_y = np.sum(tau[6:10]) * 0.01
        
        # Simplified CoM dynamics
        com_acc_x = avg_force_x / self.mass
        com_acc_y = avg_force_y / self.mass
        com_acc_z = -self.g  # Always gravity in z direction
        
        self.com_acc = np.array([com_acc_x, com_acc_y, com_acc_z])
        
        # Update CoM velocity and position
        self.com_vel += self.com_acc * dt
        self.com_pos += self.com_vel * dt
        
        # Keep CoM above ground
        if self.com_pos[2] < 0.1:  # Robot cannot go below 10cm above ground
            self.com_pos[2] = 0.1
            self.com_vel[2] = max(0, self.com_vel[2])  # Bounce if needed
    
    def compute_zmp(self) -> np.ndarray:
        """
        Compute Zero Moment Point based on current CoM state
        
        Returns:
            ZMP position [x, y] in world coordinates
        """
        x_com, y_com, z_com = self.com_pos
        x_com_dd, y_com_dd, z_com_dd = self.com_acc
        
        # ZMP formula: zmp = com - (z_height / g) * com_acc_horizontal
        zmp_x = x_com - (z_com / self.g) * x_com_dd
        zmp_y = y_com - (z_com / self.g) * y_com_dd
        
        return np.array([zmp_x, zmp_y])
    
    def is_balanced(self, support_polygon: np.ndarray) -> bool:
        """
        Check if the robot is balanced based on ZMP position
        
        Args:
            support_polygon: Vertices of the support polygon (e.g., feet positions)
            
        Returns:
            True if balanced, False otherwise
        """
        zmp = self.compute_zmp()
        
        # Simple check: is ZMP within the convex hull of support polygon
        # This is a simplified check for demonstration purposes
        min_x = np.min(support_polygon[:, 0])
        max_x = np.max(support_polygon[:, 0])
        min_y = np.min(support_polygon[:, 1])
        max_y = np.max(support_polygon[:, 1])
        
        return (min_x <= zmp[0] <= max_x) and (min_y <= zmp[1] <= max_y)


def visualize_planar_walker():
    """
    Visualize the planar walker model
    """
    walker = PlanarWalker()
    
    # Simulate a few steps of walking
    dt = 0.01
    t_max = 5.0
    t = np.arange(0, t_max, dt)
    
    # Initialize arrays to store trajectory
    x_pos = np.zeros(len(t))
    z_pos = np.zeros(len(t))
    theta_pos = np.zeros(len(t))
    
    for i in range(len(t)):
        state = walker.step_dynamics(dt)
        x_pos[i] = state[0]
        z_pos[i] = state[1]
        theta_pos[i] = state[2]
    
    # Plot the results
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(t, x_pos, label='X Position')
    plt.plot(t, z_pos, label='Z Position')
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.title('Planar Walker Position Over Time')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(x_pos, z_pos)
    plt.xlabel('X Position (m)')
    plt.ylabel('Z Position (m)')
    plt.title('Planar Walker Trajectory')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('static/simulations/chapter-03/robot_models/planar_walker_trajectory.png', dpi=150)
    plt.show()


if __name__ == "__main__":
    print("Testing simplified robot models...")
    
    # Test Planar Walker
    print("\nTesting Planar Walker model:")
    walker = PlanarWalker()
    print(f"Initial state: {walker.state}")
    
    # Test ThreeD Hopper
    print("\nTesting 3D Hopper model:")
    hopper = ThreeDHopper()
    print(f"Initial state: {hopper.state}")
    
    # Test Simplified Humanoid
    print("\nTesting Simplified Humanoid model:")
    humanoid = SimplifiedHumanoid()
    print(f"Initial CoM position: {humanoid.com_pos}")
    print(f"Initial joint positions: {humanoid.q}")
    
    # Run visualization
    print("\nGenerating visualization...")
    visualize_planar_walker()
    
    print("\nRobot model tests complete.")