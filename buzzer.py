# This program sends a signal to the buzzer (3 pronged passive)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
 
 
# Using GPIO 20 as the signal pin
# The Left and center pins are Ground and +ve respectively

GPIO_PIN = 20
GPIO.setup(GPIO_PIN, GPIO.OUT)
 
# Set the frequency in Hz of the output pin
Freq = 500 #In Hertz
pwm = GPIO.PWM(GPIO_PIN, Freq)
pwm.start(50)

#print ("Please press enter" ,input())
 
# Unless there's a keyboard interrupt -send the signal to the buzzer 
try:
        while True:
                print ("----------------------------------------")
                print ("Aktuelle Frequenz: %d", Freq)
                Freq = input("Enter a Frequency between (50 -5000):")
                Freq = float(Freq)
                pwm.ChangeFrequency(Freq)
                 
        # Stop when ^C or Esc keys are pressed
except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()
