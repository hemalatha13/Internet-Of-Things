const int led = 16; 
const int button = 2; 
int previousReading = LOW;
int counter = 0; 

int state = 0;

void setup() {
pinMode(led, OUTPUT);
pinMode(button, INPUT);
Serial.begin(9600);
}

void loop() {

int reading = digitalRead(button);
if (reading == HIGH && previousReading == LOW) {
delay(100);
if (previousReading == LOW && reading == HIGH) {
digitalWrite(led, HIGH);
delay(100);
counter++;
Serial.print("Button pressed ");
Serial.print(counter);
Serial.println(" times");
digitalWrite(led, LOW);
delay(100);
}

}
previousReading = reading;

}
