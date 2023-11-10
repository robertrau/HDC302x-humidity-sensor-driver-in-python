#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @mainpage MCP2221A interface to TI HDC302x humidity sensor
#
# on the command line, you must:
# pip3 install hidapi
# pip3 install adafruit-blinka
# export BLINKA_MCP2221="1"
#
# Stuff I read to help write this:
# https://learn.adafruit.com/circuitpython-libraries-on-any-computer-with-mcp2221
# https://learn.adafruit.com/circuitpython-libraries-on-any-computer-with-mcp2221/gpio
# see https://learn.adafruit.com/circuitpython-libraries-on-any-computer-with-mcp2221/i2c
# see: https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Jupyter_USB/PCT2075.ipynb
# more info found here   https://learn.adafruit.com/circuitpython-basics-i2c-and-spi?view=all
# from https://learn.adafruit.com/msa301-triple-axis-accelerometer/python-circuitpython#circuitpython-installation-of-msa301-library-6-7
# this stuff from https://github.com/adafruit/Adafruit_CircuitPython_VEML6070/blob/main/adafruit_veml6070.py
#
import time
import board
import digitalio
import busio
from adafruit_bus_device.i2c_device import I2CDevice
import math
from datetime import datetime
import sys


def HDC302xReset():
	i2c = busio.I2C(board.SCL, board.SDA)
	addr =  0x44
	SoftResetCmd = bytes([0x30, 0xa2])
	i2c.writeto(addr, SoftResetCmd)

	time.sleep(0.40) # readings take up to 15ms
			


def HDC302xRead():
	i2c = busio.I2C(board.SCL, board.SDA)
	addr =  0x44
	TriggerOnDemandMode0 = bytes([0x24, 0x00])
	HDC302xTandHArray = bytearray(6)
	i2c.writeto(addr, TriggerOnDemandMode0)

	time.sleep(0.40) # readings take up to 15ms
			
	buffer = bytearray(6)
	i2c.readfrom_into(addr, HDC302xTandHArray)
	#print (HDC302xTandHArray)

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

TemperatureCelcius, HumidityPercent = HDC302xRead()
print(f"{Date} {Time} Temperature={TemperatureCelcius: .2f}°C   Relitive humidity={HumidityPercent: .2f}%")