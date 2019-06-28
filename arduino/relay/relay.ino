#define PUMP 17
#define VALVE1 13
void setup()
{
    pinMode(PUMP, OUTPUT); //Pump HIGH -- off, LOW -- on
    pinMode(VALVE1, OUTPUT);

    digitalWrite(PUMP, LOW);
    digitalWrite(VALVE1, LOW);
}
void loop()
{
    digitalWrite(VALVE1, LOW);
    digitalWrite(PUMP, LOW);
    // digitalWrite(VALVE3, LOW);
    delay(3000);
    digitalWrite(VALVE1, HIGH);
    digitalWrite(PUMP, HIGH);
    // digitalWrite(VALVE3, HIGH);
    delay(3000);
}