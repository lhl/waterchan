from machine import Pin
import time

# Keep doing this
while True:
    # Turn LED on
    Pin(2, Pin.OUT).value(1)
    time.sleep(1)
    # Turn LED off
    Pin(2, Pin.OUT).value(0)
    time.sleep(1)