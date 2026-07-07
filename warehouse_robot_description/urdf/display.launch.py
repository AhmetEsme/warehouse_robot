import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command

def generate_launch_description():

    urdf_path = os.path.join(
        get_package_share_directory('warehouse_robot_description'),
        'urdf',
        'standalone_arm.urdf.xacro'
    )

    rviz_config_path = os.path.join(
        get_package_share_directory('warehouse_robot_description'),
        'rviz',
        'urdf_config.rviz'
    )

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': Command(f'xacro {urdf_path}')}]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config_path]
        )
    ])