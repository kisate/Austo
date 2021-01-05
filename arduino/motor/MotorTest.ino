#define AMotorCW 3
#define AMotorCCW 4
#define AMotorPWM 10

#define BMotorCW 7
#define BMotorCCW 8
#define BMotorPWM 9

#define CMotorCW 4
#define CMotorCCW 5
#define CMotorPWM 10

#define DMotorCW 12
#define DMotorCCW 13
#define DMotorPWM 11

#define Speed 255

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


  for (int i = 40; i < Speed; ++i)
  {
    motorA(i);
    delay(50);
  }


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
