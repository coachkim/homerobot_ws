#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <Adafruit_BMP280.h>

// 스캐너에서 확인한 주소로 확실하게 지정!
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28); 
Adafruit_BMP280 bmp; 

void setup() {
  Serial.begin(9600);
  while (!Serial); 
  Serial.println("--- 7800X3D급 정밀 센서 모니터링 시작 ---");

  // BNO055 초기화
  if (!bno.begin()) {
    Serial.println("BNO055가 응답하지 않습니다. 다시 시도 중...");
    delay(1000);
    if(!bno.begin()) { Serial.println("BNO055 최종 실패!"); while(1); }
  }

  // BMP280 초기화 (0x76 주소 명시)
  if (!bmp.begin(0x76)) {
    Serial.println("BMP280을 찾을 수 없습니다!");
    while (1);
  }

  Serial.println("모든 센서 연결 성공! 데이터를 출력합니다.");
  bno.setExtCrystalUse(true);
}

void loop() {
  // 1. 방향 데이터 (각도)
  sensors_event_t event;
  bno.getEvent(&event);

  // 2. 출력 (Yaw: 수평 회전, Roll: 좌우 기울기, Pitch: 앞뒤 기울기)
  Serial.print("Y: "); Serial.print(event.orientation.x, 1);
  Serial.print(" R: "); Serial.print(event.orientation.y, 1);
  Serial.print(" P: "); Serial.print(event.orientation.z, 1);
  
  // 3. 온도/기압 데이터
  Serial.print(" | T: "); Serial.print(bmp.readTemperature(), 1);
  Serial.print("C | P: "); Serial.print(bmp.readPressure()/100.0F, 1);
  Serial.println(" hPa");

  delay(200); // 0.2초마다 갱신 (빠른 반응!)

  // 보정 상태 읽기 (0: 미보정, 3: 완벽보정)
  uint8_t system, gyro, accel, mag;
  system = gyro = accel = mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);

  // 출력 추가
  Serial.print(" [CAL] Sys:"); Serial.print(system);
  Serial.print(" G:"); Serial.print(gyro);
  Serial.print(" A:"); Serial.print(accel);
  Serial.print(" M:"); Serial.println(mag);

  delay(200);
}



// // [왼쪽 모터 - Channel A]
// const int AIN1 = 8; const int AIN2 = 7; const int PWMA = 6;
// // [오른쪽 모터 - Channel B]
// const int BIN1 = 12; const int BIN2 = 11; const int PWMB = 10;
// // [상태 표시 LED]
// const int LED_PIN = 13;

// void stopMotors() {
//   digitalWrite(AIN1, LOW); digitalWrite(AIN2, LOW); analogWrite(PWMA, 0);
//   digitalWrite(BIN1, LOW); digitalWrite(BIN2, LOW); analogWrite(PWMB, 0);
//   Serial.println("Robot: STOP");
// }

// void setup() {
//   pinMode(AIN1, OUTPUT); pinMode(AIN2, OUTPUT); pinMode(PWMA, OUTPUT);
//   pinMode(BIN1, OUTPUT); pinMode(BIN2, OUTPUT); pinMode(PWMB, OUTPUT);
//   pinMode(LED_PIN, OUTPUT);
  
//   Serial.begin(9600);
//   stopMotors(); // 처음엔 정지 상태로 시작
//   Serial.println("Command Mode Ready! (F: Forward, B: Backward, S: Stop)");
// }

// void loop() {
//   if (Serial.available() > 0) {
//     char cmd = Serial.read(); // 파이에서 보낸 한 글자 읽기

//     if (cmd == 'F' || cmd == 'f') { // 전진
//       digitalWrite(AIN1, HIGH); digitalWrite(AIN2, LOW); analogWrite(PWMA, 190);
//       digitalWrite(BIN1, HIGH); digitalWrite(BIN2, LOW); analogWrite(PWMB, 210);
//       digitalWrite(LED_PIN, HIGH);
//       Serial.println("Robot: FORWARD");
//     } 
//     else if (cmd == 'B' || cmd == 'b') { // 후진
//       digitalWrite(AIN1, LOW); digitalWrite(AIN2, HIGH); analogWrite(PWMA, 190);
//       digitalWrite(BIN1, LOW); digitalWrite(BIN2, HIGH); analogWrite(PWMB, 210);
//       digitalWrite(LED_PIN, HIGH);
//       Serial.println("Robot: BACKWARD");
//     } 
//     else if (cmd == 'S' || cmd == 's') { // 정지
//       stopMotors();
//       digitalWrite(LED_PIN, LOW);
//     }
//   }
// }