/*

This example code is in the public domain
http://arduino.cc/en/Tutorial/WiFi101ThingSpeakDataUploader



http://www.arduinesp.com/arduinesp/wp-content/uploads/2015/04/ThingspeakESP8266.txt
*/


#include <SPI.h>
#include <ESP8266WiFi.h>




// replace with your channel's thingspeak API key, 
String apiKey = "A3STSBSVLKFDT2PQ"; 
const char* ssid = "UDay Tangs NET_guest"; //replace
const char* password = "tangsguest"; //replace
const char* server = "api.thingspeak.com";
 
WiFiClient client;
   
 
void setup() {                
  Serial.begin(115200);
  delay(10);
  
  WiFi.begin(ssid, password);
 
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
   
  WiFi.begin(ssid, password);
   
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  
}
 
 
void loop() {
   
  float h = 375;
  float t = 29;
  
  if (client.connect(server,80)) {  //   "184.106.153.149" or api.thingspeak.com
    String postStr = apiKey;
           postStr +="&field1=";
           postStr += String("april");
           postStr +="&field2=";
           postStr += String(t);
           postStr +="&field3=";
           postStr += String(h);
           postStr += "\r\n\r\n";
 
     client.print("POST /update HTTP/1.1\n"); 
     client.print("Host: api.thingspeak.com\n"); 
     client.print("Connection: close\n"); 
     client.print("X-THINGSPEAKAPIKEY: "+apiKey+"\n"); 
     client.print("Content-Type: application/x-www-form-urlencoded\n"); 
     client.print("Content-Length: "); 
     client.print(postStr.length()); 
     client.print("\n\n"); 
     client.print(postStr);
           
 
     Serial.print("quality: ");
     Serial.print(t);
     Serial.print(" temp: "); 
     Serial.print(h);
     Serial.println("% send to Thingspeak");    
  }
  client.stop();
   
  Serial.println("Waiting...");    
  // thingspeak needs minimum 15 sec delay between updates
  delay(20000);  
}
