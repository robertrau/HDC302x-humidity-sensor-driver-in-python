################################################################
# Raspberry Pi Driver for Texas Instruments HDC302x
# From code by D. Alex Gray dalexgray@mac.com wrote for the HTU21D
# This requires the pigpio library
# Get pigpio at http://abyz.co.uk/rpi/pigpio/index.html
################################################################

import time
import pigpio
import math
from datetime import datetime
import sys

pi = pigpio.pi()

# HDC302x Address
addr = 0x44

# i2c bus, if you have a Raspberry Pi Rev A, change this to 0
bus = 1

# HDC302x Commands
TriggerOnDemandMode0 = [0x24, 0x00]
SoftReset = [0x30, 0xa2]

def HDC302xReset():
    try:
        handle = pi.i2c_open(bus, addr) # open i2c bus
    except:
        print(f"ERROR - You must run 'sudo pigpiod' first")
        sys.exit(-100)
    pi.i2c_write_device(handle, SoftReset) # send reset command
    pi.i2c_close(handle) # close i2c bus
    time.sleep(0.4) # 


def HDC302xRead():
    handle = pi.i2c_open(bus, addr) # open i2c bus
    pi.i2c_write_device(handle, TriggerOnDemandMode0) # send read  command
    time.sleep(0.40) # readings take up to 15ms
    (count, HDC302xTandHArray) = pi.i2c_read_device(handle, 6) # collect temperatue, humidity with the CRC bytes
    pi.i2c_close(handle) # close the i2c bus
    
    # read array
    TemperatureMSB = HDC302xTandHArray[0]
    TemperatureLSB = HDC302xTandHArray[1]
    HumidityMSB = HDC302xTandHArray[3]
    HumidityLSB = HDC302xTandHArray[4]
    
    # Humidity
    HumidityDEC = (HumidityMSB << 8) + HumidityLSB
    HumidityPercent = ((float(HumidityDEC) / 65535) * 100)
    
    # Temperature
    TemperatureDEC = (TemperatureMSB << 8) + TemperatureLSB
    TemperatureCelcius = ((float(TemperatureDEC) / 65535) * 175) -45
    return TemperatureCelcius, HumidityPercent
    

HDC302xReset()
Now = datetime.now()
Date = Now.strftime("%m/%d/%Y")
Time = Now.strftime("%H:%M:%S")

print(Date, Time, HDC302xRead())