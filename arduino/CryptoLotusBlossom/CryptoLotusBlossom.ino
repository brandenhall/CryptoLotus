#include <JeeLib.h>
#include <avr/sleep.h>

#define BAND RF12_915MHZ // wireless frequency band
#define GROUP 4     // wireless net group
#define NODE_ID 10   // node id
#define MAX_RETRY 3
#define ACK_TIME 10

byte command = 0;
byte offset = 0;

byte input[5];
byte inputIndex = 0;

byte lastPadId;
byte lastValue;

byte colors[6][3];
byte buttons[6];

boolean odd = true;

MilliTimer timer;

void setup() {
  Serial.begin(9600);  
  rf12_initialize(NODE_ID, BAND, GROUP);
  
  Serial.println("Crypto Lotus Blossom v1.0");  
  input[0] = 0;
  input[1] = 0;
  input[2] = 0;
  input[3] = 0;
  input[4] = 0;
  
  colors[0][0] = 0;
  colors[0][1] = 0;
  colors[0][2] = 0;
  
  colors[1][0] = 0;
  colors[1][1] = 0;
  colors[1][2] = 0;
  
  colors[2][0] = 0;
  colors[2][1] = 0;
  colors[2][2] = 0;
  
  colors[3][0] = 0;
  colors[3][1] = 0;
  colors[3][2] = 0;
  
  colors[4][0] = 0;
  colors[4][1] = 0;
  colors[4][2] = 0;
  
  colors[5][0] = 0;
  colors[5][1] = 0;
  colors[5][2] = 0;
  
  buttons[0] = 0;
  buttons[1] = 0;
  buttons[2] = 0;
  buttons[3] = 0;
  buttons[4] = 0;
  buttons[5] = 0;
  
  inputIndex = 0;
}


void handleInput() {  
  inputIndex = 0;
  
  if (input[0] == 1) {
    colors[input[1]][0] = input[2];
    colors[input[1]][1] = input[3];
    colors[input[1]][2] = input[4];
  }
}

void checkMessages() {
 if (rf12_recvDone() 
      && rf12_hdr == (RF12_HDR_DST | NODE_ID)
      && rf12_crc == 0) {
  
    // sensor on/off
    if (rf12_data[0] == 2) {
      
      Serial.print(rf12_data[1] - 10);
      Serial.println(rf12_data[2]);
      
    // bootstrapping
    } else if (rf12_data[0] == 128) {
      byte message[2];
      message[0] = 129;
      message[1] = offset + 10;
      offset += 1;

      delay(50);
      
      while (!rf12_canSend()) {
        rf12_recvDone();
        delay(10);
      } 
      
      rf12_sendStart(RF12_HDR_DST | 2, &message, sizeof message);
      rf12_sendWait(0);
    }
  }
}

// wait a few milliseconds for proper ACK to me, return true if indeed received
static byte waitForAck() {
  MilliTimer ackTimer;
  while (!ackTimer.poll(ACK_TIME)) {
    if (rf12_recvDone() 
      && rf12_crc == 0
      && rf12_hdr == RF12_HDR_CTL | lastPadId) {
      
      if (rf12_data[0] == 0) {
        if (buttons[rf12_data[1] - 1] != rf12_data[2]) {
          buttons[rf12_data[1] - 1] = rf12_data[2];
          
          Serial.print((char) 0);
          Serial.print((char) rf12_data[1] - 1);
          Serial.println((char) rf12_data[2]);
        }
      } else {
        Serial.print((char) rf12_data[0]);
        Serial.print((char) rf12_data[1]);
        Serial.println((char) rf12_data[2]);
      }
      
      return 1;
    }
  }
  return 0;
}

void loop() {
  while (Serial.available()) {
    byte value = Serial.read();
    
    if (inputIndex < 5) {
      input[inputIndex] = value;
      ++inputIndex;
    }
      
    if (value == 10) {
      handleInput();          
      inputIndex == 0;
    }

  }

  // loop over all of the lilypads, sending each its color
  for (byte i=0; i<6; ++i) {
    for (byte j=0; j<MAX_RETRY; ++j) {
      lastPadId = i + 1;
      rf12_sendNow(RF12_HDR_ACK | (RF12_HDR_DST | i + 1), &colors[i], sizeof colors[i]);
      rf12_sendWait(0);
      if (waitForAck()) {
          break;
      }
    }  
  } 
}
