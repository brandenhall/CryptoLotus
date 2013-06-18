#include <JeeLib.h>

#define BAND RF12_915MHZ // wireless frequency band
#define GROUP 4     // wireless net group
#define NODE_ID 1   // node id
#define POLL_RATE 10

byte command = 0;
byte offset = 0;

byte reset[4];
byte input[5];
byte inputIndex = 0;

MilliTimer timer;

void setup() {
  reset[0] = 0;
  reset[1] = 0;
  reset[2] = 0;
  reset[3] = 0;
  Serial.begin(57600);  
  rf12_initialize(NODE_ID, BAND, GROUP);
  
  input[0] = 0;
  input[1] = 0;
  input[2] = 0;
  input[3] = 0;
  input[4] = 0;
  
  inputIndex = 0;
}


void handleInput() {  
  inputIndex = 0;
  
  if (input[0] == 0 && input[1] == 0 && input[2] == 0 && input[3] == 0 && input[4] == 0) {
    
    offset = 0;
         
    while (!rf12_canSend()) {
      rf12_recvDone();
      delay(10);
    }
    
    rf12_sendStart(RF12_HDR_DST | 2, &reset, sizeof reset);
    rf12_sendWait(0);
    
  } else if (input[0] == 1) {
    byte message[4];
    message[0] = 1;
    message[1] = input[2];
    message[2] = input[3];
    message[3] = input[4];
    
    while (!rf12_canSend()) {
      checkMessages();
      delay(10);
    }
    
    rf12_sendStart(RF12_HDR_DST | (input[1] + 10), &message, sizeof message);
    rf12_sendWait(0);
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

void loop() {
  if (timer.poll(POLL_RATE)) {
    checkMessages();
  }
  
  while (Serial.available()) {
    byte value = Serial.read();
    
    if (value != 254) {
      input[inputIndex] = value;
      ++inputIndex;
      
      if (inputIndex == 5) {
        handleInput();  
      }
    }
  }  
}
