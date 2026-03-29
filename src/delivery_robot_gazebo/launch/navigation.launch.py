import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_gazebo_path = get_package_share_directory('delivery_robot_gazebo')
    nav2_launch_path = os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py')

    map_file = os.path.join(pkg_gazebo_path, 'maps', 'my_home_map.yaml')
    params_file = os.path.join(pkg_gazebo_path, 'config', 'nav2_params.yaml') 

    # [EKF 노드 정의]
    start_robot_localization_cmd = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[os.path.join(pkg_gazebo_path, 'config', 'ekf.yaml')],
    )

    return LaunchDescription([
        # 1. EKF 노드 실행 (리스트에 추가!)
        #start_robot_localization_cmd,

        # 2. Nav2 Bringup 실행
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(nav2_launch_path),
            launch_arguments={
                'map': map_file,
                'use_sim_time': 'true',
                'params_file': params_file
            }.items()
        )
    ])