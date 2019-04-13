
void setup() {
	Serial.begin(115200); // use the same baud-rate as the python side
}

int a = 180;
int b = 180; 

void loop() {
	Serial.print(a);
	delay(1000);
	a += 1;
}