import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    urdf_path = os.path.join(
        get_package_share_directory('warehouse_robot_description'),
        'urdf',
        'warehouse_robot_full.urdf.xacro'
    )

    gazebo_launch_path = os.path.join(
        get_package_share_directory('ros_gz_sim'),
        'launch',
        'gz_sim.launch.py'
    )

    bridge_config_path = os.path.join(
        get_package_share_directory('warehouse_robot_bringup'),
        'config',
        'gazebo_bridge.yaml'
    )

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[
                {'robot_description': ParameterValue(Command(f'xacro {urdf_path}'), value_type=str)},
                {'use_sim_time': True}
            ]
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gazebo_launch_path),
            launch_arguments={'gz_args': '-v 4 -r empty.sdf'}.items()
        ),
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-topic', 'robot_description', '-name', 'warehouse_robot']
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=['--ros-args', '-p', f'config_file:={bridge_config_path}']
        )
    ])