# -*- coding: utf-8 -*-
import serial
import Adafruit_BBIO.UART as UART
from time import sleep

UART.setup("UART1")
GPS = serial.Serial('/dev/ttyO1', 9600)
isGPRMC=False
isGPGGA=False

#Poll for new GPA coordinates
def poll():
    global isGPRMC
    global isGPGGA
    
    while isGPRMC==False and isGPGGA==False:
        
        while GPS.inWaiting()==0:
                pass
        
        NMEA=GPS.readline()
        sleep(.1)
        
        splitNM = NMEA.split(',')
        if splitNM[0]=='$GPRMC':
            isGPRMC=True
        
        if splitNM[0]=='$GPGGA':
            isGPGGA=True
        sleep(.1)
    
    isGPRMC=False
    isGPGGA=False
    return NMEA

#Kalman Filter for more accuracy
def kalmanFilter(GPS):
    print GPS
    #ToDo
    return

