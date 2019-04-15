#define AMotorCW 1
#define AMotorCCW 2
#define AMotorPWM 3

#define BMotorCW 6
#define BMotorCCW 7
#define BMotorPWM 5

#define CMotorCW 8
#define CMotorCCW 9
#define CMotorPWM 10

#define DMotorCW 12
#define DMotorCCW 13
#define DMotorPWM 11

#define Speed 150

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

 pinMode(CMotorCW, OUTPUT);
 pinMode(CMotorCCW, OUTPUT);
 pinMode(CMotorPWM, OUTPUT);

}
void motorA(int motspeed)
{ 
 if (motspeed >= 0)
 {
  analogWrite(AMotorPWM, motspeed);
  digitalWrite(AMotorCW, LOW);
  digitalWrite(AMotorCCW, HIGH);
 }
 else
 {
  analogWrite(AMotorPWM, -motspeed);
  digitalWrite(AMotorCW, HIGH);
  digitalWrite(AMotorCCW, LOW);
 }
}

void motorB(int motspeed)
{ 
 if (motspeed >= 0)
 {
  analogWrite(BMotorPWM, motspeed);
  digitalWrite(BMotorCW, LOW);
  digitalWrite(BMotorCCW, HIGH);
 }
 else
 {
  analogWrite(BMotorPWM, -motspeed);
  digitalWrite(BMotorCW, HIGH);
  digitalWrite(BMotorCCW, LOW);
 }
}

void motorC(int motspeed)
{ 
 if (motspeed >= 0)
 {
  analogWrite(CMotorPWM, motspeed);
  digitalWrite(CMotorCW, LOW);
  digitalWrite(CMotorCCW, HIGH);
 }
 else
 {
  analogWrite(CMotorPWM, -motspeed);
  digitalWrite(CMotorCW, HIGH);
  digitalWrite(CMotorCCW, LOW);
 }
}

void motorD(int motspeed)
{ 
 if (motspeed >= 0)
 {
  analogWrite(DMotorPWM, motspeed);
  digitalWrite(DMotorCW, LOW);
  digitalWrite(DMotorCCW, HIGH);
 }
 else
 {
  analogWrite(DMotorPWM, -motspeed);
  digitalWrite(DMotorCW, HIGH);
  digitalWrite(DMotorCCW, LOW);
 }
}

void loop() {


  motorA(Speed);
  motorB(Speed);
  motorC(Speed);
  motorD(Speed);
  delay(4000);
  motorA(0);
  motorB(0);
  motorC(0);
  motorD(0);
  delay(1000);
  motorA(-Speed);
  motorB(-Speed);
  motorC(-Speed);
  motorD(-Speed);
  delay(4000);
  motorA(0);
  motorB(0);
  motorC(0);
  motorD(0);
  delay(1000);


  /*
  for (int i = 0; i <= 100; i++)
   {
       
    delay(15);
   }
   
  delay(5000); 
  
  for (int i = 100; i >= 0; i--)
   {
    
    
    delay(15);
   }
  
  for (int i = 0; i <= 100; i++)
   {
        
    delay(15);
   }
   
  delay(5000); 
  
  for (int i = 100; i >= 0; i--)
   {
        
    delay(15);  
   }
   */
}
