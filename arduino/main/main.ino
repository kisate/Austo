#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>


Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVOMIN  150
#define SERVOMAX  600
 
bool fingerings [12][8] = {
    {1, 1, 1, 0, 0, 0, 0, 0}, //A
    {1, 1, 0, 1, 1, 0, 0, 0}, //A#
    {1, 1, 0, 0, 0, 0, 0, 0}, //B
    {1, 1, 1, 1, 1, 1, 1, 1}, //C
    {1, 1, 1, 1, 1, 1, 1, 0}, //C#
    {1, 1, 1, 1, 1, 1, 1, 0}, //D
    {1, 1, 1, 1, 1, 1, 0, 0}, //D#
    {1, 1, 1, 1, 1, 1, 0, 0}, //E
    {1, 1, 1, 1, 1, 0, 0, 0}, //F
    {1, 1, 1, 1, 0, 1, 1, 1}, //F#
    {1, 1, 1, 1, 0, 0, 0, 0}, //G
    {1, 1, 1, 0, 1, 1, 0, 0}}; //G#

short state = 0;

void setup() {
    Serial.begin(9600);

    // pwm.begin();
    // pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
    delay(10);
}

// you can use this function if you'd like to set the pulse length in seconds
// e.g. setServoPulse(0, 0.001) is a ~1 millisecond pulse width. its not precise!
void setServoPulse(uint8_t n, double pulse) {
  double pulselength;
  
  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= 60;   // 60 Hz
  Serial.print(pulselength); Serial.println(" us per period"); 
  pulselength /= 4096;  // 12 bits of resolution
  Serial.print(pulselength); Serial.println(" us per bit"); 
  pulse *= 1000000;  // convert to us
  pulse /= pulselength;
  Serial.println(pulse);
  pwm.setPWM(n, 0, pulse);
}

void loop() {
  // Drive each servo one at a time

    switch(state)
    {
        case 0 :
            if(Serial.available() > 0) {
                char data = Serial.read();
                char str[2];
                str[0] = data;
                str[1] = '\0';
                Serial.print(str);
            }
            Serial.print("A");
            break;
        default :
            break;
    }

    Serial.println("B");
    delay(1000);
}