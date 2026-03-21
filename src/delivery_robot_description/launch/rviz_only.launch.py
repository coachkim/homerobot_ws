import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    pkg_description_path = get_package_share_directory('delivery_robot_description')
    
    # [변경] 기본 경로를 설정하되, 외부에서 인자를 통해 변경 가능하게 만듦
    default_rviz_config_path = os.path.join(pkg_description_path, 'rviz', 'default.rviz')
    
    rviz_config_arg = DeclareLaunchArgument(
        'rviz_config',
        default_value=default_rviz_config_path,
        description='Full path to the RViz config file to use'
    )

    return LaunchDescription([
        rviz_config_arg,
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            # [변경] LaunchConfiguration을 통해 전달받은 경로 사용
            arguments=['-d', LaunchConfiguration('rviz_config')],
            parameters=[{'use_sim_time': True}], # 시뮬레이션 시간 동기화 필수
            output='screen'
        ),
    ])