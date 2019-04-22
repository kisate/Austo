#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVOMIN 80
#define SERVOMAX 600
#define UPBORDER 9
#define DOWNBORDER 7 
#define ARMSMOTORUP 50
#define ARMSMOTORDOWN 48
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
    {25, 0},
    {75, 100}, 
    {75, 100}, // палец болтается
    {75, 100}, // перетянуть
    {75, 100},
    {25, 0},
    {25, 0}};


short servos[] = {3, 2, 0, 1, 6, 5, 7, 4};

short state = 0;
short sequence[100][2];
short seq_length = 0;


short tempo = 100;
uint16_t beat = 500;
uint16_t times[] = {6*beat, 5*beat, 4*beat, 3*beat, 2.5*beat, 2*beat, 3*beat/2, beat, 3*beat/4, beat/2, beat/4};


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

    delay(100);
    
    digitalWrite(PUMP, HIGH);
    digitalWrite(VALVE, HIGH);
    digitalWrite(ARMSMOTORUP, LOW);
    digitalWrite(ARMSMOTORDOWN, LOW);

    delay(100);
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
// void loop()
// {
//     // if 


//     // Drive each servo one at a time

//     // switch(state)
//     // {
//     //     case 0 :
//     //         if(Serial.available() > 0) {
//     //             char data = Serial.read();
//     //             char str[2];
//     //             str[0] = data;
//     //             str[1] = '\0';
//     //             Serial.print(str);
//     //         }
//     //         // Serial.print("A");
//     //         break;
//     //     default :
//     //         break;
//     // }

//     // // Serial.println("B");
//     // delay(1000);


//     // rotate_from_to(int(positions[servonum-4][0]*7/3) + SERVOMIN, int(positions[servonum-4][1]*7/3) + SERVOMIN, servonum);
//     // rotate_from_to(int(positions[servonum-4][1]*7/3) + SERVOMIN, int(positions[servonum-4][0]*7/3) + SERVOMIN, servonum);


    

//     // pwm.setPWM(servos[servonum], 0, p2);
    

//     // int p1 = get_pulse(positions[4][0]);
//     // int p2 = get_pulse(positions[4][1]);
//     // int p3 = get_pulse(positions[5][0]);
//     // int p4 = get_pulse(positions[5][1]);
//     // int p5 = get_pulse(positions[6][0]);
//     // int p6 = get_pulse(positions[7][0]);

//     // digitalWrite(9, HIGH);
//     // pwm.setPWM(servos[4], 0, p2);
//     // pwm.setPWM(servos[6], 0, p5);
//     // pwm.setPWM(servos[7], 0, p6);
//     // delay(400);
//     // pwm.setPWM(servos[5], 0, p4);
//     // delay(400);

//     // digitalWrite(9, LOW);
//     // pwm.setPWM(servos[5], 0, p3);
//     // delay(400);
//     // pwm.setPWM(servos[4], 0, p1);
//     // delay(400);
    
    
//     // int note = scale[step];
//     // step++;
//     // if (step > 6) step = 0;

//     // pick_note(note);
//     // delay(1000);

//     if(Serial.available() > 0) {
// 		char data = Serial.read();
// 		char str[2];
// 		str[0] = data;
// 		str[1] = '\0';
// 		Serial.print(str);
//         pick_note(int(data));
//         delay(1000);
// 	}


//     // int p1 = get_pulse(positions[servonum][1]);
//     // int p2 = get_pulse(positions[servonum][0]);

//     // rotate_from_to(p1, p2, servos[servonum]);
//     // delay(100);
//     // rotate_from_to(p2, p1, servos[servonum]);
//     // delay(100);
//     // servonum ++;
//     // if (servonum > 7) servonum = 1;

// }

// void setup() {
// 	Serial.begin(115200);
// }
void loop() {
	if(state == 0 && Serial.available() > 1) {
		unsigned note = Serial.read();
        unsigned dur = Serial.read();
		
        if (note > 11) state = 1;

        else 
        {
            sequence[seq_length][0] = note;
            sequence[seq_length][1] = dur;
            seq_length ++;
            Serial.write(note);
        }
	}

    else if (state == 1)
    {
        // digitalWrite(11, LOW);
        for (int i = 0; i < seq_length; ++i)
        {
            pick_note(sequence[i][0]);
            digitalWrite(13, LOW);
            delay(uint16_t(times[sequence[i][1]]*0.95));
            digitalWrite(13, HIGH);
            delay(uint16_t(times[sequence[i][1]]*0.05));
        }
    }

    // Serial.print("A");
    
}