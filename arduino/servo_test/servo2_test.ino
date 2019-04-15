#include <Servo.h>

Servo myservo;
Servo myservo2;
Servo myservo3; // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0; // variable to store the servo position

void setup()
{
  myservo.attach(1);
  myservo2.attach(2);
  myservo3.attach(3); // attaches the servo on pin 9 to the servo object
}

void loop()
{
  for (pos = 30; pos <= 70; pos += 1)
  { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo3.write(pos);
    myservo2.write(100 + pos);
    myservo.write(pos + 80); // tell servo to go to position in variable 'pos'
    delay(10);               // waits 15ms for the servo to reach the position
  }
  for (pos = 70; pos >= 30; pos -= 1)
  { // goes from 180 degrees to 0 degrees
    myservo3.write(pos);
    myservo2.write(100 + pos);
    myservo.write(80 + pos); // tell servo to go to position in variable 'pos'
    delay(10);               // waits 15ms for the servo to reach the position
  }
}