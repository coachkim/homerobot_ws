import os
import xacro  # [수정] xacro 파일을 해석하기 위해 라이브러리 추가
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # 패키지 경로 설정
    gazebo_pkg_path = get_package_share_directory('delivery_robot_gazebo')
    desc_pkg_path = get_package_share_directory('delivery_robot_description')

    # 1. 가제보 모델 경로 및 환경 변수 설정
    # [수정] os.path.dirname 제거: 'models' 폴더 자체를 경로로 지정해야 하위 모델을 바로 찾음
    gazebo_models_path = os.path.join(gazebo_pkg_path, 'models')
    
    # [보안] 기존 GAZEBO_MODEL_PATH가 없을 경우를 대비해 처리
    if 'GAZEBO_MODEL_PATH' in os.environ:
        model_path = gazebo_models_path + ':' + os.environ['GAZEBO_MODEL_PATH']
    else:
        model_path = gazebo_models_path

    set_gazebo_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH', 
        value=model_path
    )

    # 2. Gazebo 실행 (기본 gazebo.launch.py 호출)
    world_file = os.path.join(gazebo_pkg_path, 'worlds', 'home.world')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={'world': world_file}.items()
    )

    # 3. [핵심 수정] Xacro 파일을 URDF(XML)로 변환하여 읽기
    # [이유] Gazebo와 robot_state_publisher는 'xacro' 형식을 직접 읽지 못함
    # 따라서 런치 단계에서 xacro 명령어로 해석(Parse)하여 'xml' 문자열로 변환해야 함
    xacro_file = os.path.join(desc_pkg_path, 'urdf', 'delivery_robot.xacro')
    robot_description_config = xacro.process_file(xacro_file).toxml()

    # 4. 로봇 상태 퍼블리셔 (robot_state_publisher) 실행
    # [수정] 변환된 robot_description_config(XML 문자열)를 파라미터로 전달
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_config}]
    )

    # 5. 가제보에 로봇 소환 (spawn_entity)
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description', 
            '-entity', 'delivery_robot',
            '-z', '0.1'  # <--- 이 줄을 꼭 추가해 주세요!
        ],
        output='screen'
    )

    return LaunchDescription([
        set_gazebo_model_path,
        gazebo,
        rsp,
        spawn_entity
    ])