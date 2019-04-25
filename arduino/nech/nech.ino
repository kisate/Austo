#include <TimerOne.h>
#include <button.h>
#include <MsTimer2.h>
#define eA A0
#define eB A1
#define eC A2
#define eD A3
#define eE A4
#define eF A5
#define eG A6
#define eH A7
int ms = 10000;
Button encoderA (eA, 4); // сигнал A
Button encoderB (eB, 4); //  сигнал B
Button encoderC (eC, 4); // сигнал A
Button encoderD (eD, 4); //  сигнал B
Button encoderE (eE, 4); // сигнал A
Button encoderF (eF, 4); //  сигнал B
Button encoderG (eG, 4); // сигнал A
Button encoderH (eH, 4); //  сигнал B

long posA = 0, posC = 0, posE = 0, posG = 0; // пооложение энкодера
float speedA = 50000, speedC = 50000, speedE = 50000, speedG = 50000;
long time1 = 0, time2 = 0, time3 = 0, time4 = 0;

#define AMotorCW 2
#define AMotorCCW 3
#define AMotorPWM 4

#define BMotorCW 7
#define BMotorCCW 6
#define BMotorPWM 5

#define CMotorCW 8
#define CMotorCCW 9
#define CMotorPWM 10

#define DMotorCW 12
#define DMotorCCW 11
#define DMotorPWM 13

int Speed = 200;
float speedich1 = 80, speedich2 = 80, speedich3 = 80, speedich4 = 80;
void setup() {
  
  pinMode(AMotorCW, OUTPUT);
  pinMode(AMotorCCW, OUTPUT);
  pinMode(AMotorPWM, OUTPUT);
 
  pinMode(BMotorCW, OUTPUT);
  pinMode(BMotorCCW, OUTPUT);
  pinMode(BMotorPWM, OUTPUT);

  pinMode(CMotorCW, OUTPUT);
  pinMode(CMotorCCW, OUTPUT);
  pinMode(CMotorPWM, OUTPUT);

  pinMode(DMotorCW, OUTPUT);
  pinMode(DMotorCCW, OUTPUT);
  pinMode(DMotorPWM, OUTPUT);
  Serial.begin(115200); // инициализируем порт, скорость 9600
  Timer1.initialize(250); // инициализация таймера 1, период 250 мкс
  Timer1.attachInterrupt(timerInterrupt, 250); // задаем обработчик прерываний
  
}
void motorA(int motspeed)
{ 
 if (motspeed > 0)
 {
  analogWrite(AMotorPWM, motspeed);
  digitalWrite(AMotorCW, LOW);
  digitalWrite(AMotorCCW, HIGH);
 }
 else if (motspeed < 0)
 {
  analogWrite(AMotorPWM, -motspeed);
  digitalWrite(AMotorCW, HIGH);
  digitalWrite(AMotorCCW, LOW);
 }
 else
 {
  analogWrite(AMotorPWM, 0);
  digitalWrite(AMotorCW, LOW);
  digitalWrite(AMotorCCW, LOW);
  }
}

void motorB(int motspeed)
{ 
 if (motspeed > 0)
 {
  analogWrite(BMotorPWM, motspeed);
  digitalWrite(BMotorCW, LOW);
  digitalWrite(BMotorCCW, HIGH);
 }
 else if (motspeed < 0)
 {
  analogWrite(BMotorPWM, -motspeed);
  digitalWrite(BMotorCW, HIGH);
  digitalWrite(BMotorCCW, LOW);
 }
 else
 {
   analogWrite(BMotorPWM, 0);
   digitalWrite(BMotorCW, LOW);
   digitalWrite(BMotorCCW, LOW);
 }
}

void motorC(int motspeed)
{ 
 if (motspeed > 0)
 {
  analogWrite(CMotorPWM, motspeed);
  digitalWrite(CMotorCW, LOW);
  digitalWrite(CMotorCCW, HIGH);
 }
 else if(motspeed < 0)
 {
  analogWrite(CMotorPWM, -motspeed);
  digitalWrite(CMotorCW, HIGH);
  digitalWrite(CMotorCCW, LOW);
 }
 else
 {
   analogWrite(CMotorPWM, 0);
   digitalWrite(CMotorCW, LOW);
   digitalWrite(CMotorCCW, LOW);  
 }
}

void motorD(int motspeed)
{ 
 if (motspeed > 0)
 {
  analogWrite(DMotorPWM, motspeed);
  digitalWrite(DMotorCW, LOW);
  digitalWrite(DMotorCCW, HIGH);
 }
 else if(motspeed < 0)
 {
  analogWrite(DMotorPWM, -motspeed);
  digitalWrite(DMotorCW, HIGH);
  digitalWrite(DMotorCCW, LOW);
 }
 else
 {
    analogWrite(DMotorPWM, 0);
    digitalWrite(DMotorCW, LOW);
    digitalWrite(DMotorCCW, LOW); 
  }
}
void motor_go(int speed1, int speed2, int speed3, int speed4){
  if(speedich2 < 255 && speedich2 > 0)
    if(speed2 < 0)
    {
      motorA((int)(-speedich2));
      speed2 = abs(speed2);
    }
    else if(speed2 != 0)
      motorA((int)(speedich2));
    else
      motorA(0);
  if(speedich1 < 255 && speedich1 > 0)
    if(speed1 < 0)
    {
      motorC((int)(-speedich1));
      speed1 = abs(speed1);
    }
    else if (speed1 != 0)
      motorC((int)(speedich1));
    else
      motorC(0);
  if(speedich4 < 255 && speedich4 > 0)
    if(speed4 < 0)
    {
      motorB((int)(-speedich4));
      speed4 = abs(speed4);
    }
    else if (speed4 != 0)
      motorB((int)(speedich4));
    else
    motorB(0);
      
  if(speedich3 < 255 && speedich3 > 0)
    if(speed3 < 0)
    {
      motorD((int)(-speedich3));
      speed3 = abs(speed3);
    }
    else if(speed3 != 0)
      motorD((int)(speedich3));
    else
      motorD(0);
  if(speedA > 300)
    speedA = 0;
      speedich1 -= 0.1*(speedA - speed1);
  if(speedC > 300)
    speedC = 0;
      speedich2 -= 0.1*(speedC - speed2);
  if(speedE > 300)
    speedE = 0;
      speedich3 -= 0.1*(speedE - speed3);
  if(speedG > 300)
   speedG = 0;
      speedich4 -= 0.1*(speedG - speed4);
  }
  void motor_stop()
  {
    motorA(0);
    motorB(0);
    motorC(0);
    motorD(0);
  }
  void motor_go_time(int p1, int p2, int p3, int p4, int timer)
  {
    unsigned long timeich = millis();
    while(millis() < timeich + timer)
      motor_go(p1,p2,p3,p4);
    motor_stop();
    delay(10);   
    motor_stop();   
    // Serial.println("DONE");
  }
  void motor_go_enc(int p1, int p2, int p3, int p4, int timer)
  {
    posA = 0;
    while(posA < timer)
      motor_go(p1,p2,p3,p4);
    motor_stop();
    delay(10);   
    motor_stop();
    // Serial.println("DONE");
  }
  void backward(int s, int timeichkekich)
  {
    speedich1 = speedich2 = speedich3 = speedich4 = 80;
    motor_go_time(-s, s, -s, s, timeichkekich);
  }
  void forward(int s, int timeichkekich)
  {
    speedich1 = speedich2 = speedich3 = speedich4 = 80;
    motor_go_time(s, -s, s, -s, timeichkekich);
  }
  void right(int s, int timeichkekich)
  {
    speedich1 = speedich2 = speedich3 = speedich4 = 80;
    motor_go_time(s, s, s, s, timeichkekich);
  }
  void left(int s, int timeichkekich)
  {
    speedich1 = speedich2 = speedich3 = speedich4 = 80;
    motor_go_time(-s, -s, -s, -s, timeichkekich);
  }
  void rotate(int s, int timeichkekich)
  {
    speedich1 = speedich2 = speedich3 = speedich4 = 80;
    motor_go_enc(-s, -s, s, s, timeichkekich);
  }
void loop() {

  if (Serial.available() > 0)
  {
    forward(55, 2000);
    delay(4000);
    left(25, 2000);
    delay(4000);
    Serial.read();
  }
}
void timerInterrupt() {
  time1++;
  time2++;
  time3++;
  time4++;
  encoderA.filterAvarage(); // вызов метода фильтрации
  encoderB.filterAvarage();
  encoderC.filterAvarage();// вызов метода фильтрации 
  encoderD.filterAvarage();
  encoderE.filterAvarage(); // вызов метода фильтрации
  encoderF.filterAvarage();
  encoderG.filterAvarage();// вызов метода фильтрации 
  encoderH.filterAvarage();
// обработка сигналов энкодера
  if( encoderA.flagClick == true ) {
    encoderA.flagClick = false;
      if( encoderB.flagPress == true) {
        posA++;
      }
      else {
        posA++;
      }
      speedA = ms / time1;
      time1 = 0;
  } 
  if( encoderC.flagClick == true ) {
    encoderC.flagClick = false;
      if( encoderD.flagPress == true) {
        posC++;
      }
      else {
        posC++;
      }
      speedC = ms / time2;
      time2 = 0;
  }
  if( encoderE.flagClick == true ) {
    encoderE.flagClick = false;
      if( encoderF.flagPress == true) {
        posE++;
      }
      else {
        posE++;
      }
      speedE = ms / time3;
      time3 = 0;
  } 
  if( encoderG.flagClick == true ) {
    encoderG.flagClick = false;
      if( encoderH.flagPress == true) {
        posG++;
      }
      else {
        posG++;
      }
      speedG = ms / time4;
      time4 = 0;
  } 
}
