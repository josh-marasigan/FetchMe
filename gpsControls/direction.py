# -*- coding: utf-8 -*-
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import serial
import math
from math import radians, cos, sin, asin, sqrt
from time import sleep
from pythonled import pythonled
from decimal import *

ADC.setup()
#Front, Right, Left, Back in that order
#USE 1.8V ONLY FOR THESE PORTS!!!
#USE 1.8V ONLY FOR THESE PORTS!!!
#USE 1.8V ONLY FOR THESE PORTS!!!
#USE 1.8V ONLY FOR THESE PORTS!!!
#There is currently a bug in the ADC driver. 
#You'll need to read the values twice 
#in order to get the latest value.
#WE WILL FRY THE CIRCUIT IF WE DONT LOL
#WE WILL FRY THE CIRCUIT IF WE DONT LOL
#WE WILL FRY THE CIRCUIT IF WE DONT LOL
#WE WILL FRY THE CIRCUIT IF WE DONT LOL

#Motor Controls. Front/Back, Left/Right
GPIO.setup("P8_8", GPIO.OUT)
GPIO.setup("P8_9", GPIO.OUT)
GPIO.setup("P8_11", GPIO.OUT)
GPIO.setup("P8_14", GPIO.OUT)

#Hearbeat. 2 USR, 1 LED
GPIO.setup("P8_44", GPIO.OUT)
user2 = pythonled(2)
user3 = pythonled(3)
user0 = pythonled(0)
user2.off()
user3.off()
user0.off()

#Directions
directions = ["NE", "E", "SE", "S", "SW", "W", "NW", "N"]

#Obstacle detection Flags
obsL = False
obsC = False
obsR = False
obsB = False
obsBR = False
obsBL = False

#Need to interface 5 sensors
def is_obstruction():
	#Analog read and time delay (Only front sensor)
	#There is currently a bug in the ADC driver. 
	#You'll need to read the values twice in order to get the latest value.
	'''
	wait_pin_change(ADC.read("AIN2"))
	print "Front Detected"
	'''
	value = ADC.read("AIN2") #"P9_37"
	value = ADC.read("AIN2")
	
	'''
	#wait_pin_change(ADC.read("AIN3"))
	#print "Right Detected"
	valRight = ADC.read("AIN3") #"P9_38"
	valRight = ADC.read("AIN3")
	
	#wait_pin_change(ADC.read("AIN0"))
	#print "Left Detected"
	valLeft = ADC.read("AIN0") #"P9_39"
	valLeft = ADC.read("AIN0")
	
	#wait_pin_change(ADC.read("AIN1"))
	#print "Back"
	valBack = ADC.read("AIN1") #"P9_40"
	valBack = ADC.read("AIN1")
	'''
	
	#POLL FOR INTERRUPT, range is 0-1.65V
	voltage = value * 1.8
	'''
	voltRight = valRight * 1.8
	voltLeft = valLeft * 1.8
	voltBack = valBack * 1.8
	'''
	
	voltRight = 0
	voltLeft = 0
	voltBack = 0
	
	sensorFlag=False
	voltArr = [voltage,voltRight,voltLeft,voltBack]
	count = 0
	for v in voltArr:
		#print (v)
		if v > 1.6:
			sensorFlag=True
			#Poll which sensor went off
			if count==0:
				obsC=True
			elif count==1:
				obsR=True
			elif count==2:
				obsL=True
			elif count==3:
				obsB=True
		else:
			if count==0:
				obsC=False
			elif count==1:
				obsR=False
			elif count==2:
				obsL=False
			elif count==3:
				obsB=False
		#increment
		count = count+1
	
	return sensorFlag

#Henry's Algorithm for obstacle avoidance
def avoid_obstruction():
	#Assert that correct movements according to obstructions
	global obsL
	global obsC
	global obsR
	global obsBL
	global obsBR
	avoidCount=0
	obsBR = obsB
	obsBL = obsB
	
	#Poll analog ports to update obs variables/prevent lock
	if obsC == True:
		#print("Only Thread Running should be actUpon...")
		while obsC == True:
			print("Iteration count... ",avoidCount)
			#Can go right
			if obsR == False:
				
				#Go back left first
				if obsBL == False:
					bearing = 'SW'
					
					#Go straight now (Turning right essentially)
					if obsC == False:
						bearing = 'N'
			
			elif obsR == True and obsL == False:
				
				#Go back left first
				if obsBR == False:
					bearing = 'SE'
					
					#Go straight now (Turning right essentially)
					if obsC == False:
						bearing = 'N'
			
			else:
				print ("No Obstruction")
			
			motorController(bearing)
			sleep(5)
			avoidCount=avoidCount+1

#Inputs: myGPS.latDeg, myGPS.latMin, myGPS.lonDeg, myGPS.lonMin
#Outputs: Converted Coordinates in Radians
def useCoordinates(passed_coordinates):
    latDeg = math.radians(passed_coordinates[0])
    latMin = math.radians(passed_coordinates[1])
    lonDeg = math.radians(passed_coordinates[2])
    lonMin = math.radians(passed_coordinates[3])
    
    print ("This are the coordinates:" ,latDeg, latMin, lonDeg, lonMin)
    radian_list = [latDeg, latMin, lonDeg, lonMin]
    return radian_list

#Get bearing from given degrees
def bearings(brng):
    bearings = ["NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    index = brng - 22.5
    if index < 0:
        index += 360;
    index = int(index / 45);
    return bearings[index]

#Algorithm for direction given old coordinate format
def travel(past, current):
	dLon = (current[2]+current[3]/60) - (past[2]+past[3]/60)
	y = math.sin(dLon)*math.sin(current[0]+current[1]/60)
	x = math.cos(past[0]+past[1]/60)*math.sin(current[0]+current[1]/60)-math.sin(past[0]+past[1]/60)*math.cos(current[0])*math.cos(dLon)
	print ("Y:" ,y)
	print ("X:" ,x)
	brng = math.atan2(y,x)
	temp = math.degrees(brng)
	res = bearings(temp)
	print (res)
	return res

# Input : Two pairs of tuple coordinates
def inRadius(first, second):
	# Within 4th decimal coordinate
	buffer_dist = 0.009
	
	#flt = float(radius)
	#isInside = (pow((second[0] - first[0]),2) + pow((second[1] - first[1]),2) < pow(flt,2))
	lon1 = first[0]
	lat1 = first[1]

	print second

	getcontext().prec = 6
	lon2 = Decimal(second[0])
	lat2 = Decimal(second[1])
	
	lon2 = round(lon2,6)
	lat2 = round(lat2,6)
	
	print "Second Longitude... ", lon2," Second Latitude... ", lat2
	
	#find distance between coordinates by haversine formula
	distance = haversine(lon1, lat1, lon2, lat2)
	
	if (distance < buffer_dist):
		return True
	else:
		return False

#Perpetually call this to keep motor running at all time
#Dedicate and run a new single thread for this function
def alwaysRun(bearing):
	if bearing!="X":
		motorController(bearing)

#Accommodate bearings with direction. These ports will remain at specified state
#until updated accordingly
#Make a thread for perpetually running the car
def motorController(bearing):
	if bearing == 'N': #going straight
		#Corrected
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.LOW)
		GPIO.output("P8_14", GPIO.LOW)

	elif bearing == 'NW':
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.LOW)
		GPIO.output("P8_14", GPIO.LOW)
		'''
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)
		'''
		
	elif bearing == 'NE':
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.LOW)
		GPIO.output("P8_14", GPIO.LOW)
		#turn right 1 period
		'''
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.LOW)
		GPIO.output("P8_14", GPIO.HIGH)
		'''

	elif bearing == 'W': #turn right 3 periods
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)

	elif bearing == 'E': #turn left, 1 period
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)
		
	elif bearing == 'SE': #turn left 2 periods
		GPIO.output("P8_8", GPIO.LOW)
		GPIO.output("P8_9", GPIO.HIGH)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)
	
	elif bearing == 'S': #turn left 3 periods
		GPIO.output("P8_8", GPIO.LOW)
		GPIO.output("P8_9", GPIO.HIGH)
		GPIO.output("P8_11", GPIO.LOW)
		GPIO.output("P8_14", GPIO.LOW)
	
	elif bearing == 'SW':#turn left 4 periods
		GPIO.output("P8_8", GPIO.LOW)
		GPIO.output("P8_9", GPIO.HIGH)
		GPIO.output("P8_11", GPIO.LOW)
		GPIO.output("P8_14", GPIO.HIGH)
			
	else:
		print ("ERROR, NO BEARING")

# Haversine formula
def haversine(lon1, lat1, lon2, lat2):
	# convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	
	# haversine formula 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a)) 
	km = 6367 * c
	return km

#Credit to https://github.com/jeromer
#"""
#Calculates the bearing between two points.
#The formulae used is the following:
#    θ = atan2(sin(Δlong).cos(lat2),
#              cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))

#:Parameters:
#  - `pointA: The tuple representing the latitude/longitude for the
#    first point. Latitude and longitude must be in decimal degrees
#  - `pointB: The tuple representing the latitude/longitude for the
#    second point. Latitude and longitude must be in decimal degrees

#:Returns:
#  The bearing in degrees

#:Returns Type:
#  float
def calculate_initial_compass_bearing(pointA, pointB):
	if (type(pointA) != tuple) or (type(pointB) != tuple):
		raise TypeError("Only tuples are supported as arguments")
	
	lat1 = math.radians(float(pointA[0]))
	lat2 = math.radians(float(pointB[0]))
	
	diffLong = math.radians(float(pointB[1])-float(pointA[1]))
	
	x = math.sin(diffLong) * math.cos(lat2)
	y = math.cos(lat1)*math.sin(lat2)-(math.sin(lat1)*math.cos(lat2)*math.cos(diffLong))
	
	initial_bearing = math.atan2(x, y)
	
	# Now we have the initial bearing but math.atan2 return values
	# from -180° to + 180° which is not what we want for a compass bearing
	# The solution is to normalize the initial bearing as shown below
	initial_bearing = math.degrees(initial_bearing)
	compass_bearing = (initial_bearing + 360) % 360
	return compass_bearing

#Get degrees needed for angle A to align to angle B
def get_angle(angle_A, angle_B):
	theta = abs(angle_B-angle_A) % 360
	sign = 1
	
	#Signed Angle
	if not ((angle_A-angle_B >= 0 and angle_A-angle_B <= 180) 
		or (angle_A-angle_B <= -180 and angle_A-angle_B >= -360)):
		sign = -1

	if theta > 180:
		result = 360-theta
	else:
		result = theta
	
	return result*sign

#Simple Heartbeat
def heartbeat(flip):
	#Toggle
	if flip:
		user2.on()
		user3.on()
		GPIO.output("P8_44", GPIO.HIGH)
	
	else:
		user2.off()
		user3.off()
		GPIO.output("P8_44", GPIO.LOW)

def nearly_equal(a,b,sig_fig):
	return (a==b or int(a*10**sig_fig) == int(b*10**sig_fig))

#Debouncer needed due to ultrasonic sensor noise
def wait_pin_change():
	print "Wait for pin debounce"
	cur_value = is_obstruction()
	active = 0

	#200ms~2s
	while active < 30:
		#Inrement if no toggle
		#if not nearly_equal(pin, cur_value,2):
		if is_obstruction() != cur_value:
			active += 1

		#if pin.value() != cur_value:
		#Restart Count if noise detected
		else:
			active = 0

		sleep(.01)

#Time delay: 5s
def setDelay():
	count = 0
	while count < 500:
		sleep(.01)

	return
