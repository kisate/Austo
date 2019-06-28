#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVOMIN 80
#define SERVOMAX 600
#define PUMP 17 //HIGH -- off, LOW -- on
#define VALVE 13 //HIGH -- off, LOW -- on

byte buffer[50];

bool read_meta = false;
bool read_seq = false;

uint16_t sequence[1024][3];
uint16_t seq_length = 0; 
unsigned tempo = 0;
uint16_t total_seq_length = 0;

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
    {50, 100},
    {95, 60},
    {75, 35}};

short servos[] = {0, 1, 2, 3, 4, 5, 6, 7, 8};


void setup()
{
    Serial.begin(115200);

    pwm.begin();
    pwm.setPWMFreq(60); // Analog servos run at ~60 Hz updates
    
    pinMode(PUMP, OUTPUT); 
    pinMode(VALVE, OUTPUT);  
    
    delay(100);
    
    digitalWrite(PUMP, HIGH);
    digitalWrite(VALVE, LOW);
    
    delay(100);
    pick_note(0);
    delay(100);

    pwm.setPWM(8, 0, get_pulse(45));
}

void pick_note(uint8_t note)
{
    for (int i = 0; i < 8; ++i)
    {
        int p = get_pulse(positions[i][fingerings[note][i]]);
        pwm.setPWM(i, 0, p);
    }
}

int get_pulse(int angle)
{
    return map(angle, 0, 100, SERVOMIN, SERVOMAX);
}

void loop()
{
    if (not read_seq && Serial.available() > 3)
    {   
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
                read_seq = true;  
                digitalWrite(VALVE, LOW);    
                digitalWrite(PUMP, LOW);
                delay(4000);
            }
        }  
    }

    if (read_seq)
    {
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
    }
}