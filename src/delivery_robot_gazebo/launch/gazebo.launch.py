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

    # 3. [핵심 수정] 가제보 패키지에 저장한 '시뮬레이션 전용 RViz 설정' 경로 지정
    sim_rviz_config_path = os.path.join(pkg_gazebo_path, 'rviz', 'delivery_robot.rviz')

    # 4. rviz_only.launch.py 포함 (인자 전달)
    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            pkg_description_path, 'launch', 'rviz_only.launch.py'
        )]),
        # [변경] rviz_only에 시뮬레이션용 설정 파일 경로를 인자로 넘겨줌
        launch_arguments={'rviz_config': sim_rviz_config_path}.items()
    )

    return LaunchDescription([
        sim_launch,
        rviz_launch
    ])