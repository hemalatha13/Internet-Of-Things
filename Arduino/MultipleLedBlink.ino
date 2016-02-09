
int ledPins[] = {12,13,14,15,16};
void setup() {
  // put your setup code here, to run once:
  for(int i = 0; i < 5; i++){         //this is a loop and will repeat eight times
      pinMode(ledPins[i],OUTPUT); //we use this to set each LED pin to output
  }   
}

void loop() {
  // put your main code here, to run repeatedly:
  oneAfterAnother();
}

void oneAfterAnother(){
  int delayTime = 500;
  //Turn Each LED on one after another
  for(int i = 0; i <= 4; i++){
    digitalWrite(ledPins[i], HIGH);  //Turns on LED #i each time this runs i
    delay(delayTime);                //gets one added to it so this will repeat
  } 

  //Turn Each LED off one after another
  for(int i = 4; i >= 0; i--){  //same as above but rather than starting at 0 and counting up
                                //we start at seven and count down
    digitalWrite(ledPins[i], LOW);  //Turns off LED #i each time this runs i
    delay(delayTime);                
  }
  digitalWrite(ledPins[0], HIGH);  //Turns on LED #0 (connected to pin 12 )
  digitalWrite(ledPins[1], HIGH);  //Turns on LED #1 (connected to pin 13 )
  digitalWrite(ledPins[2], HIGH);  //Turns on LED #2 (connected to pin 14 )
  digitalWrite(ledPins[3], HIGH);  //Turns on LED #3 (connected to pin 15 )
  digitalWrite(ledPins[4], HIGH);  //Turns on LED #4 (connected to pin 16 ) 
    delay(delayTime);                //waits delayTime milliseconds
  digitalWrite(ledPins[4], LOW);  //Turns on LED #4 (connected to pin 16 )
  digitalWrite(ledPins[3], LOW);  //Turns on LED #3 (connected to pin 15 )
  digitalWrite(ledPins[2], LOW);  //Turns on LED #2 (connected to pin 14 )
  digitalWrite(ledPins[1], LOW);  //Turns on LED #1 (connected to pin 13 )
  digitalWrite(ledPins[0], LOW);  //Turns on LED #0 (connected to pin 12 )          
  delay(delayTime);                //waits delayTime milliseconds
}

