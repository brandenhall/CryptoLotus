#include <JeeLib.h>
#include <avr/sleep.h>

#define BAND RF12_915MHZ // wireless frequency band
#define GROUP 4     // wireless net group
#define NODE_ID 1   // node id
#define INPUT_PIN 6

byte code[3];

boolean odd = true;

MilliTimer timer;

void setup() {
  pinMode(INPUT_PIN, INPUT);
  
  code[0] = 1;
  code[1] = 1;
  code[2] = 1;
  Serial.begin(9600);  
  rf12_initialize(NODE_ID, BAND, GROUP);
  
  Serial.println("Crypto Lotus Special Box v1.0");  
}

void loop() {
  if (digitalRead(INPUT_PIN)) {
    Serial.println("Pressed!");
    rf12_sendNow(RF12_ACK_REPLY, &code, sizeof code);
  }
  delay(10);
}
