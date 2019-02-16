#!/usr/bin/python

import RPi.GPIO as GPIO
import smtplib
import picamera
import time
import urllib.request
from datetime import datetime

GPIO.setmode(GPIO.BCM)

Ch_MSensor =6
Ch_Buzzer = 12
Ch_Light = 16
current_state = 0
sleep_time= 4
camera = picamera.PiCamera()

GPIO.setup (Ch_MSensor,GPIO.IN)
GPIO.setup (Ch_Buzzer,GPIO.OUT)
GPIO.setup (Ch_Light, GPIO.OUT)

def sendEmail(message): 
    to = 'mgodfrey@live.com'    
    email_acct = 'alarm-alert@outlook.com'
    email_pwd = '1million!'
    smtpserver = smtplib.SMTP("smtp.live.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(email_acct, email_pwd)
    header = 'To:' + to + '\n' + 'From: ' + email_acct + '\n' + 'Subject:testing \n'
    print (header)
    when = str(datetime.now())[:-7]
    msg = header + '\n' + 'This is test msg triggered by a motion detector to ' + message + ' ' + when + ' \n\n'
    smtpserver.sendmail(email_acct, to, msg)
    print ('done!')
    smtpserver.close()
    return

def AlarmLight (OnOff):                                                               #Generic code to be used to activate anything
    print ("Light State", OnOff)
    GPIO.output(Ch_Light,OnOff)
    return

def Buzzer(buzzer_OnOff):                                                               #Generic code to be used to activate anything
    print ("Buzzer State", buzzer_OnOff)
    GPIO.output(Ch_Buzzer,buzzer_OnOff)
    return


def connected(host='https://www.google.com'):                                           # checks for a valid internet connection
    internetUp = urllib.request.urlopen(host).getcode()
    if internetUp == 200:                                                               #print ("Should be return code 200",internetUp)
        return True
    else:
        return False 

def photo():
    #camera.vflip = True
    camera.capture('example.jpg')

# MAIN BODY of the program

if __name__ == '__main__':
    try:
        while True:
            print ("Current State", current_state)                                          #print ("GPIO pin %s is %s" % (P_Sensor, current_state))
            if current_state ==1:
                AlarmLight(False)
                Buzzer(True)
                photo()
                time.sleep(4)                                                               #Allows time for the sensor to reset
                if connected():                                                             # Checks there is an Internet connection
                       sendEmail("Buzzer & Email")                                          # then sends an email alert, then turns on
                else:
                        print ("No Internet Connection - data written to log")              # or writes the event to the log file (pending)
            else:
                Buzzer(False)
                AlarmLight(True)

            time.sleep(0.1)
            current_state = GPIO.input(Ch_MSensor)
   
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

