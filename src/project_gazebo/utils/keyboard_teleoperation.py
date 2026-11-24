#!/usr/bin/env python3
"""Run the installed keyboard teleoperation with the Humble API workaround."""

import argparse
import inspect
from pathlib import Path
import runpy
import sys

from ament_index_python.packages import get_package_share_directory
import yaml


def fix_motion_reference_handler():
    from as2_python_api import drone_interface_teleop

    handler = drone_interface_teleop.MotionReferenceHandlerModule
    if inspect.isabstract(handler) and handler.__abstractmethods__ == {'__call__'}:
        class ConcreteMotionReferenceHandler(handler):
            def __call__(self, *args, **kwargs) -> bool:
                raise NotImplementedError('Use hover(), position, speed or speed_in_a_plane')

        drone_interface_teleop.MotionReferenceHandlerModule = ConcreteMotionReferenceHandler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('namespace', help='Drone namespaces separated by commas')
    args = parser.parse_args()

    package = Path(get_package_share_directory('as2_keyboard_teleoperation'))
    config = package / 'config' / 'teleop_values_config.yaml'
    parameters = yaml.safe_load(config.read_text())['/**']['ros__parameters']
    parameters['namespace'] = args.namespace
    for key in ('verbose', 'use_sim_time'):
        parameters[key] = str(parameters[key]).lower()

    fix_motion_reference_handler()
    executable = package / 'keyboard_teleoperation.py'
    sys.argv = [str(executable), *(f'--{key}={value}' for key, value in parameters.items())]
    runpy.run_path(str(executable), run_name='__main__')


if __name__ == '__main__':
    main()
