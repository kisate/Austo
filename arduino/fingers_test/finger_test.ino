#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVOMIN 80
#define SERVOMAX 600
#define VALVE 13
#define PUMP 17

short fingerings[12][8] = {
    {1, 1, 1, 1, 1, 1, 1, 1},  //C
    {1, 1, 1, 1, 1, 1, 1, 0},  //C#
    {1, 1, 1, 1, 1, 1, 1, 0},  //D
    {1, 1, 1, 1, 1, 1, 0, 0},  //D#
    {1, 1, 1, 1, 1, 1, 0, 0},  //E
    {1, 1, 1, 1, 1, 0, 0, 0},  //F
    {1, 1, 1, 1, 0, 1, 1, 1},  //F#
    {1, 1, 1, 1, 0, 0, 0, 0},  //G
    {1, 1, 1, 0, 1, 1, 0, 0},   //G#
    {1, 1, 1, 0, 0, 0, 0, 0},  //A
    {1, 1, 0, 1, 1, 0, 0, 0},  //A#
    {1, 1, 0, 0, 0, 0, 0, 0}}; //B
    
short scale[] = {3, 5, 7, 8, 10, 0, 2};
short positions[8][2] = {
    {0, 0},
    {40, 15},
    {60, 100}, 
    {20, 80}, 
    {45, 90},
    {25, 90},
    {100, 40},
    {70, 30}};

short servos[] = {0, 1, 2, 3, 4, 5, 6, 10, 8};

short state = 0;
short sequence[100];
short seq_length = 0;

short tempo = 120;

uint16_t beat = 60/tempo*1000;
uint16_t times[] = {4*beat, 2*beat, 3*beat/2, beat, beat/2, 3*beat/4, beat/4};


void setup()
{
    Serial.begin(115200);
    
    pwm.begin();
    pwm.setPWMFreq(60); // Analog servos run at ~60 Hz updates
    
    
    pinMode(17, OUTPUT); //Pump HIGH -- off, LOW -- on
    pinMode(13, OUTPUT);  //Valve HIGH -- off, LOW -- on
    delay(100);
    digitalWrite(13, HIGH);
    digitalWrite(17, LOW);
    pwm.setPWM(8, 0, get_pulse(50));
    pick_note(0);
}

void pick_note(uint8_t note)
{
    for (int i = 0; i < 8; ++i)
    {
        int p = get_pulse(positions[i][fingerings[note][i]]);
        
        pwm.setPWM(servos[i], 0, p);
    }
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
    return map(angle, 0, 100, SERVOMIN, SERVOMAX);
}

void loop() {
	if(Serial.available() > 1) {
		unsigned s = Serial.read();
		unsigned angle = Serial.read();
		
        // Serial.write(s);
        // Serial.write(angle);
        // if (angle > 20) 
        
        if (s == 11)
        {
            digitalWrite(13, LOW);
            digitalWrite(17, HIGH);
        }
        else if (s == 12)
        {
            digitalWrite(13, HIGH);
            digitalWrite(17, LOW);
            pwm.setPWM(8, 0, get_pulse(45));
        }
        else if(s == 10)
        {
            for (int i = SERVOMIN; i < SERVOMAX; ++i)
            {
                pwm.setPWM(angle, 0, i);
            }
            for (int i = SERVOMAX; i > SERVOMIN; --i)
            {
                pwm.setPWM(angle, 0, i);
            }
        }
        else if (s > 7)
        {
            pick_note(angle);
        }
        else 
        {
            pwm.setPWM(servos[s], 0, get_pulse(angle));
        }
        // else 
        // pwm.setPWM(servos[s], 0, SERVOMIN);
        // pick_note(s);
        // delay(times[angle]);
        // Serial.write()
	}

    // for (int note = 0; note < 12; ++note)
    // {
    //     pick_note(note);
    //     delay(2000);
    // }
    
    // for (int note = 11; note >= 0; --note)
    // {
    //     pick_note(note);
    //     delay(2000);
    // }

}