#include <JeeLib.h>

#define BAND RF12_915MHZ // wireless frequency band
#define GROUP 4     // wireless net group
#define DEFAULT_NODE_ID 2   // default node id until it's been set
#define STEP_DELTA 100
#define SENSOR_POLL_RATE 100
#define DATA_POLL_RATE 10

// mode pointer
void (*mode)();

// color we should be showing
static byte color[3];

boolean active = true;
byte nodeId;

// time based slots for doing software PWM for RGB LEDs
static byte slots[256];

MilliTimer timer;

int stepThreshold;

byte state[3];

// register masks for the LED strip
static const byte masks[3] = { 0x10, 0x01, 0x20};

static void prepareSlots() {
    // fill the slots arrray with on-bits, as implied by the intensity values
    memset(slots, 0, sizeof slots);
    for (byte i = 0; i < 3; ++i) {
        // get the requested PWM level
        word intensity = color[i];
        // don't use intensities 1 and 254, as they would toggle within 4 us
        // convert 0..255 values to 0 = off, 2..254 = dimmed, 256 = on
        if (intensity > 0) ++intensity;     // change 1..255 to 2..256
 //       if (intensity == 255) ++intensity;  // change (original) 254 to 256
        // fill in the 1's
        byte mask = masks[i]; // map setting to corresponding I/O pin
        for (word i = 0; i < intensity; ++i)
            slots[i] |= mask;
    }
}

void red() {
  byte bits = 0;
  bits |= masks[0];
  PORTC = (PORTC & 0xF0) | (bits & 0x0F);
  PORTD = (PORTD & 0x0F) | (bits & 0xF0); 
}

void green() {
  byte bits = 0;
  bits |= masks[1];
  PORTC = (PORTC & 0xF0) | (bits & 0x0F);
  PORTD = (PORTD & 0x0F) | (bits & 0xF0); 
}

void blue() {
  byte bits = 0;
  bits |= masks[2];
  PORTC = (PORTC & 0xF0) | (bits & 0x0F);
  PORTD = (PORTD & 0x0F) | (bits & 0xF0);  
}

void yellow() {
  byte bits = 0;
  bits |= masks[0] | masks[1];
  PORTC = (PORTC & 0xF0) | (bits & 0x0F);
  PORTD = (PORTD & 0x0F) | (bits & 0xF0);
}

void cyan() {
  byte bits = 0;
  bits |= masks[1] | masks[2];
  PORTC = (PORTC & 0xF0) | (bits & 0x0F);
  PORTD = (PORTD & 0x0F) | (bits & 0xF0);
}

void magenta() {
  byte bits = 0;
  bits |= masks[0] | masks[2];
  PORTC = (PORTC & 0xF0) | (bits & 0x0F);
  PORTD = (PORTD & 0x0F) | (bits & 0xF0);
}

void white() {
  byte bits = 0;
  bits |= masks[0] | masks[1] | masks[2];
  PORTC = (PORTC & 0xF0) | (bits & 0x0F);
  PORTD = (PORTD & 0x0F) | (bits & 0xF0); 
}

void black() {
  PORTC &= 0xF0;
  PORTD &= 0x0F;  
}



void waitForLotus(void) {  
  if (timer.poll(10)) {
    checkMessages();                         
  }  
}

void calibrate(void) {
  int total = 0;
  
  for (byte i=0; i<20; ++i) {
    total += analogRead(2);
    delay(100);
  }
  
  stepThreshold = (int)((total / 20.0)) + STEP_DELTA;
  
  blue();
  
  mode = waitForStep;
  
  Serial.println("WAIT FOR STEP");
}

void waitForStep(void) {  
  if (timer.poll(10)) {
    
    
    if (analogRead(2) > stepThreshold) {
      byte cmd[1];
      cmd[0] = 128;
    
      green();
      
      while (analogRead(2) > stepThreshold) {
        delay(100);  
      }
      
      black();
      
      while (!rf12_canSend()) {
        rf12_recvDone();
        delay(10);
      } 
      
      rf12_sendStart(RF12_HDR_DST | 1, &cmd, sizeof cmd);
      rf12_sendWait(0);
      
      mode = setupNetwork; 
      
      yellow();

    } else if(rf12_recvDone() && rf12_crc == 0 && rf12_hdr == (RF12_HDR_DST | nodeId)) {
      if (rf12_len == 4 && rf12_data[0] == 0 && rf12_data[1] == 0 && rf12_data[2] == 0 && rf12_data[3] == 0) {
        black();
        nodeId = DEFAULT_NODE_ID;
        rf12_initialize(nodeId, BAND, GROUP);
        white();
        mode = calibrate;
      }     
    }
  }
}

void setupNetwork(void) {
    if (timer.poll(10) && rf12_recvDone() && rf12_hdr == (RF12_HDR_DST | nodeId) && rf12_crc == 0) {
      
      if (rf12_data[0] == 129) {    
        nodeId = rf12_data[1];
        Serial.print("NODE ID ");
        Serial.println(nodeId);    
        state[0] = 2; // id for state messages
        state[1] = nodeId;
        state[2] = 0;
        active = false;
        rf12_initialize(nodeId, BAND, GROUP);
        black();
        
        for (int i=0; i < nodeId - 9; ++i) {
           white();
           delay(100);
           black();
           delay(500);
        }
        black();
        
        mode = play;
        
      } else if (rf12_len == 4 && rf12_data[0] == 0 && rf12_data[1] == 0 && rf12_data[2] == 0 && rf12_data[3] == 0) {
        black();
        nodeId = DEFAULT_NODE_ID;
        rf12_initialize(nodeId, BAND, GROUP);
        white();
        mode = calibrate;
      }     
    }
}

void checkMessages() {
  
  if (rf12_recvDone()) {
    Serial.println("GOT MESSAGE");
    
    Serial.println(rf12_hdr);
    Serial.println((RF12_HDR_DST | nodeId));
    Serial.println("---");
    
    if (rf12_hdr == (RF12_HDR_DST | nodeId)
      && rf12_crc == 0) {
      
      Serial.println("GOT MESSAGE");
      Serial.println(rf12_data[0]);
      
      // reset
      if (rf12_data[0] == 0 && rf12_data[1] == 0 && rf12_data[2] == 0 && rf12_data[3] == 0) {
        black();
        nodeId = DEFAULT_NODE_ID;
        rf12_initialize(nodeId, BAND, GROUP);
        white();
        mode = calibrate;        
        
      // set color 
      } else if (rf12_data[0] == 1) {
        Serial.println("GOT COLOR");
        // turn LEDs off before making changes
  //          PORTC &= 0xF0;
  //          PORTD &= 0x0F;
          yellow();
  //      color[0] = rf12_data[1];
  //      color[1] = rf12_data[2];
  //      color[2] = rf12_data[3];
  //      prepareSlots();
      }
    }
  }
}

void play() {
    if (timer.poll(DATA_POLL_RATE)) {
      checkMessages();
    }  
  
    if (timer.poll(SENSOR_POLL_RATE)) {
      
      int sensor = analogRead(2);
      
      if (!active && sensor > stepThreshold) {
        active = true;
        state[2] = 1;
        
        while (!rf12_canSend()) {
          checkMessages();
          delay(10);
        } 
        
        rf12_sendStart(RF12_HDR_DST | 1, &state, sizeof state);
        rf12_sendWait(0);
        
      } else if (active && sensor < stepThreshold) {
        active = false;
        state[2] = 0;
        
        while (!rf12_canSend()) {
          checkMessages();
          delay(10);
        } 
        
        rf12_sendStart(RF12_HDR_DST | 1, &state, sizeof state);
        rf12_sendWait(0);
      }       
    }
    
//    byte bits = slots[TCNT0];
    
//    PORTC = (PORTC & 0xF0) | (bits & 0x0F);
//    PORTD = (PORTD & 0x0F) | (bits & 0xF0);
}

void setup() {
  Serial.begin(57600);  
  Serial.println("Crypto Lotus Lily Pad v1.0");

  // setup the pins
  for (byte i = 0; i < 3; ++i) {
      PORTC &= ~ (masks[i] & 0x0F);   // turn AIO pin off
      DDRC |= masks[i] & 0x0F;        // make pin an output
      PORTD &= ~ (masks[i] & 0xF0);   // turn DIO pin off
      DDRD |= masks[i] & 0xF0;        // make pin an output
  }
  
  nodeId = DEFAULT_NODE_ID;
  yellow();
  delay(1000);
  cyan();
  delay(1000);
  magenta();
  delay(1000);
  red();
  
  mode = waitForLotus;
}

void loop() {
 mode(); 
}

