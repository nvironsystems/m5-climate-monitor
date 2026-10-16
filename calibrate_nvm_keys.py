from machine import I2C, Pin

# Adjust these pins to match your specific Cardputer setup
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
BME688_ADDR = 0x77 # Or 0x76

def print_sensor_identity():
    # Burst read 25 bytes starting at 0x89
    # This block contains T1-T3, P1-P9, and H1-H2
    try:
        data = i2c.readfrom_mem(BME688_ADDR, 0x89, 25)
        print("Raw Calibration Data (25 bytes):")
        print(list(data))
        print("\nCopy this list into your main script to hard-code your sensor's identity.")
    except Exception as e:
        print("Could not read from sensor. Check your I2C address and wiring.")

print_sensor_identity()