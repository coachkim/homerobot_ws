from setuptools import setup, find_packages # find_packages 추가 확인
import os
from glob import glob

package_name = 'delivery_robot_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # [중요] URDF 폴더 안의 모든 파일을 설치 폴더로 복사
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        # [중요] RViz 설정 폴더 안의 모든 파일을 설치 폴더로 복사
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*')),
        # [선택] 만약 이 패키지에도 런치 파일이 있다면 추가 (rviz_only.launch.py 등)
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ksw',
    maintainer_email='ksw@todo.todo',
    description='Robot description package with URDF and RViz config',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)