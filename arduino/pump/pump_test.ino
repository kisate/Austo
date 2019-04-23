void setup() {
  pinMode(15, OUTPUT); //Pump
    pinMode(13, OUTPUT);  //Valve
}

void loop() {

  digitalWrite(13, LOW);
  // digitalWrite(11, HIGH);
  delay(1000);
  digitalWrite(13, HIGH);
  delay(1000);

//   digitalWrite(48, LOW);
//   digitalWrite(50, HIGH); // sets the digital pin 13 off
//   delay(1000);            // waits for a second
}