/*
  SDA -> A4
  SCL -> A5
*/

#include <Wire.h>
#include <BH1750.h>

BH1750 lightMeter(0x23);
uint16_t lux;

void setup() {
  Serial.begin(9600);
  lightMeter.begin(BH1750_CONTINUOUS_HIGH_RES_MODE);
}

void loop() {
  lux = lightMeter.readLightLevel();
  Serial.println(lux);
  delay(500);
}
