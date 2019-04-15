#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVOMIN 110
#define SERVOMAX 530

bool fingerings[12][8] = {
    {1, 1, 1, 0, 0, 0, 0, 0},  //A
    {1, 1, 0, 1, 1, 0, 0, 0},  //A#
    {1, 1, 0, 0, 0, 0, 0, 0},  //B
    {1, 1, 1, 1, 1, 1, 1, 1},  //C
    {1, 1, 1, 1, 1, 1, 1, 0},  //C#
    {1, 1, 1, 1, 1, 1, 1, 0},  //D
    {1, 1, 1, 1, 1, 1, 0, 0},  //D#
    {1, 1, 1, 1, 1, 1, 0, 0},  //E
    {1, 1, 1, 1, 1, 0, 0, 0},  //F
    {1, 1, 1, 1, 0, 1, 1, 1},  //F#
    {1, 1, 1, 1, 0, 0, 0, 0},  //G
    {1, 1, 1, 0, 1, 1, 0, 0}}; //G#

short positions[8][2] = {
    {},
    {175, 160},
    {130, 170},
    {30, 70},
    {80, 130},
    {120, 180},
    {150, 70},
    {180, 120}};

short servos[] = {8, 9, 11, 10, 6, 5, 7, 4};

short state = 0;
uint8_t servonum = 4;
int pos = 0;

void setup()
{
    pinMode(11, OUTPUT); //Pump
    pinMode(9, OUTPUT);  //Valve
    pwm.begin();
    pwm.setPWMFreq(60); // Analog servos run at ~60 Hz updates
    delay(10);
}

void rotate_from_to(uint16_t pos1, uint16_t pos2, short servonum)
{
    if (pos1 > pos2)
    {
        for (int pos = pos1; pos > pos2; --pos)
        {
            pwm.setPWM(servonum, 0, pos);
            delay(1);
        }
    }
    else
    {
        for (int pos = pos1; pos < pos2; ++pos)
        {
            pwm.setPWM(servonum, 0, pos);
            delay(1);
        }
    }
}

int get_pulse(int angle)
{
    return angle * 7 / 3 + SERVOMIN;
}

void loop()
{
    // Drive each servo one at a time

    // switch(state)
    // {
    //     case 0 :
    //         if(Serial.available() > 0) {
    //             char data = Serial.read();
    //             char str[2];
    //             str[0] = data;
    //             str[1] = '\0';
    //             Serial.print(str);
    //         }
    //         // Serial.print("A");
    //         break;
    //     default :
    //         break;
    // }

    // // Serial.println("B");
    // delay(1000);


    // rotate_from_to(int(positions[servonum-4][0]*7/3) + SERVOMIN, int(positions[servonum-4][1]*7/3) + SERVOMIN, servonum);
    // rotate_from_to(int(positions[servonum-4][1]*7/3) + SERVOMIN, int(positions[servonum-4][0]*7/3) + SERVOMIN, servonum);

    digitalWrite(11, LOW);

    

    // pwm.setPWM(servos[servonum], 0, p2);
    

    int p1 = get_pulse(positions[4][0]);
    int p2 = get_pulse(positions[4][1]);
    int p3 = get_pulse(positions[5][0]);
    int p4 = get_pulse(positions[5][1]);
    int p5 = get_pulse(positions[6][0]);
    int p6 = get_pulse(positions[7][0]);

    // digitalWrite(9, HIGH);
    pwm.setPWM(servos[4], 0, p2);
    pwm.setPWM(servos[6], 0, p5);
    pwm.setPWM(servos[7], 0, p6);
    delay(400);
    pwm.setPWM(servos[5], 0, p4);
    delay(400);

    digitalWrite(9, LOW);
    pwm.setPWM(servos[5], 0, p3);
    delay(400);
    pwm.setPWM(servos[4], 0, p1);
    delay(400);
    
    
    // rotate_from_to(p1, p2, servos[servonum]);
    // delay(100);
    // rotate_from_to(p2, p1, servos[servonum]);
    // delay(100);
    // servonum ++;
    // if (servonum > 5) servonum = 4;
}