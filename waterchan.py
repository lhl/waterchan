from   machine import Pin, ADC
import network
import urequests
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

PUMP_WATER_TIME = 60 # about 16-17ml in 60s with gauze

LAST_WATERED = time.time()

# Setup Sensor
# ADC setup: https://docs.micropython.org/en/latest/esp32/quickref.html#adc-analog-to-digital-conversion
# GPIO Pins: https://i2.wp.com/randomnerdtutorials.com/wp-content/uploads/2018/08/ESP32-DOIT-DEVKIT-V1-Board-Pinout-36-GPIOs-updated.jpg?ssl=1
# https://randomnerdtutorials.com/esp32-pinout-reference-gpios/
adc = ADC(Pin(32))
adc.atten(ADC.ATTN_11DB)

def blink(on, off=-1, times=1):
    i = 0
    if times > 1 and off == -1:
        off = on
    while i < times:
        Pin(2, Pin.OUT).value(1)
        time.sleep(on)
        Pin(2, Pin.OUT).value(0)
        if off > 0:
            time.sleep(off)
        i+=1

# 1s LED Boot
blink(1,1)

# Connect to Internet
sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
sta_if.active(True)
ap_if.active(False)
sta_if.connect('SSID', 'PSK')
# sta_if.isconnected()
# sta_if.ifconfig()
blink(0.5,0.5,3)

time.sleep(10)

# Main Program
def main():
    log('=== WATERCHAN ON! ===')
    while True:
        blink(0.5)
        current_moisture = adc.read()
        log(current_moisture)
        if current_moisture > SENSOR_WATER_START:
            water_plant()
        time.sleep(SENSOR_WAIT_TIME)


def log(log):
    print(log)
    log = str(log)
    if sta_if.isconnected():
        try:
            urequests.get('https://example.com/waterchan?log=' + log)
        except:
            print('ERROR: could not log')


def water_plant():
    log('START WATERING...')
    current_moisture = adc.read()
    # Stop when it's too while
    while current_moisture > SENSOR_WATER_STOP:
        # run pump for PUMP_WATER_TIME
        log('...pumping')
        Pin(26, Pin.OUT).value(1)
        time.sleep(PUMP_WATER_TIME)
        Pin(26, Pin.OUT).value(0)
        # wait for SENSOR_WAIT_TIME for moisture to diffuse
        time.sleep(SENSOR_WAIT_TIME)
        current_moisture = adc.read()
        log(current_moisture)
    log('DONE WATERING')


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
TODO
---
[] Don't overwater:

[] Don't underwater:
  last_watered > 4 days, then water for 40s = mL
'''
