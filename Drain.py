import RPi.GPIO as GPIO
from time import sleep
from Tkinter import *
import math
import time
import numpy as np
import spidev
from datetime import datetime, timedelta
import sys

#Setting up Spi to read ADC
spi_0 = spidev.SpiDev()
spi_0.open(0, 0)

#Setting up Global Variables
ForwardPumpTarget=15
ForwardFlowCount = 0.0
oldForwardFlowCount= 0.0
BackwashPumpTarget=30
BackwashFlowCount = 0.0
oldBackwashFlowCount= 0.0
StartTime = datetime.now()
samplePeriod = 100

#setting up GPIO pins
ForwardTankValve = 14
ForwardPump = 15
BackwashPump = 18
ForwardPumpValve = 23
BackwashTankValve = 24
BackwashPumpValve = 25                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
ForwardFlow = 22
BackwashFlow = 17

on = GPIO.LOW
off = GPIO.HIGH
vopen = GPIO.LOW
vclose = GPIO.HIGH

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ForwardTankValve, GPIO.OUT)
GPIO.setup(ForwardPumpValve, GPIO.OUT)
GPIO.setup(ForwardPump, GPIO.OUT)
GPIO.setup(BackwashTankValve, GPIO.OUT)
GPIO.setup(BackwashPumpValve, GPIO.OUT)
GPIO.setup(BackwashPump, GPIO.OUT)
GPIO.setup(ForwardFlow, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BackwashFlow, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#----------------------Function Definitons--------------------------------

def readadc_0(adcnum_0): #this fucntion can be used to find out the ADC value on ADC 0
    if adcnum_0 > 7 or adcnum_0 < 0:
        return -1
    r_0 = spi_0.xfer2([1, 8 + adcnum_0 << 4, 0]) #start bit, Single/Differential mode, Don't care bit OR
    adcout_0 = ((r_0[1] & 3) << 8) + r_0[2]
    return adcout_0


GPIO.output(ForwardTankValve, vopen)
GPIO.output(BackwashPumpValve, vopen)
GPIO.output(ForwardPumpValve, vopen)
GPIO.output(BackwashTankValve, vopen)

time.sleep(15)

GPIO.output(ForwardTankValve, vclose)
GPIO.output(BackwashPumpValve, vclose)
GPIO.output(ForwardPumpValve, vclose)
GPIO.output(BackwashTankValve, vclose)

