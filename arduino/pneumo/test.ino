#define UPBORDER 9
#define DOWNBORDER 5
#define ARMSMOTORUP 48
#define ARMSMOTORDOWN 50
#define LCD 3
void setup()
{
  pinMode(DOWNBORDER, INPUT_PULLUP);
  pinMode(UPBORDER, INPUT_PULLUP);
  pinMode(13, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(ARMSMOTORDOWN, OUTPUT);
  pinMode(ARMSMOTORUP, OUTPUT);
}

void loop()
{
    
    raise_arms();
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