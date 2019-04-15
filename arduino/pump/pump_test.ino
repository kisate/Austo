void setup() {
  pinMode(48, OUTPUT);
  pinMode(50, OUTPUT); 
  delay(100);   // sets the digital pin 13 as output
}

void loop() {
  digitalWrite(48, HIGH); //LOW -- up; HIGH -- down
  digitalWrite(50, LOW); // HIGH -- up; LOW -- down
  delay(100);         
//   digitalWrite(48, LOW);
//   digitalWrite(50, HIGH); // sets the digital pin 13 off
//   delay(1000);            // waits for a second
}