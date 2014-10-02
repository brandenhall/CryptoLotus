#include <JeeLib.h>

#define BAND RF12_915MHZ // wireless frequency band
#define GROUP 4     // wireless net group
#define SENSOR_POLL_RATE 30
#define STEP_DELTA 200

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
        for (word j = 0; j < intensity; ++j)
            slots[j] |= mask;
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


// calibrate the off state of the step sensor
void calibrateUp(void) {
  int total = 0;
  
  for (byte i=0; i<100; ++i) {
    total += analogRead(2);
    delay(30);
  }
  
  stepThreshold = (int)((total / 100.0)) + STEP_DELTA;
  
  Serial.println(stepThreshold);
  
  green();
  
  mode = calibrateDown;
  
  Serial.println("WAIT FOR STEP");
}

void calibrateDown(void) {  
  if (timer.poll(30)) {
    
    
    if (analogRead(2) > stepThreshold) {
      white();
      
      while (analogRead(2) > stepThreshold) {
        delay(30);  
      }
      
      black();
      
      mode = play;
    }
  }
}

void play() {  
    if (timer.poll(SENSOR_POLL_RATE)) {
      
      int sensor = analogRead(2);
      
      if (!active && sensor > stepThreshold) {
        active = true;
        state[2] = 1;
        white();
        
      } else if (active && sensor < stepThreshold) {
        active = false;
        state[2] = 0;
        
        black();
      }       
    }
    
    if (rf12_recvDone()
        && rf12_crc == 0
        && RF12_WANTS_ACK
        && rf12_len == 3) {
          
 //     PORTC &= 0xF0;
 //     PORTD &= 0x0F;

      if (rf12_data[0] != color[0] || rf12_data[1] != color[1] || rf12_data[2] != color[2]) {
        memcpy(color, (void*) rf12_data, rf12_len);
        rf12_sendNow(RF12_ACK_REPLY, &state, sizeof state);
        prepareSlots();
      } else {
        rf12_sendNow(RF12_ACK_REPLY, &state, sizeof state);
      }
    }
    
    byte bits = slots[TCNT0];
    PORTC = (PORTC & 0xF0) | (bits & 0x0F);
    PORTD = (PORTD & 0x0F) | (bits & 0xF0);
}

void setup() {
  Serial.begin(57600);  
  Serial.println("Crypto Lotus Lily Pad v1.1");

  // setup the pins
  for (byte i = 0; i < 3; ++i) {
      PORTC &= ~ (masks[i] & 0x0F);   // turn AIO pin off
      DDRC |= masks[i] & 0x0F;        // make pin an output
      PORTD &= ~ (masks[i] & 0xF0);   // turn DIO pin off
      DDRD |= masks[i] & 0xF0;        // make pin an output
  }
  
  // read the node ID from pins
  pinMode(6, INPUT);
  pinMode(7, INPUT);
  pinMode(17, INPUT);
  
  nodeId = (digitalRead(6) | digitalRead(7) << 1 | digitalRead(17) << 2) + 1;

  Serial.print("Node ID: ");
  Serial.println(nodeId);
  
  delay(1000);
  
  for (byte i=0; i<nodeId; ++i) {
     white();
     delay(500);
     black();
     delay(250); 
  }
  
  delay(1000);
  
  state[0] = 0;
  state[1] = nodeId;
  
  rf12_initialize(nodeId, BAND, GROUP);
  
  yellow();
  delay(1000);
  cyan();
  delay(1000);
  magenta();
  delay(1000);
  red();
  
  mode = calibrateUp;
}

void loop() {
 mode(); 
}

