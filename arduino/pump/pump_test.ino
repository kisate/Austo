void setup() {
  pinMode(11, OUTPUT); //Pump
    pinMode(9, OUTPUT);  //Valve
}

void loop() {

  digitalWrite(9, LOW);
  // digitalWrite(11, HIGH);
  delay(1000);
  digitalWrite(11, LOW);
  delay(1000);

//   digitalWrite(48, LOW);
//   digitalWrite(50, HIGH); // sets the digital pin 13 off
//   delay(1000);            // waits for a second
}