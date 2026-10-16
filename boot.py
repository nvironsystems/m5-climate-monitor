from machine import Pin
import time

# Pin 38 is the LCD Backlight - turn it off to hide the boot noise
backlight = Pin(38, Pin.OUT)
backlight.off()

# Force a hard reset of the display controller to clear noise
reset_pin = Pin(18, Pin.OUT)
reset_pin.off()
time.sleep(0.1)
reset_pin.on()