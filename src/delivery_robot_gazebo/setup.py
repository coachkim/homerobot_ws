from setuptools import setup, find_packages # find_packages를 추가했습니다.
import os
from glob import glob

package_name = 'delivery_robot_gazebo'

setup(
    name=package_name,
    version='0.0.0',
    # 패키지 내의 파이썬 모듈을 자동으로 찾아주는 함수입니다.
    packages=find_packages(exclude=['test']), 
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # [중요] Launch 파일들을 설치 폴더(install)로 복사합니다.
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        # [중요] Gazebo 월드 파일들을 설치 폴더로 복사합니다.
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ksw',
    maintainer_email='ksw@todo.todo',
    description='Delivery Robot Gazebo Simulation Package',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # 나중에 파이썬 노드를 만들면 여기에 등록합니다.
            # '노드이름 = 패키지명.파일명:메인함수'
        ],
    },
)