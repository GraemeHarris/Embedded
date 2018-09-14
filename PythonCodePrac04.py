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
import collections

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
freq_count=0
freq=0.5
pot=0
stop=False
readings = collections.deque(maxlen=5)

def reset_cb(channel): #When Switch 1 is triggered
    global timer
    #reset timer
    timer = datetime.datetime(1999,12,31,0,0,0)
    #Clears the terminal, everything else is a dirty hack
    print("\033[H\033[J")
            
def freq_cb(channel): #when Switch 2 is triggered
    global freq_count
    global freq
    
    freq_count=freq_count+1
    if(freq_count<=2):
        if(freq_count==0):
            freq=0.5
        elif(freq_count==1):
            freq=1
        else:
            freq=2
    else:
        freq=0.5
        freq_count=0
        
def stop_cb(channel): #when Switch 3 is triggered
    global stop
    stop=~stop
    
def disp_cb(channel): #when Switch 4 is triggered
    print("TIME    ", "TIMER\t", "  POT\t", " TEMP\t", "LIGHT\t");
    for r in readings:
        print(r)
        print('------------------------------------')
    
def pot2volt(pot):
    return (pot/1023)*3.3

def volt2temp(temp):
    #Ambient voltage at 0 degree celsius
    v_0deg=0.5
    #0.1 is the mv/degree celsius of temp sensor
    return (((temp/1023)*3.3)-0.5)/0.01

def light2pcnt(light):
    return(light/857)*100

GPIO.add_event_detect(Sw1, GPIO.FALLING, callback=reset_cb, bouncetime=300)
GPIO.add_event_detect(Sw2, GPIO.FALLING, callback=freq_cb, bouncetime=300)
GPIO.add_event_detect(Sw3, GPIO.FALLING, callback=stop_cb, bouncetime=300)
GPIO.add_event_detect(Sw4, GPIO.FALLING, callback=disp_cb, bouncetime=300)

print("TIME    ", "TIMER\t", "  POT\t", " TEMP\t", "LIGHT\t");
print('------------------------------------')
while True:
    for i in range(8):
        values[i] = mcp.read_adc(i)
        # delay for a half second
        current_time=strftime("%H:%M:%S", gmtime())
    
    pot='{0:.2g}V'.format(pot2volt(values[0]))
    temp=' {0:.2g}C'.format(volt2temp(values[2]))
    light='  {0:.2g}%'.format(light2pcnt(values[1]))
        
    timer=timer+datetime.timedelta(0,freq)
    time.sleep(freq)
    
    if(~stop):
        print(current_time, str(timer.strftime("%H:%M:%S")), pot,temp,light)
        print('------------------------------------')
    else:
        readings.append(""+current_time + " " + str(timer.strftime("%H:%M:%S"))+ " " + pot+ " " + temp+ " " + light)

