import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import serial
import math
from time import sleep

ADC.setup() #USE 1.8V ONLY!!! 
GPIO.setup("P8_8", GPIO.OUT)
GPIO.setup("P8_9", GPIO.OUT)
GPIO.setup("P8_11", GPIO.OUT)
GPIO.setup("P8_14", GPIO.OUT)
#Directions
directions = ["NE", "E", "SE", "S", "SW", "W", "NW", "N"]

def is_obstruction():
	value = ADC.read("P9_36")
	#POLL FOR INTERRUPT, range is 0-1.65V
	voltage = value * 1.8
	if voltage > 1.6:
		print 'Obstruction Detected'
		return True
	elif voltage < .3:
		print 'No Obstruction'
		return False
	else:
		print 'Should not be able to execute: Error'
		return False

#Algorithm for obstacle avoidance
def clearpath():
	sleep(10)

# inputs: myGPS.latDeg, myGPS.latMin, myGPS.lonDeg, myGPS.lonMin
def useCoordinates(passed_coordinates):
    latDeg = math.radians(passed_coordinates[0])
    latMin = math.radians(passed_coordinates[1])
    lonDeg = math.radians(passed_coordinates[2])
    lonMin = math.radians(passed_coordinates[3])
    
    print "This are the coordinates:" ,latDeg, latMin, lonDeg, lonMin
    radian_list = [latDeg, latMin, lonDeg, lonMin]
    return radian_list

def bearings(brng):
    bearings = ["NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    index = brng - 22.5
    if index < 0:
        index += 360;
    index = int(index / 45);
    return bearings[index]
    
# algorithm for direction
def travel(past, current):
	dLon = (current[2]+current[3]/60) - (past[2]+past[3]/60)
    y = math.sin(dLon)*math.sin(current[0]+current[1]/60)
    x = math.cos(past[0]+past[1]/60)*math.sin(current[0]+current[1]/60)-math.sin(past[0]+past[1]/60)*math.cos(current[0])*math.cos(dLon)
    print "Y:" ,y
    print "X:" ,x
    brng = math.atan2(y,x)
    temp = math.degrees(brng)
    res = bearings(temp)
    print res
    return res

def inRadius(first, second):
	return True

def motorController(bearing):
	if bearing == 'NE':
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)
	elif bearing == 'E':
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)
	elif bearing == 'SE':
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)
	elif bearing == 'S':
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)
	elif bearing == 'SW':
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)
	elif bearing == 'W':
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)
	elif bearing == 'NW':
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)
	elif bearing == 'N':
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)
	else:
		print "ERROR, NO BEARING"