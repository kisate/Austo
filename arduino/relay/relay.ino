#define PUMP 15
#define VALVE1 13
#define VALVE2 29
#define VALVE3 27

void setup()
{
    pinMode(PUMP, OUTPUT); //Pump HIGH -- off, LOW -- on
    pinMode(VALVE1, OUTPUT);
    pinMode(VALVE2, OUTPUT); //Pump HIGH -- off, LOW -- on
    pinMode(VALVE3, OUTPUT);

    digitalWrite(PUMP, LOW);
    digitalWrite(VALVE1, HIGH);
    digitalWrite(VALVE3, HIGH);
}
void loop()
{
    digitalWrite(VALVE3, LOW);
    // digitalWrite(VALVE3, LOW);
    delay(1000);
    digitalWrite(VALVE3, HIGH);
    // digitalWrite(VALVE3, HIGH);
    delay(1000);
}