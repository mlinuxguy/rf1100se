/* Markham Thomas  Feb 12th, 2017
 *  rf1101se (TI cc1101 based), created to match my pyrf1101se.py code
 *  and allow battery powered distance testing to a RPI or Odroid-C1 base station
 *  I wrote this (along with the Odroid-c1 companion (in python) because examples I found
 *  all prevented me from using an I2C OLED with their SPI implementation using a CC1100
 *  
 *  Uses 7 wires
    MOSI: 11,     MISO: 12
    CSN:  10,      SCK: 13
    GDO0:  2,      GND
    VCC

    This is a beacon display program that uses a 128x32 OLED to show RSSI and the beacon number
    It uses a momentary pushbutton to show values on the OLED to prevent burn-in
    The program expects the Odroid-c1 or RPI basestation to send a number that increments every 5 seconds
    and will display the RSSI value along with the current beacon number on the OLED.
 */
#include <avr/pgmspace.h>
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// #define DEBUG          // uncomment if you want serial.println() debug info

#define OLED_RESET 4
Adafruit_SSD1306 display(OLED_RESET);

#if (SSD1306_LCDHEIGHT != 32)
#error("Height incorrect, please fix Adafruit_SSD1306.h!");
#endif

const uint8_t msk_433_250k_config_regs[23] PROGMEM = {0x02,0x08,0x0A,0x0B,0x0D,0x0E,0x0F,0x10,0x11,0x12,0x15,0x18,0x19,0x1A,0x1B,0x1C,0x1D,0x21,0x23,0x24,0x25,0x26,0x2E};
const uint8_t msk_433_250k_config_vals[23] PROGMEM = {0x06,0x05,0x01,0x0A,0x10,0xB1,0x3B,0x2D,0x3B,0x73,0x00,0x18,0x1D,0x1C,0xC7,0x00,0xB0,0xB6,0xEA,0x2A,0x00,0x1F,0x09};
const uint8_t ask_433_250k_config_regs[24] PROGMEM = {0x02,0x08,0x0A,0x0B,0x0D,0x0E,0x0F,0x10,0x11,0x12,0x15,0x18,0x19,0x1A,0x1B,0x1C,0x1D,0x21,0x22,0x23,0x24,0x25,0x26,0x2E};
const uint8_t ask_433_250k_config_vals[24] PROGMEM = {0x06,0x05,0x01,0x0A,0x10,0xB1,0x3B,0x2D,0x3B,0x33,0x00,0x18,0x1D,0x1C,0xC7,0x00,0xB0,0xB6,0x11,0xEA,0x2A,0x00,0x1F,0x09};
const uint8_t gfs_433_250k_config_regs[23] PROGMEM = {0x02,0x08,0x0A,0x0B,0x0D,0x0E,0x0F,0x10,0x11,0x12,0x15,0x18,0x19,0x1A,0x1B,0x1C,0x1D,0x21,0x23,0x24,0x25,0x26,0x2E};
const uint8_t gfs_433_250k_config_vals[23] PROGMEM = {0x06,0x05,0x01,0x0A,0x10,0xB1,0x3B,0x2D,0x3B,0x13,0x00,0x18,0x1D,0x1C,0xC7,0x00,0xB0,0xB6,0xEA,0x2A,0x00,0x1F,0x09};
const uint8_t fs2_433_250k_config_regs[23] PROGMEM = {0x02,0x08,0x0A,0x0B,0x0D,0x0E,0x0F,0x10,0x11,0x12,0x15,0x18,0x19,0x1A,0x1B,0x1C,0x1D,0x21,0x23,0x24,0x25,0x26,0x2E};
const uint8_t fs2_433_250k_config_vals[23] PROGMEM = {0x06,0x05,0x01,0x0A,0x10,0xB1,0x3B,0x2D,0x3B,0x03,0x00,0x18,0x1D,0x1C,0xC7,0x00,0xB0,0xB6,0xEA,0x2A,0x00,0x1F,0x09};

const int cc1100_csn_pin = 10;
const int cc1100_rdy_pin = 2;
const int cc1100_miso_pin = 12;
const int cc1100_mosi_pin = 11;
const int pushbutton_line1 = 8;
const int pushbutton_line2 = 9;

#define BUFFER_SIZE         128   // keep this small since an arduino mini doesn't have much ram

#define SYNC1               0x04
#define SYNC0               0x05
#define WRITE_SINGLE_BYTE   0x00
#define WRITE_BURST         0x40
#define READ_SINGLE_BYTE    0x80
#define READ_BURST          0xc0
#define SRES                0x30
#define SFTX                0x3b
#define SFRX                0x3a
#define SRX                 0x34
#define STX                 0x35
#define SIDLE               0x36
#define PARTNUM             0xF0
#define VERSION             0xF1
#define LQI                 0xF3
#define RSSIV               0xF4
#define MARCSTATE           0xF5
#define TXBYTES             0xFA
#define RXBYTES             0xFB
#define TXFIFO_BURST        0x7F
#define RXFIFO_SINGLE_BYTE  0xBF
#define ADDR                0x09
#define CHANNR              0x0A
#define PKTCTRL0            0x08
#define PKTCTRL1            0x07

#define SYNCWORD            0xEEEE

uint8_t rxbuf[BUFFER_SIZE];   // receive buffer
//uint8_t txbuf[BUFFER_SIZE];

// PORTB maps to Arduino digital pins 8 to 13 The two high bits (6 & 7) map to the crystal pins and not usable
#define PORT_SPI_MISO   PINB
#define BIT_SPI_MISO    5           // pin 12 (MISO) should be bit 5
// Wait until SPI MISO line goes low
// When CSn is pulled low, the MCU must wait until CC1101 SO pin goes low before starting to transfer the header byte. 
#define wait_miso()  while(bitRead(PORT_SPI_MISO, BIT_SPI_MISO))

void reset_cc1100(void) {
  digitalWrite(cc1100_csn_pin, LOW);
  wait_miso();
  SPI.transfer(SRES);   // reset cc1100 chip
  wait_miso();
  SPI.transfer(SFTX);   // flush TX FIFO
  delay(200);
  SPI.transfer(SFRX);   // flush RX FIFO
  delay(200);
  SPI.transfer(SRX);    // enter RX mode
  delay(500);
  digitalWrite(cc1100_csn_pin, HIGH);
}

// read froma single register, OR the cc1100 read value with register
uint8_t readRegister(byte reg) {
  uint8_t result;
  digitalWrite(cc1100_csn_pin, LOW);
  wait_miso();
  SPI.transfer(reg | READ_SINGLE_BYTE);
  result = SPI.transfer(0x00);  // send value of 0 to read first byte
  digitalWrite(cc1100_csn_pin, HIGH);
  return (result);
}

// write to a single register, no need to OR bits since we'd be OR'ing zero
void writeRegister(byte reg, byte val) {
  digitalWrite(cc1100_csn_pin, LOW);
  wait_miso();
  SPI.transfer(reg);    // register that we are going to write to
  SPI.transfer(val);    // send the value to the register
  delay(10);
  digitalWrite(cc1100_csn_pin, HIGH);
}

// write a burst of data to TX FIFO
void cc1100_loadtx(uint8_t * buff, byte len) {
  uint8_t x;
  digitalWrite(cc1100_csn_pin, LOW);
  wait_miso();
  SPI.transfer(TXFIFO_BURST | WRITE_BURST);    // register that we are going to write to
  for (x=0;x<len+1;x++) {
      SPI.transfer(buff[x]);    // transfer the data
  }
  digitalWrite(cc1100_csn_pin, HIGH);
}

// set the word that is being used for syncing the packet
void set_syncword(word syncword) {
  byte sval;
  sval = (syncword & 0xff00) >> 8;
  writeRegister(SYNC1, sval);     // sync1 is high byte of syncword
  sval = syncword & 0x00ff;
  writeRegister(SYNC0, sval);
}

// compute RSSI DBM
int compute_rssi_dbm(uint8_t x) {
  int y;
  if (x >= 128) y = (x - 256) / 2 - 74;
  else 
  if (x < 128)  y = (x/2) - 74;
  return (y);
}

// get the received signal strength value
uint8_t check_rssi(void) {
  byte x;
  int rssiv = 0xff;
  x = readRegister(RSSIV);
  rssiv = compute_rssi_dbm(x);
  return (rssiv);
}

// return the bytes in the RXFIFO
uint8_t bytes_in_rx(void) {
  uint8_t byte_count;
  byte_count = readRegister(RXBYTES);
  return (byte_count);
}

// if any bytes in RX FIFO return the data
uint8_t read_rx_fifo(uint8_t *buf) {
  uint8_t cnt, x;
  cnt = bytes_in_rx();
  if ((cnt != 0) && (cnt < BUFFER_SIZE)) {
    for (x = 0; x < cnt; x++) {
      rxbuf[x] = readRegister(RXFIFO_SINGLE_BYTE);
    }
  }
  return (cnt);
}

// dump config register values, pass in length since can't determine that inside a function
void dump_config_registers(const uint8_t *Regs, uint8_t len) {
  uint8_t regs, vals;
  int x,y;
  for (y = 0; y < len; y++) {
    regs = pgm_read_byte_near(Regs + y);
    Serial.print(regs,HEX);
    Serial.print(":");
    vals = readRegister(regs);
    Serial.print(vals,HEX);
    Serial.print(", ");
  }
  Serial.println();
}

// packet control
void set_packet_ctrl1(uint8_t val) {
  writeRegister(PKTCTRL1, val);
}

void set_packet_ctrl0(uint8_t val) {
  writeRegister(PKTCTRL0, val);
}

// set the cc1100 into IDLE mode
void cc1100_idle(void) {
  byte marc_reg, marc_state = 0xff;
  digitalWrite(cc1100_csn_pin, LOW);
  wait_miso();
  SPI.transfer(SIDLE);    // command strobe to request idle state
  digitalWrite(cc1100_csn_pin, HIGH);
  marc_reg = MARCSTATE | READ_SINGLE_BYTE;
  while (marc_state != 0x01) {
    marc_state = readRegister(marc_reg) & 0x1f;
  }
}

// set the cc1100 into receive mode
void cc1100_receive(void) {
  byte marc_reg, marc_state = 0xff;
  cc1100_idle();
  digitalWrite(cc1100_csn_pin, LOW);
  wait_miso();
  SPI.transfer(SRX);    // command strobe to request RX mode
  digitalWrite(cc1100_csn_pin, HIGH);
  marc_reg = MARCSTATE | READ_SINGLE_BYTE;
  while (marc_state != 0x0d) {
    marc_state = readRegister(marc_reg) & 0x1f;
  }
}

// set the cc1100 into transmit mode, need TX buffer pre-loaded before calling
void cc1100_transmit(void) {
  byte marc_reg, marc_state = 0xff;
  cc1100_idle();
  digitalWrite(cc1100_csn_pin, LOW);
  wait_miso();
  SPI.transfer(STX);    // command strobe to request TX mode
  digitalWrite(cc1100_csn_pin, HIGH);
  marc_reg = MARCSTATE | READ_SINGLE_BYTE;
  while (marc_state != 0x01) {    // bugfix, its not 0x13 but 0x01 to wait for
    marc_state = readRegister(marc_reg) & 0x1f;
  }
}

// sets device address (for filtration) and channel number
void device_address_and_channel(byte addr, byte chann) {
  writeRegister(ADDR, addr);
  writeRegister(CHANNR, chann);
}

// write the values in the array we've selected to the cc1100 config register
void cc1100_setup(const uint8_t *Regs, const uint8_t *Vals, uint8_t len) {
  uint8_t regs, vals;
  int x,y,z;
  for (y = 0; y < len; y++) {
    regs = pgm_read_byte_near(Regs + y);
    vals = pgm_read_byte_near(Vals + y);
    writeRegister(regs,vals);
  }
#ifdef DEBUG
  x = readRegister(PARTNUM);
  Serial.print("Part: ");
  Serial.println(x,HEX);
  x = readRegister(VERSION);
  Serial.print("Version: ");
  Serial.println(x,HEX);
#endif
}

void setup() {
  int x,y,z;
  Serial.begin (9600);
  SPI.begin();
  SPI.beginTransaction (SPISettings (500000, MSBFIRST, SPI_MODE0));  // 2 MHz clock, MSB first, mode 0
  //SPI.begin();
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // initialize with the I2C addr 0x3C (for the 128x32)
  display.display();
  delay(2);
  // Clear the buffer.
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.println("RSSI: ");
  display.display();

  memset(rxbuf,0,sizeof(rxbuf));     // zero out receive buffer
  pinMode(cc1100_rdy_pin, INPUT);
  pinMode(cc1100_csn_pin, OUTPUT);
  pinMode(pushbutton_line1, INPUT_PULLUP);  // float this line high
  pinMode(pushbutton_line2, OUTPUT);        // let this line provide gnd
  digitalWrite(pushbutton_line2, 0);
  reset_cc1100();
  cc1100_setup(msk_433_250k_config_regs, msk_433_250k_config_vals, sizeof(msk_433_250k_config_regs)); 
  device_address_and_channel(0x02, 0x01);
//  set_syncword(SYNCWORD);   // setting this breaks TX/RX, need to investigate why
  set_packet_ctrl1(0x07);     // append 2 status bytes (RSSI+LQI)
  set_packet_ctrl0(0x45);     // variable packet length
//  dump_config_registers(msk_433_250k_config_regs, sizeof(msk_433_250k_config_regs));
}

// globals for the loop() section of code
int rssival = 0;
bool oled_display = true;         // turn display on or off
int button_state = HIGH;          // track state of button
long last_debounce_time = 0;      // previous time output changed
long debounce_delay = 500;        // debounce time
String beacon = " ";
  
// This is the beacon receive loop
void loop() {
  uint8_t count = 0;
  cc1100_receive();
  count = read_rx_fifo(rxbuf);
  if (count > 0) {
    rssival = rxbuf[count-2];
    rssival = compute_rssi_dbm(rssival);
#ifdef DEBUG
    Serial.print("Cnt: ");
    Serial.println(count);
    Serial.print("rssi: ");
    Serial.println(rssival);
    Serial.print("LQI: ");
    Serial.println(rxbuf[count-1] & 0x7f);   
    String str = (char *)rxbuf;
    Serial.println(str.substring(2,count-2));  // strip off address(start byte) and the ending RSSI+LQI bytes
    Serial.println();
#endif
  }
  // button debounce section to turn OLED on and off
  button_state = digitalRead(pushbutton_line1);
  if ((millis() - last_debounce_time) > debounce_delay) {
    if ( (button_state == LOW) && (oled_display)) {
      oled_display = !oled_display;     // toggle OLED display on and off
      last_debounce_time = millis();    //set the current time
    } else 
    if ( (button_state == LOW) && (!oled_display)) {
      oled_display = !oled_display;     // toggle OLED display on and off
      last_debounce_time = millis(); //set the current time
    }
  }
  if ((oled_display)) {
    String str = (char *)rxbuf;
    if (count > 0) beacon = str.substring(2,count-2);
    display.clearDisplay();
    display.setCursor(0,0);
    display.println("RSSI:");
    display.setCursor(80,0);
    display.println(rssival);
    display.setCursor(0,17);
    display.println(beacon);
    display.display();
  } else {   // Turn the OLED display off
    display.clearDisplay();
    display.display();
  }
}
