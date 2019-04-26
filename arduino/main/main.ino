#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVOMIN 80
#define SERVOMAX 600
#define UPBORDER 9
#define DOWNBORDER 7 
#define ARMSMOTORUP 50
#define ARMSMOTORDOWN 48
#define HEADSERVO 8
#define PUMP 15 //HIGH -- off, LOW -- on
#define VALVE 13 //HIGH -- off, LOW -- on
#define LCD 3


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
    {70, 100}, 
    {70, 100},
    {70, 100},
    {30, 0},
    {30, 0}};


short servos[] = {3, 2, 0, 1, 6, 5, 7, 4};

short state = 0;
short sequence[100][2];
short seq_length = 0;
short prefix = 0;


short tempo = 100;
uint16_t semiq1 = 125;
uint16_t semiq2 = 200;



void setup()
{
    Serial.begin(115200);
    
    pwm.begin();
    pwm.setPWMFreq(60); // Analog servos run at ~60 Hz updates
    
    
    pinMode(PUMP, OUTPUT); 
    pinMode(VALVE, OUTPUT);  
    pinMode(DOWNBORDER, INPUT_PULLUP);
    pinMode(UPBORDER, INPUT_PULLUP);
    pinMode(ARMSMOTORDOWN, OUTPUT);
    pinMode(ARMSMOTORUP, OUTPUT);
    pinMode(LCD, OUTPUT);

    delay(100);
    
    digitalWrite(PUMP, HIGH);
    digitalWrite(VALVE, HIGH);
    digitalWrite(ARMSMOTORUP, LOW);
    digitalWrite(ARMSMOTORDOWN, LOW);

    delay(100);
    pwm.setPWM(8, 0, get_pulse(45));
    pick_note(3);
    delay(100);
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

void lower_arms()
{
    while (digitalRead(DOWNBORDER) == 0)
    {
        digitalWrite(ARMSMOTORDOWN, HIGH);
        digitalWrite(ARMSMOTORUP, LOW);
    }

    digitalWrite(ARMSMOTORDOWN, LOW);
    digitalWrite(ARMSMOTORUP, LOW);
}

void raise_arms()
{
    while (digitalRead(UPBORDER) == 0)
    {
        digitalWrite(ARMSMOTORDOWN, LOW);
        digitalWrite(ARMSMOTORUP, HIGH);
    }

    digitalWrite(ARMSMOTORDOWN, LOW);
    digitalWrite(ARMSMOTORUP, LOW);
}

void loop() {

    if (state == 0 && Serial.available() > 0)
    {
        Serial.read();
        
        //lower_arms();

        for (int i = 45; i > 22; --i)
        {
            pwm.setPWM(8, 0, get_pulse(i));
            delay(50);
        }
        
        delay(2000);

        for (int i = 22; i <= 45; ++i)
        {
            pwm.setPWM(8, 0, get_pulse(i));
            delay(50);
        }

        raise_arms();
        
        digitalWrite(VALVE, HIGH);
        digitalWrite(PUMP, LOW);    

        delay(1000);

        state = 1;

        Serial.write(1);
    }

    else if (state == 1 && Serial.available() > 0)
    {
        Serial.read();

        delay(500);

        pick_note(3);
        digitalWrite(VALVE, LOW);
        delay(1000);
        
        pick_note(7);
        delay(1000);

        pick_note(10);
        delay(500);

        digitalWrite(VALVE, HIGH);
        delay(500);
        digitalWrite(PUMP, HIGH);

        state = 2;
        Serial.write(1);

    }

    else if (state == 2 && Serial.available() > 0)
    {   
        Serial.read();

        delay(500);

        pick_note(10);
        digitalWrite(VALVE, LOW);
        digitalWrite(PUMP, LOW);
        delay(1000);
        
        pick_note(2);
        delay(1000);

        pick_note(5);
        delay(500);

        digitalWrite(VALVE, HIGH);
        delay(500);
        digitalWrite(PUMP, HIGH);
        pick_note(3);

        Serial.write(1);

        state = 3;
    }

    else if(state == 3 && Serial.available() > 0)
    {
        Serial.read();
        for (int i = 45; i > 22; --i)
        {
            pwm.setPWM(8, 0, get_pulse(i));
            delay(50);
        }
        digitalWrite(LCD, HIGH);
        digitalWrite(VALVE, HIGH);
        digitalWrite(PUMP, HIGH);
        state = 4;
        Serial.write(1);
    }

	else if(state == 4 && Serial.available() > 1) {
        digitalWrite(LCD, LOW);
		unsigned note = Serial.read();
        unsigned dur = Serial.read();
        Serial.write(note);
		
        if (dur == 0) 
        {
            
            for (int i = 22; i <= 45; ++i)
            {
                pwm.setPWM(8, 0, get_pulse(i));
                delay(50);
            }

            digitalWrite(VALVE, HIGH);
            digitalWrite(PUMP, LOW);
            
            delay(1000);
               
            state = 5;
        }

        else 
        {
            sequence[seq_length][0] = note;
            sequence[seq_length][1] = dur;
            seq_length ++;
            
        }
	}

    else if (state == 5 && Serial.available() > 0)
    {
        Serial.read();
        short passed = 0;
        for (int i = prefix; i < seq_length; ++i)
        {
            if (sequence[i][0] == 12)
            {
                digitalWrite(VALVE, HIGH);
                digitalWrite(PUMP, HIGH);
                
                delay(uint16_t(sequence[i][1]*semiq2*1));
            }

            else 
            {
                pick_note(sequence[i][0]);
                digitalWrite(PUMP, LOW);
                digitalWrite(VALVE, LOW);
                delay(uint16_t(sequence[i][1]*semiq2*0.95));
                digitalWrite(VALVE, HIGH);
                delay(uint16_t(sequence[i][1]*semiq2*0.05));
            }
        }

        digitalWrite(VALVE, HIGH);
        digitalWrite(PUMP, HIGH);
        seq_length = 0;
        state = 6;
        
        Serial.write(1);
    }

    else if(state == 6 && Serial.available() > 1) {
        digitalWrite(LCD, LOW);
		unsigned note = Serial.read();
        unsigned dur = Serial.read();
        Serial.write(note);
		
        if (dur == 0) 
        {
            
            digitalWrite(PUMP, LOW);
            digitalWrite(VALVE, HIGH);
            delay(1000);
               
            state = 7;
        }

        else 
        {
            sequence[seq_length][0] = note;
            sequence[seq_length][1] = dur;
            seq_length ++;
            
        }
	}

    else if (state == 7 && Serial.available() > 0)
    {   
        Serial.read();

        short passed = 0;
        for (int i = prefix; i < seq_length; ++i)
        {
            if (sequence[i][0] == 12)
            {
                
                digitalWrite(VALVE, HIGH);
                digitalWrite(PUMP, HIGH);
                
                delay(uint16_t(sequence[i][1]*semiq1*1));
            }

            else 
            {
                pick_note(sequence[i][0]);
                digitalWrite(PUMP, LOW);
                digitalWrite(VALVE, LOW);
                delay(uint16_t(sequence[i][1]*semiq1*0.9));
                // digitalWrite(PUMP, HIGH);
                digitalWrite(VALVE, HIGH);
                delay(uint16_t(sequence[i][1]*semiq1*0.1));
            }
        }

        digitalWrite(VALVE, HIGH);
        digitalWrite(PUMP, HIGH);
        state = 8;
        Serial.write(1);
    }   
}