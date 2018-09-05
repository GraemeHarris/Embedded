#!/usr/bin/python -u
#DDXIRS001 - Irshaad Dodia
#HRRGRA004 - Graeme Harris
#EEE3096S - Embedded Systems II
#Prac 04 - SPI and Interrupts

import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import os
from time import gmtime, strftime
import sys
import datetime

GPIO.setmode(GPIO.BCM)    #Pin Numbering

#Setting Pin Numbers
Sw1 = 23 #Orange 
Sw2 = 24 #Blue
Sw3 = 25 #Green
Sw4 = 17 #Yellow

SPICLK = 11 #Purple
SPIMISO = 9 #Blue
SPIMOSI = 10 #Green
SPICS = 8 #Yellow

#Note:
#White = 3v3
#Red = 5v
#Black = GND

#Setting GPIO I/O 
GPIO.setup(Sw1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Sw2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Sw3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Sw4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)

# global variables
values = [0]*8
current_time=""
timer = datetime.datetime(1999,12,31,0,0,0)
freq=1
pot=0

def reset_cb(channel): #When Switch 1 is triggered
        
    print("Switch 1 pressed")
            
def freq_cb(channel): #when Switch 2 is triggered
    
    print("Switch 2 pressed")
        
def stop_cb(channel): #when Switch 3 is triggered
        
    print("Switch 3 pressed")
    
def exit_cb(channel): #when Switch 4 is triggered
        
    print("Switch 4 pressed")
    GPIO.cleanup()
    
def pot2volt(pot):
    return (pot/1023)*3.3

while True:
    
    for i in range(8):
        values[i] = mcp.read_adc(i)
        # delay for a half second
        current_time=strftime("%H:%M:%S", gmtime())
    
    pot=pot2volt(values[0])
    
    timer=timer+datetime.timedelta(0,freq)
    time.sleep(freq)
    
    print(values)
    print(pot)
    print(current_time)
    print(str(timer.strftime("%H:%M:%S")))
    
GPIO.add_event_detect(Sw1, GPIO.FALLING, callback=reset_cb, bouncetime=300)
GPIO.add_event_detect(Sw2, GPIO.FALLING, callback=freq_cb, bouncetime=300)
GPIO.add_event_detect(Sw3, GPIO.FALLING, callback=stop_cb, bouncetime=300)
GPIO.add_event_detect(Sw4, GPIO.FALLING, callback=exit_cb, bouncetime=300)