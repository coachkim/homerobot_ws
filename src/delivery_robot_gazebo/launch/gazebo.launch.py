import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # 1. 경로 설정
    pkg_description_path = get_package_share_directory('delivery_robot_description')
    pkg_gazebo_path = get_package_share_directory('delivery_robot_gazebo')

    # 2. sim_only.launch.py 포함 (가제보 + 로봇 소환)
    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            pkg_gazebo_path, 'launch', 'sim_only.launch.py'
        )])
    )

    # 3. rviz_only.launch.py 포함 (시각화)
    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            pkg_description_path, 'launch', 'rviz_only.launch.py'
        )])
    )

    return LaunchDescription([
        sim_launch,
        rviz_launch
    ])