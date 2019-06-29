#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVOMIN 80
#define SERVOMAX 600
#define UPBORDER 9
#define DOWNBORDER 5 
#define ARMSMOTORUP 48
#define ARMSMOTORDOWN 50
#define HEADSERVO 8
#define PUMP 17 //HIGH -- off, LOW -- on
#define VALVE 13 //HIGH -- off, LOW -- on
#define LCD 3


short fingerings[12][8] = {
    {1, 1, 1, 1, 1, 1, 1, 1},  //C
    {1, 1, 1, 1, 1, 1, 1, 0},  //C#
    {1, 1, 1, 1, 1, 1, 1, 0},  //D
    {1, 1, 1, 1, 1, 1, 0, 0},  //D#
    {1, 1, 1, 1, 1, 1, 0, 0},  //E
    {1, 1, 1, 1, 1, 0, 0, 0},  //F
    {1, 1, 1, 1, 0, 1, 1, 1},  //F#
    {1, 1, 1, 1, 0, 0, 0, 0},  //G
    {1, 1, 1, 0, 1, 1, 0, 0}, //G#
    {1, 1, 1, 0, 0, 0, 0, 0},  //A
    {1, 1, 0, 1, 1, 0, 0, 0},  //A#
    {1, 1, 0, 0, 0, 0, 0, 0}};  //B
short scale[] = {3, 5, 7, 8, 10, 0, 2};
short positions[8][2] = {
    {0, 0},
    {40, 15},
    {70, 100}, 
    {75, 100}, 
    {45, 90},
    {40, 100},
    {95, 60},
    {85, 25}};

short servos[] = {0, 1, 2, 3, 4, 5, 6, 7, 8};

short state = 0;

byte buffer[50];

bool read_seq = false;
bool read_meta = false;

uint16_t sequence[1024][3];
uint16_t seq_length = 0; 
unsigned tempo = 0;
uint16_t total_seq_length = 0;

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
    pick_note(0);
    delay(100);
    lower_arms();
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
        
        delay(1500);

        for (int i = 22; i <= 45; ++i)
        {
            pwm.setPWM(8, 0, get_pulse(i));
            delay(50);
        }
        
        digitalWrite(VALVE, LOW);
        digitalWrite(PUMP, LOW);    

        raise_arms();
        
        delay(4000);

        state = 1;

        Serial.write(1);
    }

    else if (state == 1 && Serial.available() > 0)
    {
        Serial.read();

        delay(500);

        pick_note(0);
        digitalWrite(VALVE, HIGH);
        delay(1000);
        
        pick_note(4);
        delay(1000);

        pick_note(7);
        delay(1000);

        digitalWrite(VALVE, LOW);
        digitalWrite(PUMP, HIGH);

        state = 3;
        Serial.write(1);

    }

    else if (state == 2 && Serial.available() > 0)
    {   
        Serial.read();

        delay(500);

        pick_note(10);
        digitalWrite(VALVE, HIGH);
        digitalWrite(PUMP, LOW);
        delay(1000);
        
        pick_note(2);
        delay(1000);

        pick_note(5);
        delay(1000);

        digitalWrite(VALVE, LOW);
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
        digitalWrite(VALVE, LOW);
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

            digitalWrite(VALVE, LOW);
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
        for (int i = 0; i < seq_length; ++i)
        {
            if (sequence[i][0] == 12)
            {
                digitalWrite(VALVE, LOW);
                digitalWrite(PUMP, HIGH);
                
                delay(uint16_t(sequence[i][1]*semiq2*1));
            }

            else 
            {
                pick_note(sequence[i][0]);
                digitalWrite(PUMP, LOW);
                digitalWrite(VALVE, HIGH);
                delay(uint16_t(sequence[i][1]*semiq2*0.95));
                digitalWrite(VALVE, LOW);
                delay(uint16_t(sequence[i][1]*semiq2*0.05));
            }
        }

        digitalWrite(VALVE, LOW);
        digitalWrite(PUMP, HIGH);
        seq_length = 0;
        state = 6;
        
        Serial.write(1);
    }

    else if(state == 6 && Serial.available() > 3) {

        Serial.readBytes(buffer, 4);
        Serial.write(1);

        if (not read_meta)
        {
            total_seq_length = ((unsigned) buffer[2]) << 8 | ((unsigned) buffer[3]);
            read_meta = true;
        }

        else 
        {
            unsigned note = (unsigned) buffer[0];
            unsigned velocity = (unsigned) buffer[1];
            uint16_t msg_time = ((unsigned) buffer[2] << 8) | (unsigned) buffer[3]; 
            sequence[seq_length][0] = note;
            sequence[seq_length][1] = velocity;
            sequence[seq_length][2] = msg_time;
            seq_length++;
            if (seq_length == total_seq_length) 
            {
                digitalWrite(PUMP, LOW);
                digitalWrite(VALVE, LOW);
                delay(1000);
                
                state = 7;
            }  
        }  
	}

    else if (state == 7 && Serial.available() > 0)
    {   
        Serial.read();
        

        for (int i = 0; i < seq_length; ++i)
        {

            delay(sequence[i][2]);
            pick_note(sequence[i][0]);
            
            if (sequence[i][1] > 0)
            {
                digitalWrite(VALVE, HIGH);    
                digitalWrite(PUMP, LOW);
            }
            else 
            {
                digitalWrite(VALVE, LOW);
            } 

        }

        digitalWrite(VALVE, LOW);
        digitalWrite(PUMP, HIGH);
        state = 8;
        lower_arms();
        Serial.write(1);
    }   
}