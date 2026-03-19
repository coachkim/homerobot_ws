import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # 1. 패키지 및 파일 경로 설정
    pkg_description_path = get_package_share_directory('delivery_robot_description')
    xxacro_file = os.path.join(pkg_description_path, 'urdf', 'delivery_robot.xacro')
    rviz_config_path = os.path.join(pkg_description_path, 'rviz', 'default.rviz')
    
    # 2. Xacro 파일을 XML(URDF)로 변환
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    # 3. Gazebo 실행 (GUI를 끄고 물리 엔진만 실행)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={'gui': 'true'}.items() # ★ GUI를 끔으로써 저사양 환경 최적화(다시킴)
    )

    # 4. Robot State Publisher (TF 데이터 게시)
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_raw,
            'use_sim_time': True
        }]
    )

    # 5. Gazebo에 로봇 소환 (Spawn)
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'delivery_robot'],
        output='screen'
    )

    # 6. RViz2 실행 (저장된 설정 파일 로드)
    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
        node_rviz,
    ])