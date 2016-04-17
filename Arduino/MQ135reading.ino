/* this code not only detects the overall airquality but also calculates the CO2 values
references: from adafruit and arduino blog
*/

#include "MQ135.h"



const int ANALOGPIN = A0; //GAS sensor output pin to Arduino analog A0 pin


void setup()
{
  Serial.begin(9600); //Initialize serial port - 9600 bps
}

void loop()
{

  
  MQ135 gasSensor = MQ135(ANALOGPIN);
      Serial.print("value is");

  Serial.println(analogRead(ANALOGPIN));
    Serial.print("rzero is");

  delay(1000); // Print value every 1 sec.
  float rzero = gasSensor.getRZero();
  Serial.print(rzero);
    Serial.print("ppm is");
float ppm = gasSensor.getPPM();
    Serial.print(ppm);


}

 
