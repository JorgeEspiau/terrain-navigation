# Project Gazebo

Please refer to https://aerostack2.github.io/_02_examples/gazebo/project_gazebo/index.html for more information.

## Instalación en Ubuntu 22.04

Esta guía instala ROS 2 Humble, Aerostack2 **1.1.3** y Gazebo Fortress para
volar `drone0` en simulación. Usa una sesión gráfica de Ubuntu para abrir
Gazebo y la ventana de teleoperación.

1. Sigue la guía de ROS 2 Humble para configurar el repositorio APT e instalar
   `ros-humble-desktop`. [Instalación oficial de ROS 2 Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)
2. Instala Aerostack2 y las dependencias del proyecto. El paquete de
   Aerostack2 trae las dependencias de Fortress en Humble. [Instalación de Aerostack2](https://aerostack2.org/docs/getting-started/installation), [Gazebo en Aerostack2](https://aerostack2.org/docs/aerial-platforms/gazebo-simulation)

   ```bash
   sudo apt update
   sudo apt install ros-humble-aerostack2 git tmux tmuxinator \
     python3-pip python3-tk python3-yaml python3-scipy
   ```

3. Para la ventana de teclado, comprueba primero si ya puedes importar
   `PySimpleGUI`. Si falta, instala una versión de la serie 4 en tu cuenta.
   [PySimpleGUI 4.60.5.1](https://pypi.org/project/pysimplegui/4.60.5.1/)

   ```bash
   /usr/bin/python3 -c 'import tkinter, PySimpleGUI'
   # Solo si falta PySimpleGUI
   /usr/bin/python3 -m pip install --user 'PySimpleGUI==4.60.5.1'
   ```

4. Copia la carpeta `project_gazebo` de esta entrega o clona la rama que
   contiene estos cambios en tu repositorio compartido. La guía usa
   `~/robmovil_ws/src/project_gazebo` como ruta de ejemplo. Comprueba que la
   copia contiene `utils/keyboard_teleoperation.py`,
   `config/ground_truth_fortress.yaml` y `config/pid_speed_controller_humble.yaml`.
   Los lanzadores usan los paquetes APT directamente y puedes ejecutarlos
   desde la carpeta del proyecto.

5. Comprueba que ROS encuentra la plataforma de Aerostack2 y que Fortress está
   disponible. La versión APT de Aerostack2 debe empezar por `1.1.3` y
   `ign gazebo --versions` debe mostrar una versión `6.x`.

   ```bash
   source /opt/ros/humble/setup.bash
   dpkg-query -W ros-humble-aerostack2
   ros2 pkg prefix as2_platform_gazebo
   ign gazebo --versions
   /usr/bin/python3 -c 'import tkinter, PySimpleGUI'
   ```

### Comando opcional `dron`

Si quieres cargar el entorno de la simulación escribiendo solo `dron`, añade
esta función al final de `~/.bashrc`:

```bash
dron() {
    unset PYTHONPATH
    source /opt/ros/humble/setup.bash || return
    unset CYCLONEDDS_URI FASTRTPS_DEFAULT_PROFILES_FILE FASTDDS_DEFAULT_PROFILES_FILE
    export ROS_DOMAIN_ID=75 ROS_LOCALHOST_ONLY=1 RMW_IMPLEMENTATION=rmw_fastrtps_cpp
    export IGN_PARTITION=project_gazebo_drone0 GZ_PARTITION=project_gazebo_drone0
    printf 'Dron: dominio %s, Fast DDS local\n' "$ROS_DOMAIN_ID"
}
```

Ejecuta `source ~/.bashrc` en los terminales que ya estén abiertos. Después
escribe `dron` en cada terminal donde vayas a usar la simulación o la
teleoperación.

## Execution

### Primera prueba de vuelo con ROS 2 Humble y Gazebo Fortress

Entra en la carpeta del proyecto en los **dos terminales**
(`cd ~/robmovil_ws/src/project_gazebo` si usaste la ruta de esta guía).
Después carga el entorno con el [comando `dron`](#comando-opcional-dron).

```bash
dron
```

En el **primer terminal**, arranca la simulación en un servidor tmux aislado
para que los procesos hereden el perfil del dron. El lanzador abre la ventana
de Fortress.

```bash
export TMUX_TMPDIR="$(mktemp -d /tmp/project_gazebo_tmux.XXXXXX)"
./launch_as2.bash -n drone0
```

En el **segundo terminal**, comprueba que la plataforma ofrece
`/drone0/set_arming_state` en **Service Servers** y que despegue y aterrizaje
muestran **Action servers: 1**. Después abre la interfaz de teclado.

```bash
ros2 node list --no-daemon
ros2 node info /drone0/platform
ros2 action info /drone0/TakeoffBehavior
ros2 action info /drone0/LandBehavior
```

```bash
python3 utils/keyboard_teleoperation.py drone0
```

Con la ventana del teclado enfocada, pulsa **`t`** para armar y despegar,
**flechas** para mover, **Espacio** para mantener posición y **`l`** para
aterrizar. Puedes observar el desplazamiento con
`ros2 run tf2_ros tf2_echo earth drone0/base_link`.

El aviso `Trajectory generator service not found` hace referencia al
servicio antiguo `traj_gen/run_node`. El vuelo básico con el teclado usa
los controles de posición y velocidad y puede continuar.

Para cerrar, aterriza el dron y cierra la ventana de teclado. Pulsa
**Ctrl+B** y luego **D** para salir de la vista de tmux. En el mismo terminal
donde configuraste `TMUX_TMPDIR`, ejecuta `./stop.bash`.

### 1. Launch aerostack2 nodes for each drone
To launch aerostack2 nodes for each drone, execute once the following command:

```bash
./launch_as2.bash
```

The flags for the components launcher are:

- **-m**: multi agent. Default not set
- **-n**: select drones namespace to launch, values are comma separated. By default, it will get all drones from world description file
- **-s**: if set, the simulation will not be launched. Default launch simulation
- **-g**: launch using gnome-terminal instead of tmux. Default not set

### 2. Launch aerostack2 nodes for the ground station
To launch aerostack2 nodes for the ground station, execute once the following command:

```bash
./launch_ground_station.bash
```

The flags for the components launcher are:

- **-m**: multi agent. Default not set
- **-t**: launch keyboard teleoperation. Default not launch
- **-v**: open rviz. Default not launch
- **-r**: record rosbag. Default not launch
- **-n**: drone namespaces, comma separated. Default get from world description config file
- **-g**: launch using gnome-terminal instead of tmux. Default not set

### 3. Launch a mission
There are several missions that can be executed:

- **AS2 keyboard teleoperation control**: You can use the keyboard teleoperation launched with the ground station, using the flag `-t`:
  ```bash
  ./launch_ground_station.bash -t
  ```
  You can launch a **swarm of drones** with the flag `-m` and control them with the keyboard teleoperation, as:
  ```bash
  ./launch_as2.bash -m
  ```
  ```bash
  ./launch_ground_station.bash -m -t
  ```
- **AS2 Python API single drone mission**: You can execute a mission that used AS2 Python API, launching the mission with:
  ```bash
  python3 mission.py
  ```
- **AS2 Python API single drone mission using GPS**: You can execute a mission that used AS2 Python API with GPS, launching the mission with:
  ```bash
  python3 mission_gps.py
  ```
- **AS2 Python API swarm of drones mission**: You can execute a mission with a swarm of drones that used AS2 Python API, launching the mission with:
  ```bash
  python3 mission_swarm.py
  ```
  You must launch a **swarm of drones** with the flag `-m`, as:
  ```bash
  ./launch_as2.bash -m
  ```
  ```bash
  ./launch_ground_station.bash -m
  ```
- **AS2 Mission Interpreter single drone mission**: You can execute a mission that used AS2 Mission Interpreter, launching the mission with:
  ```bash
  python3 mission_interpreter.py
  ```
- **AS2 Behavior Trees single drone mission**: You can execute a mission that used AS2 Behavior Trees, launching the mission with:
  ```bash
  python3 mission_behavior_tree.py
  ```

### 4. End the execution

If you are using tmux, you can end the execution with the following command:

```bash
./stop.bash
```

You can force the end of all tmux sessions with the command:
```bash
tmux kill-server
```

If you are using gnome-terminal, you can end the execution by closing the terminal.


## Developers guide

All projects in aerostack2 are structured in the same way. The project is divided into the following directories:

- **tmuxinator**: Contains the tmuxinator launch file, which is used to launch all aerostack2 nodes.
  - **aerostack2.yaml**: Tmuxinator launch file for each drone. The list of nodes to be launched is defined here.
  - **ground_station.yaml**: Tmuxinator launch file for the ground station. The list of nodes to be launched is defined here.
- **config**: Contains the configuration files for the launchers of the nodes in the drones.
- **config_ground_station**: Contains the configuration files for the launchers of the nodes in the ground station.
- **launch_as2.bash**: Script to launch nodes defined in *tmuxinator/aerostack2.yaml*.
- **launch_ground_station.bash**: Script to launch nodes defined in *tmuxinator/ground_station.yaml*.
- **mission_\*.py**: Differents python mission files that can be executed.
- **stop_tmuxinator_as2.bash**: Script to stop all nodes launched by *launch_as2.bash*.
- **stop_tmuxinator_ground_station.bash**: Script to stop all nodes launched by *launch_ground_station.bash*.
- **stop_tmuxinator.bash**: Script to stop all nodes launched by *launch_as2.bash* and *launch_ground_station.bash*.
- **rosbag/record_rosbag.bash**: Script to record a rosbag. Can be modified to record only the topics that are needed.
- **trees\***: Contains the behavior trees that can be executed. They can be selected in the *aerostack2.yaml* file.
- **utils**: Contains utils scripts for launchers.

Both python and bash scripts have a help message that can be displayed by running the script with the `-h` option. For example, `./launch_as2.bash -h` will display the help message for the `launch_as2.bash` script.

**Note**: For knowing all parameters for each launch, you can execute the following command:

```bash
ros2 launch my_package my_launch.py -s
```

Also, you can see them in the default config file of the package, in the *config* folder. If you want to modify the default parameters, you can add the parameter to the config file.
