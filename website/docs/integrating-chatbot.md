---
sidebar_position: 4
---

# The Digital Twin (Gazebo & Unity)

This chapter focuses on creating digital twins of our humanoid robots using Gazebo and Unity. A digital twin is a virtual representation of a physical robot that allows us to simulate physics, gravity, collisions, and sensor data in a safe environment before deploying to the real world.

## Component Structure

Our digital twin system consists of:

1. **Gazebo Simulation Environment**: Physics simulation with realistic gravity, collisions, and contact dynamics
2. **Unity High-Fidelity Rendering**: Advanced graphics for human-robot interaction visualization
3. **Sensor Simulation**: Simulated LiDAR, depth cameras, and IMUs for perception testing
4. **Integration with Docusaurus**: Embedded documentation with interactive elements

## Creating the Digital Twin Simulation

First, let's create a Gazebo world file with our humanoid robot:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="humanoid_world">
    <!-- Include ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Include sun for lighting -->
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Define a simple room with obstacles -->
    <model name="room">
      <pose>0 0 1.5 0 0 0</pose>
      <link name="room_link">
        <visual name="room_visual">
          <geometry>
            <box>
              <size>4 4 3</size>
            </box>
          </geometry>
          <material>
            <ambient>0.5 0.5 0.5 1</ambient>
            <diffuse>0.7 0.7 0.7 1</diffuse>
          </material>
        </visual>
        <collision name="room_collision">
          <geometry>
            <box>
              <size>4 4 3</size>
            </box>
          </geometry>
        </collision>
      </link>
    </model>

    <!-- Add a simple obstacle -->
    <model name="obstacle">
      <pose>1 0 0.5 0 0 0</pose>
      <link name="obstacle_link">
        <visual name="obstacle_visual">
          <geometry>
            <box>
              <size>0.5 0.5 1</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.2 0.2 1</ambient>
            <diffuse>1 0.3 0.3 1</diffuse>
          </material>
        </visual>
        <collision name="obstacle_collision">
          <geometry>
            <box>
              <size>0.5 0.5 1</size>
            </box>
          </geometry>
        </collision>
        <self_collide>false</self_collide>
        <kinematic>false</kinematic>
      </link>
    </model>

    <!-- Our humanoid robot will be spawned here -->
    <include>
      <name>humanoid_robot</name>
      <uri>model://humanoid_robot</uri>
    </include>
  </world>
</sdf>
```

## Launching the Simulation

To launch Gazebo with our humanoid robot:

```bash
# Source ROS 2
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash

# Launch Gazebo with our custom world
ros2 launch my_simulation bringup.launch.py
```

## Sensor Simulation

The digital twin includes simulated sensors for perception:

- **LiDAR**: Simulates laser range finder for navigation and mapping
- **Depth Cameras**: Provide 3D depth information for object detection
- **IMU**: Simulates Inertial Measurement Unit for orientation and acceleration data
- **Force/Torque Sensors**: Simulate contact forces at joints

## Integrating with Docusaurus

To visualize the simulation process in our Docusaurus documentation, we can embed interactive elements:

```md
import SimulationViewer from '@site/src/components/SimulationViewer';

# The Digital Twin

In this section, we explore our simulation environment. The following viewer shows our humanoid robot in the Gazebo simulation:

<SimulationViewer />

The robot is navigating through the environment with realistic physics simulation.
```

## Unity Integration

For high-fidelity rendering and human-robot interaction, we also create a Unity simulation:

Unity provides:
- Advanced rendering capabilities
- Physics simulation with realistic materials
- Human-robot interaction scenarios
- Training environments for neural networks

The digital twin approach allows us to test and validate our Physical AI systems in a safe, controlled environment before deployment to real robots.

import ChatbotWrapper from '@site/src/components/BookChatbot';

<ChatbotWrapper />