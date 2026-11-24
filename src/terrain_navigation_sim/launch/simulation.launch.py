"""Launch the Aerostack2 Gazebo simulation and optional keyboard control."""

import os
from pathlib import Path
import sys

from ament_index_python.packages import get_package_prefix, get_package_share_path
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument, ExecuteProcess, GroupAction, IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
import yaml


PACKAGE = 'terrain_navigation_sim'


def include_launch(package, filename, **arguments):
    """Isolate launch arguments for each component and drone."""
    path = get_package_share_path(package) / 'launch' / filename
    return GroupAction(actions=[
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(path)),
            launch_arguments=arguments.items(),
        ),
    ])


def launch_simulation(context, config_dir):
    """Create the simulator and the flight stack for each drone in the world."""
    world = Path(LaunchConfiguration('world').perform(context)).expanduser().resolve()
    with world.open(encoding='utf-8') as stream:
        namespaces = [drone['model_name'] for drone in yaml.safe_load(stream)['drones']]

    humble = os.environ.get('ROS_DISTRO') == 'humble'
    actions = [
        include_launch(
            'as2_gazebo_assets', 'launch_simulation.py',
            simulation_config_file=str(world), use_sim_time='true', headless='true',
        ),
    ]
    if LaunchConfiguration('gui').perform(context) == 'true':
        fortress = humble or os.environ.get('GZ_VERSION', '').lower() == 'fortress'
        actions.append(ExecuteProcess(
            cmd=['ign', 'gazebo', '-g'] if fortress else ['gz', 'sim', '-g'],
            output='screen',
        ))

    for namespace in namespaces:
        drone = {'namespace': namespace, 'use_sim_time': 'true'}
        config = dict(drone, config_file=str(config_dir / 'config.yaml'))
        estimator = dict(config)
        if humble:
            estimator['plugin_config_file'] = str(config_dir / 'ground_truth_fortress.yaml')
        controller_file = (
            'pid_speed_controller_humble.yaml' if humble else 'pid_speed_controller.yaml'
        )
        actions.extend([
            include_launch(
                'as2_platform_gazebo', 'platform_gazebo_launch.py', **drone,
                platform_config_file=config['config_file'], simulation_config_file=str(world),
            ),
            include_launch('as2_state_estimator', 'state_estimator_launch.py', **estimator),
            include_launch(
                'as2_motion_controller', 'controller_launch.py', **config,
                plugin_name='pid_speed_controller',
                plugin_config_file=str(config_dir / controller_file),
            ),
            include_launch('as2_behaviors_motion', 'motion_behaviors_launch.py', **config),
            include_launch(
                'as2_behaviors_trajectory_generation',
                'generate_polynomial_trajectory_behavior_launch.py', **config,
            ),
        ])

    if LaunchConfiguration('teleop').perform(context) == 'true':
        namespace_list = ','.join(namespaces)
        if humble:
            executable = Path(get_package_prefix(PACKAGE)) / 'lib' / PACKAGE
            actions.append(ExecuteProcess(
                cmd=[sys.executable, str(executable / 'keyboard_teleoperation.py'), namespace_list],
                output='screen',
            ))
        else:
            actions.append(include_launch(
                'as2_keyboard_teleoperation', 'as2_keyboard_teleoperation_launch.py',
                namespace=namespace_list, use_sim_time='true',
            ))
    return actions


def generate_launch_description():
    """Declare the ROS 2 launch arguments."""
    config_dir = get_package_share_path(PACKAGE) / 'config'
    return LaunchDescription([
        DeclareLaunchArgument(
            'teleop', default_value='false', choices=['true', 'false'],
            description='Open the keyboard teleoperation window.',
        ),
        DeclareLaunchArgument(
            'gui', default_value='true', choices=['true', 'false'],
            description='Open the Gazebo client.',
        ),
        DeclareLaunchArgument(
            'world', default_value=str(config_dir / 'world.yaml'),
            description='Path to the Aerostack2 Gazebo world YAML.',
        ),
        OpaqueFunction(function=launch_simulation, args=[config_dir]),
    ])
