#include <Arduino.h>

// [TB6612FNG / L298N 공용 제어 핀]
const int IN1 = 8;  // 방향 제어 1
const int IN2 = 7;  // 방향 제어 2
const int PWM = 6;  // 속도 제어 (물결표시 핀)

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(PWM, OUTPUT);
  
  // 시리얼 모니터 (디버깅용)
  Serial.begin(9600);
  Serial.println("모터 테스트 준비 완료!");
}

void loop() {
  Serial.println("전진!");
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(PWM, 200); // 0~255 사이 속도
  delay(2000);

  Serial.println("정지!");
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  delay(1000);
}