#define UPBORDER 9
#define DOWNBORDER 7 
#define ARMSMOTOR 
void setup()
{
  pinMode(DOWNBORDER, INPUT_PULLUP);
  pinMode(13, OUTPUT);
}

void loop()
{
  if (digitalRead(DOWNBORDER) == 1)
  {
    digitalWrite(13, HIGH);
  }
  else digitalWrite(13, LOW);
}