#include <Arduino.h>

// [왼쪽 모터 - Channel A]
const int AIN1 = 8;
const int AIN2 = 7;
const int PWMA = 6;

// [오른쪽 모터 - Channel B]
const int BIN1 = 12;
const int BIN2 = 11;
const int PWMB = 10;

// [LED 설정]
const int LED_PIN = 13; // 아두이노 내장 LED

void setup() {
  // 모든 핀을 출력(OUTPUT)으로 설정
  pinMode(AIN1, OUTPUT); pinMode(AIN2, OUTPUT); pinMode(PWMA, OUTPUT);
  pinMode(BIN1, OUTPUT); pinMode(BIN2, OUTPUT); pinMode(PWMB, OUTPUT);
  pinMode(LED_PIN, OUTPUT); // LED 핀 설정
  
  Serial.begin(9600);
  Serial.println("7800X3D급 듀얼 모터 + LED 시스템 가동!");
}

void loop() {
  // --- 1. 파이(도커)로부터 온 명령 확인 ---
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == '1') {
      digitalWrite(LED_PIN, HIGH);
      Serial.println("LED ON!");
    } else if (cmd == '0') {
      digitalWrite(LED_PIN, LOW);
      Serial.println("LED OFF!");
    }
  }

  // --- 2. 기존 모터 주행 루틴 ---
  Serial.println("양쪽 바퀴 전진!");
  digitalWrite(AIN1, HIGH); digitalWrite(AIN2, LOW); analogWrite(PWMA, 190);
  digitalWrite(BIN1, HIGH); digitalWrite(BIN2, LOW); analogWrite(PWMB, 210);

  // 주의: delay 동안은 시리얼 명령을 받을 수 없으므로 반응이 늦을 수 있습니다.
  delay(2000); 

  Serial.println("전체 정지!");
  digitalWrite(AIN1, LOW); digitalWrite(AIN2, LOW); analogWrite(PWMA, 0);
  digitalWrite(BIN1, LOW); digitalWrite(BIN2, LOW); analogWrite(PWMB, 0);
  
  delay(1000);
}