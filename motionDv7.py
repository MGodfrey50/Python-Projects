# This is the MAIN program, all sensor data feeds into this.

import RPi.GPIO as GPIO
import time
import sendit2
import datetime
import urllib.request

# GPIO Pins 
PIR_outside = 23                        # Outside motion detector GPIO pin #
PIR_inside = 18                         # Inside motion detector GPIO pin #
LED = 5
SecLight = 13
SIREN = 6
SecSiren =19

# Variables
pirState = False                        # we start, assuming no motion detected
pirVal = False                          # we start, assuming no motion detected
lightOnSecs = 10                        # set the seconds to 0 for the light and
sirenOnSecs = 5                         # siren run/on time
LED_RunTime =datetime.datetime.now()     # start time for LED to stay on
Siren_RunTime = datetime.datetime.now()  # start time for Siren to stay on

# GPIO Configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)                  # Broadcomm board configuration
GPIO.setup(PIR_outside, GPIO.IN)        # Listen for input on PIR-outside (pin 23)
GPIO.setup(PIR_inside, GPIO.IN)         # Listen for input on PIR-inside (pin 18)

GPIO.setup(LED, GPIO.OUT)               # Send out signal (turn on LED on pin 6)
GPIO.output(LED,False)                  # Force the LED off (just in case)
GPIO.setup(SIREN, GPIO.OUT)             # Send out signal (turn on SIREN LED on pin 6)
GPIO.output(SIREN, False)               # Siren LED off (just in case too)

GPIO.setup(SecLight, GPIO.OUT)          # Send out signal for security light (relay on pin 13)
GPIO.output(SecLight, GPIO.HIGH)        # Set relay signal high (relay goes on when output = low)
GPIO.setup(SecSiren, GPIO.OUT)
GPIO.output(SecSiren, GPIO.HIGH)         # Set relay signal high (relay goes on when output = low)


#GPIO.output(SIREN, GPIO.HIGH)           # Force the LED off (just in case)


def Trigger (PIR, Alarm, msg):                                                          # Trigger checks to see if the motion detector
    if GPIO.input(PIR):                                                                 # is detecting motion (if signal is high/true)
        if connected():                                                                 # Checks there is an Internet connection
             sendit2.sendEmail(msg)                                                     # then sends an email alert, then turns on
        else:
            print ("No Internet Connection - data written to log")                      # or writes the event to the log file (pending)
            
        Sec_Options(Alarm)                                                              # either the security light, or sounds the alarm
        time.sleep(5)                                                                   # allow enough time to reset sensor (avoid sending multiple emails)
    else:                                                                               # depending on which motion detector was triggered                         
        pass
    return 


def Sec_Options(whichAlarm):                                                            # Sec_Options is used to turn on the LED light
    global LED_RunTime, Siren_RunTime
    if whichAlarm == 5:                                                                 # Outside motion detector is triggered
        GPIO.output(whichAlarm, True)                                                   # Turn on LED light
        GPIO.output(SecLight, GPIO.LOW)
        LED_RunTime =datetime.datetime.now()+datetime.timedelta(0,lightOnSecs)
        
    elif whichAlarm ==6:                                                                # Inside motion detector is triggered
        GPIO.output(whichAlarm, True)
        GPIO.output(SecSiren, GPIO.LOW)
        Siren_RunTime =datetime.datetime.now()+datetime.timedelta(0,sirenOnSecs)
    elif whichAlarm ==7:                                                                # Laser beam is broken
        print ("whichAlarm= ",whichAlarm)
    else:
        pass
    return 


def Stay_On():                                                                          # Checks if current time is > LED_RunTime.  If it is it
    global LED_RunTime, Siren_RunTime                                                   # then it will turn off the light.  Not the light is
    # print ("LED_RunTime: ",LED_RunTime)                                               # Note that LED_RunTime will reset as long as the PIR
    # print ("Datetime: ",datetime.datetime.now())                                      # State is high, so light will not go off after 35 secs
    if datetime.datetime.now() < LED_RunTime:                                           # if movement continues.
       time.sleep(1)
       # pass                                                                           # Should pass parameters to this so that I can reuse
    else:                                                                               # this module for other time based events.
        print ("Turn off the light")
        GPIO.output(LED,False)
        GPIO.output(SecLight, GPIO.HIGH)
        input ("Turn off the LED on board")

    if datetime.datetime.now() < Siren_RunTime:                                         # if movement continues.
       time.sleep(1)
       # pass                                                                           # Should pass parameters to this so that I can reuse
    else:                                                                               # this module for other time based events.
        print ("Turn off the siren")
        GPIO.output(SIREN, False)
        GPIO.output(SecSiren,GPIO.HIGH)
    return

def connected(host='https://www.google.com'):                                           # checks that the program can connect to google.com
    try:                                                                                # in this case, used with sendit2.py - will only run
        urllib.request.urlopen(host)                                                    # if the connection is made, otherwise won't run.
        return True
    except:
        return False 

try:
    while True:
       Trigger (PIR_outside, LED, "Outside")                                            # Send the GPIO port, the light GPIO port, and the location
       Trigger (PIR_inside, SIREN, "Inside")                                            # then just wait a second. (prob don't need delay)
       time.sleep(1)                                                                    # Checks to see if runtime has been updated, if it has 
       Stay_On ()                                                                       # then the light will have been turned on and will stay on
                                                                                        # until the current time is > than the runtime
except KeyboardInterrupt:
       GPIO.cleanup()



