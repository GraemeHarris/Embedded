#DDXIRS001 - Irshaad Dodia
#
#EEE3096S - Embedded Systems II
#Prac 04 - SPI and Interrupts



#!/usr/bin/python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)    #Pin Numbering

#Setting Pin Numbers
Sw1 = 23 #Orange 
Sw2 = 24 #Blue
Sw3 = 25 #Green
Sw4 = 17 #Yellow


#Setting GPIO I/O 
GPIO.setup(Sw1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Sw2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Sw3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Sw4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)




def reset_cb(channel): #When Switch 1 is triggered
        
    print("Switch 1 pressed")
            
def freq_cb(channel): #when Switch 2 is triggered
    
    print("Switch 2 pressed")
        
def stop_cb(channel): #when Switch 3 is triggered
        
    print("Switch 3 pressed")
    
def exit_cb(channel): #when Switch 4 is triggered
        
    print("Switch 4 pressed")
    GPIO.cleanup()
            

    
GPIO.add_event_detect(Sw1, GPIO.FALLING, callback=reset_cb, bouncetime=300)
GPIO.add_event_detect(Sw2, GPIO.FALLING, callback=freq_cb, bouncetime=300)
GPIO.add_event_detect(Sw3, GPIO.FALLING, callback=stop_cb, bouncetime=300)
GPIO.add_event_detect(Sw4, GPIO.FALLING, callback=exit_cb, bouncetime=300)