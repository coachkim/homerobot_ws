import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
import math

def euler_to_quaternion(yaw):
    return [0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0)]

def move_to_poi(nav, poi_name, coords):
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = nav.get_clock().now().to_msg()
    goal_pose.pose.position.x = coords[0]
    goal_pose.pose.position.y = coords[1]
    q = euler_to_quaternion(coords[2])
    goal_pose.pose.orientation.z = q[2]
    goal_pose.pose.orientation.w = q[3]

    print(f"\n🚚 [배송 중] 목적지: {poi_name}")
    nav.goToPose(goal_pose)

    while not nav.isTaskComplete():
        feedback = nav.getFeedback()
        if feedback:
            print(f'📍 남은 거리: {feedback.distance_remaining:.2f} m', end='\r')
    return nav.getResult()

def main():
    rclpy.init()
    nav = BasicNavigator()

    poi = {
        "HOME":    [0.0, 0.0, 0.0],
        "KITCHEN": [-4.0, 2.0, 0.0],
        "ROOM_M":  [1.0, 3.0, -3.0],
        "ROOM_S1": [-3.5, -1.0, -3.0966],
        "ROOM_S2": [-4.5, 4.5, -0.77]
    }

    menu_map = {"1": "KITCHEN", "2": "ROOM_M", "3": "ROOM_S1", "4": "ROOM_S2", "5" : "HOME"}

    while True:
        print("\n" + "="*40)
        print("   📦 유진로봇 스타일 'Job 생성' 모드")
        print("="*40)
        for k, v in menu_map.items():
            print(f"{k}. {v}")
        print("q. 종료")
        print("-" * 40)
        print("💡 여러 곳을 가려면 번호를 띄어쓰기로 입력하세요 (예: 1 3 2)")
        
        user_input = input("👉 배송 경로 입력: ").strip().lower()

        if user_input == 'q': break
        
        # 입력받은 번호들을 리스트로 변환
        job_list = user_input.split()
        
        # 1. Job 수행 (순차 배송)
        for idx, job in enumerate(job_list):
            if job not in menu_map:
                print(f"⚠️  {job}번은 없는 목적지라 건너뜁니다.")
                continue
            
            target_name = menu_map[job]
            result = move_to_poi(nav, target_name, poi[target_name])

            if result == TaskResult.SUCCEEDED:
                print(f"\n✅ [{idx+1}/{len(job_list)}] {target_name} 도착!")
                input("🔔 물건 수령 후 'Enter'를 누르면 다음 장소로 이동합니다...")
            else:
                print(f"\n❌ {target_name} 배송 실패. 미션을 중단합니다.")
                break

        # 2. 모든 Job 완료 후 자동 복귀
        print("\n🏁 모든 배송 업무가 끝났습니다. 홈으로 복귀합니다.")
        move_to_poi(nav, "HOME", poi["HOME"])
        print("\n🏠 거실 복귀 완료. 대기 중...")

    rclpy.shutdown()

if __name__ == '__main__':
    main()