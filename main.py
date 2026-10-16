from machine import I2C, Pin
import time
import M5
from M5 import *

# 1. Hardware setup
backlight = Pin(38, Pin.OUT)
backlight.off() 
reset_pin = Pin(18, Pin.OUT)
reset_pin.off()
time.sleep(0.1)
reset_pin.on()
time.sleep(0.2)

# 2. Setup Display and I2C
Lcd.setRotation(1)
Lcd.clear(0x000000)
i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
backlight.on()

# Multiplexer selector function
def select_channel(channel):
    i2c.writeto(0x70, bytes([1 << channel]))

while True:
    try:
        # --- Get ENV Data (Channel 0) ---
        select_channel(0)
        i2c.writeto_mem(0x77, 0x74, b'\x21')
        time.sleep(0.1)
        data_env = i2c.readfrom_mem(0x77, 0x1D, 15)
        
        raw_p = (data_env[2] << 12) | (data_env[3] << 4) | (data_env[4] >> 4)
        raw_t = (data_env[5] << 12) | (data_env[6] << 4) | (data_env[7] >> 4)
        raw_g = (data_env[13] << 8) | data_env[14]

        # --- Get DLight Data (Channel 1) ---
        select_channel(1)
        i2c.writeto(0x23, b'\x10') 
        time.sleep(0.2)
        data_light = i2c.readfrom(0x23, 2)
        lux = (data_light[0] << 8) | data_light[1]
        
        # --- Update Display ---
        Lcd.clear(0x000000)
        Lcd.setCursor(10, 10)
        Lcd.print(f"Status: {hex(data_env[0])}")
        Lcd.setCursor(10, 30)
        Lcd.print(f"Temp:   {raw_t}")
        Lcd.setCursor(10, 50)
        Lcd.print(f"Press:  {raw_p}")
        Lcd.setCursor(10, 70)
        Lcd.print(f"Gas:    {raw_g}")
        Lcd.setCursor(10, 90)
        Lcd.print(f"Lux:    {lux}")
        
    except Exception as e:
        Lcd.clear(0x000000)
        Lcd.setCursor(10, 10)
        Lcd.print(f"Error: {str(e)}")
        
    time.sleep(2)