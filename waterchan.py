from machine import Pin, ADC
import time

# 3700 = 100% dry
# 3100 = really dry dirt
# 2900 = as dry as you really want it
# 2000 = optimal, partway in dirt
# 1800 = optimal if 100% in
# 1420 = 100% water
SENSOR_WATER_START = 2600
SENSOR_WATER_STOP  = 2000
SENSOR_WAIT_TIME   = 300

PUMP_WATER_TIME = 1

LAST_WATERED = time.time()
'''
* How much water does the pump pump in 10s
* How much water changes the sensor amount by how much
'''

# Setup Sensor
# ADC setup: https://docs.micropython.org/en/latest/esp32/quickref.html#adc-analog-to-digital-conversion
# GPIO Pins: https://i2.wp.com/randomnerdtutorials.com/wp-content/uploads/2018/08/ESP32-DOIT-DEVKIT-V1-Board-Pinout-36-GPIOs-updated.jpg?ssl=1
# https://randomnerdtutorials.com/esp32-pinout-reference-gpios/
adc = ADC(Pin(32))
adc.atten(ADC.ATTN_11DB) 


# Main Program
def main():
    while True:
        current_moisture = adc.read()
        if current_moisture > SENSOR_WATER_START:
            water_plant()
        time.sleep(SENSOR_WAIT_TIME)

        '''
        wetness = Pin(15, Pin.IN).value()
        print(wetness)
        # Turn LED on
        Pin(2, Pin.OUT).value(1)
        time.sleep(1)
        # Turn LED off
        Pin(2, Pin.OUT).value(0)
        time.sleep(1)
        '''

def water_plant():
    current_moisture = adc.read()
    # Stop when it's too while
    while current_moisture > SENSOR_WATER_STOP:
        # run pump for PUMP_WATER_TIME
        time.sleep(SENSOR_WAIT_TIME)
        current_moisture = adc.read()
        

# If water sensor is broken, don't overwater the plants
def overwater_check():
    # don't water more than X seconds per Y days
    pass

# If water sensor is broken, don't underwater
def underwater_check():
    # if not watered for Y days, then water for X seconds
    pass

# Try to send an alert if sensor is broken
def sensor_alert():
    pass

if __name__ == '__main__':
    main()

'''
X Set Pump time
X Initialize the Sensor

Track last watered
Track how many seconds watered in a time period

X while True:
  X Check if sensor if it's too dry
  X If too dry, then turn on the pump
  X sleep
  

Don't overwater:

Don't underwater:
  last_watered > 4 days, then water for 40s = mL
'''


# Keep doing this
while True:
    # Turn LED on
    Pin(2, Pin.OUT).value(1)
    time.sleep(1)
    # Turn LED off
    Pin(2, Pin.OUT).value(0)
    time.sleep(1)
