#define UPBORDER 9
#define DOWNBORDER 7 
#define ARMSMOTORUP 50
#define ARMSMOTORDOWN 48
void setup()
{
  pinMode(DOWNBORDER, INPUT_PULLUP);
  pinMode(UPBORDER, INPUT_PULLUP);
  pinMode(13, OUTPUT);
  pinMode(ARMSMOTORDOWN, OUTPUT);
  pinMode(ARMSMOTORUP, OUTPUT);
}

void loop()
{
  rise_arms();
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

void rise_arms()
{
  while (digitalRead(UPBORDER) == 0)
  {
    digitalWrite(ARMSMOTORDOWN, LOW);
    digitalWrite(ARMSMOTORUP, HIGH);
  }
  digitalWrite(ARMSMOTORDOWN, LOW);
  digitalWrite(ARMSMOTORUP, LOW);
}