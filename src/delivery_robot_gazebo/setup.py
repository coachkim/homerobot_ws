from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'delivery_robot_gazebo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']), 
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Launch 파일 설치
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        # World 파일 설치
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
        # [핵심] 모델 폴더 내의 모든 파일(config, sdf 등)을 설치 폴더로 복사
        (os.path.join('share', package_name, 'models/my_house'), glob('models/my_house/*')),
        # [핵심 추가] rviz 폴더 내의 모든 .rviz 파일을 설치 경로로 복사해라!
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
        (os.path.join('share', package_name, 'maps'), glob('maps/*')), # 지도 폴더
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ksw',
    maintainer_email='ksw@todo.todo',
    description='Delivery Robot Gazebo Simulation Package',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)