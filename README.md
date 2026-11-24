
# Terrain-Aided UAV Localization

**GNSS-Denied UAV Localization Using Camera-LiDAR Sensor Fusion**

## Overview

This project develops a terrain-aided localization system for an
Unmanned Aerial Vehicle (UAV) operating without GNSS availability.

The system combines visual information, LiDAR measurements and
Inertial Measurement Unit (IMU) data to estimate the UAV pose
within a previously known terrain map.

An Extended Kalman Filter (EKF) is used to fuse the independent
sensor estimations.

The project also explores 3D environment reconstruction using
3D Gaussian Splatting.

## Objectives

- Develop a simulated UAV environment using ROS 2 and Gazebo.
- Implement camera-based terrain localization.
- Implement LiDAR-based terrain localization.
- Integrate IMU measurements.
- Develop sensor fusion using an Extended Kalman Filter.
- Evaluate localization accuracy against simulation ground truth.
- Reconstruct the observed environment using 3D Gaussian Splatting.

## System Architecture

The system is organized into independent ROS 2 packages:

| Package | Description |
|---|---|
| terrain_navigation_sim | UAV and environment simulation |
| terrain_navigation_sensors | Sensor interfaces and synchronization |
| terrain_navigation_visual | Visual localization |
| terrain_navigation_lidar | LiDAR localization |
| terrain_navigation_estimation | EKF sensor fusion |
| terrain_navigation_evaluation | Ground truth and performance evaluation |
| terrain_navigation_reconstruction | 3D reconstruction |
| terrain_navigation_bringup | System integration and launch files |

## Technology Stack

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo
- Python
- C++
- OpenCV
- Point Cloud Library (PCL)
- Extended Kalman Filter
- 3D Gaussian Splatting

## Repository Structure

```text
terrain_navigation_ws/
├── src/
├── config/
├── maps/
├── data/
├── results/
├── docs/
├── rviz/
├── scripts/
└── tools/
```

## Installation

Source ROS 2 Humble:

```bash
source /opt/ros/humble/setup.bash
```

Install dependencies:

```bash
rosdep install --from-paths src --ignore-src -r -y
```

Build the workspace:

```bash
colcon build --symlink-install
```

Source the workspace:

```bash
source install/setup.bash
```

## Gazebo simulation

With the ROS 2 workspace sourced, launch Gazebo and the Aerostack2 flight stack:

```bash
ros2 launch terrain_navigation_sim simulation.launch.py teleop:=false
```

To open the keyboard teleoperation window alongside Gazebo:

```bash
ros2 launch terrain_navigation_sim simulation.launch.py teleop:=true
```

Teleoperation defaults to off. Pass `gui:=false` to run the Gazebo server
without its client.

## Status

Project structure initialized.
Algorithm development and system integration pending.

## Authors

Project developed as part of the Master's Degree in
Electronics, Robotics and Automation.
