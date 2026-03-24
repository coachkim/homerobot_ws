import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    pkg_gazebo_path = get_package_share_directory('delivery_robot_gazebo')
    nav2_launch_path = os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py')

    # 1. 우리가 저장한 지도 파일 경로
    map_file = os.path.join(pkg_gazebo_path, 'maps', 'my_home_map.yaml')

    # 2. 내비게이션 파라미터 파일 (기본값 사용 후 나중에 튜닝)
    # [수정 전] params_file = os.path.join(get_package_share_directory('nav2_bringup'), 'params', 'nav2_params.yaml')
    # [수정 후] 패키지 안의 config 폴더를 가리키게 바꿉니다.
    params_file = os.path.join(pkg_gazebo_path, 'config', 'nav2_params.yaml') 

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(nav2_launch_path),
            launch_arguments={
                'map': map_file,
                'use_sim_time': 'true',
                'params_file': params_file
            }.items()
        )
    ])