import rclpy
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
import math

# Yaw 각도를 쿼터니언으로 변환하는 함수
def euler_to_quaternion(yaw):
    return [0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0)]

def main():
    rclpy.init()
    nav = BasicNavigator()

    # 1. POI (Point of Interest) 정의
    poi = {
        "HOME":    [0.0, 0.0, 0.0],
        "KITCHEN": [-3.5, 2.0, 0.0],
        "ROOM_M":  [1.0, 3.0, -3.0],
        "ROOM_S1": [-3.5, -1.0, -3.0966],
        "ROOM_S2": [-4.5, 4.5, -0.77]
    }

    # 2. 로봇 초기 위치 활성화 (Wait for Nav2 to be active)
    # nav.setInitialPose(...) # 필요 시 설정

    # 3. 배송 목적지 설정 (여기를 수정해서 테스트해보세요!)
    target = "ROOM_S1" # <-- 주방으로 보내려면 "KITCHEN"으로 변경
    
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = nav.get_clock().now().to_msg()
    
    # 좌표 입력
    goal_pose.pose.position.x = poi[target][0]
    goal_pose.pose.position.y = poi[target][1]
    
    # 방향 입력 (Euler to Quaternion 변환 적용)
    q = euler_to_quaternion(poi[target][2])
    goal_pose.pose.orientation.z = q[2]
    goal_pose.pose.orientation.w = q[3]

    # 4. 주행 명령 발사!
    print(f"🚀 {target}으로 배송을 시작합니다!")
    nav.goToPose(goal_pose)

    # 5. 주행 상태 모니터링
    while not nav.isTaskComplete():
        feedback = nav.getFeedback()
        if feedback:
            print(f'📍 남은 거리: {feedback.distance_remaining:.2f} m', end='\r')

    # 6. 결과 확인
    result = nav.getResult()
    if result == TaskResult.SUCCEEDED:
        print(f'\n✅ {target} 배송 완료!')
    elif result == TaskResult.CANCELED:
        print(f'\n❌ 배송이 취소되었습니다.')
    elif result == TaskResult.FAILED:
        print(f'\n⚠️ 배송 실패!')

    rclpy.shutdown()

if __name__ == '__main__':
    main()