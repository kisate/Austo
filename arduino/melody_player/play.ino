#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVOMIN 80
#define SERVOMAX 600
#define PUMP 15 //HIGH -- off, LOW -- on
#define VALVE 13 //HIGH -- off, LOW -- on


short fingerings[12][8] = {
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
short scale[] = {3, 5, 7, 8, 10, 0, 2};
short positions[8][2] = {
    {0, 0},
    {30, 0},
    {70, 100}, 
    {70, 100}, // палец болтается
    {70, 100}, // перетянуть
    {70, 100},
    {30, 0},
    {30, 0}};


short servos[] = {3, 2, 0, 1, 6, 5, 7, 4};

short state = 0;
short sequence[100][2];
short seq_length = 0;
short prefix = 0;
short replays = 0;

short tempo = 100;
uint16_t semiq = 220;

void pick_note(uint8_t note)
{
    for (int i = 0; i < 8; ++i)
    {
        int p = get_pulse(positions[i][fingerings[note][i]]);
        pwm.setPWM(servos[i], 0, p);
    }
}

int get_pulse(int angle)
{
    return map(angle, 0, 100, SERVOMIN, SERVOMAX);
}

void setup()
{
    Serial.begin(115200);
    
    pwm.begin();
    pwm.setPWMFreq(60); // Analog servos run at ~60 Hz updates
    
    
    pinMode(PUMP, OUTPUT); 
    pinMode(VALVE, OUTPUT);  
    
    delay(100);
    
    digitalWrite(PUMP, HIGH);
    digitalWrite(VALVE, HIGH);
    
    delay(100);
    pick_note(3);
    delay(100);
}

void loop()
{
    if (state == 0 && Serial.available() > 1)
    {
        unsigned note = Serial.read();
        unsigned dur = Serial.read();
        Serial.write(note);
		
        if (dur == 0) 
        {
            
            digitalWrite(PUMP, LOW);
            digitalWrite(VALVE, HIGH);
            delay(3000);
               
            state = 1;
        }

        else 
        {
            sequence[seq_length][0] = note;
            sequence[seq_length][1] = dur;
            seq_length ++;
            
        }
    }
    else if (state == 1)
    {
        for (int i = prefix; i < seq_length; ++i)
        {
            if (sequence[i][0] == 12)
            {
                digitalWrite(VALVE, HIGH);
                digitalWrite(PUMP, LOW);
                
                delay(uint16_t(sequence[i][1]*semiq*1));
            }

            else 
            {
                pick_note(sequence[i][0]);
                digitalWrite(PUMP, LOW);
                digitalWrite(VALVE, LOW);
                delay(uint16_t(sequence[i][1]*semiq*1));
                // digitalWrite(PUMP, HIGH);
                // digitalWrite(VALVE, HIGH);
                // delay(uint16_t(sequence[i][1]*semiq*0.05));
            }
            
        }

        replays ++;

        digitalWrite(PUMP, LOW);
        digitalWrite(VALVE, HIGH);
        delay(4000);

        if (replays == 3)
        {
            state = 5;
            digitalWrite(PUMP, HIGH);
            digitalWrite(VALVE, HIGH);
            Serial.write(1);
        }
    }
}