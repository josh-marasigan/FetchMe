# -*- coding: utf-8 -*-
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import serial
import math
from math import radians, cos, sin, asin, sqrt
from time import sleep

ADC.setup()

#Front, Right, Left, Back in that order
#USE 1.8V ONLY FOR THESE PORTS!!!
#USE 1.8V ONLY FOR THESE PORTS!!!
#USE 1.8V ONLY FOR THESE PORTS!!!
#USE 1.8V ONLY FOR THESE PORTS!!!
GPIO.setup("P8_6", GPIO.IN)
GPIO.setup("P8_7", GPIO.IN)
GPIO.setup("P8_12", GPIO.IN)
GPIO.setup("P8_13", GPIO.IN)
#WE WILL FRY THE CIRCUIT IF WE DONT LOL
#WE WILL FRY THE CIRCUIT IF WE DONT LOL
#WE WILL FRY THE CIRCUIT IF WE DONT LOL
#WE WILL FRY THE CIRCUIT IF WE DONT LOL

#Motor Controls. Front/Back, Left/Right
GPIO.setup("P8_8", GPIO.OUT)
GPIO.setup("P8_9", GPIO.OUT)
GPIO.setup("P8_11", GPIO.OUT)
GPIO.setup("P8_14", GPIO.OUT)

#Directions
directions = ["NE", "E", "SE", "S", "SW", "W", "NW", "N"]

#Obstacle detection Flags
obsL = False
obsC = False
obsR = False
obsBL = False
obsBR = False

#Need to interface 5 sensors
def is_obstruction():
	#Analog read and time delay (Only front sensor)
	value = ADC.read("P9_36")
	sleep(.2)

	#POLL FOR INTERRUPT, range is 0-1.65V
	voltage = value * 1.8
	if voltage > 1.6:
		print ('Obstruction Detected')
		obsC = True
		return True
	elif voltage < .3:
		print ('No Obstruction')
		return False
	else:
		print ('No Sensor Connection: Error')
		return False

#Henry's Algorithm for obstacle avoidance
def avoid_obstruction():
	#Assert that correct movements according to obstructions
	global obsL
	global obsC
	global obsR
	global obsBL
	global obsBR
	
	#Poll analog ports to update obs variables/prevent lock
	if obsC == True:
		while obsC == True:
			if obsR == False:
				
				if obsBL == False:
					bearing = 'SW'
					sleep(1)
					
					if obsC == False:
						bearing = 'N'
						sleep(3)
			
			elif obsR == True and obsL == False:
				
				if obsBR == False:
					bearing = 'SE'
					sleep(1)
					
					if obsC == False:
						bearing = 'N'
						sleep(3)
			
			else:
				print ("No Obstruction")

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
	#radius = 0.00028 # Approx 2 feet
	#print 'First Circle: ',pow((second[0] - first[0]),2) + pow((second[1] - first[1]),2)

	#print 'Second Circle: ',pow(flt,2)
	buffer_dist = 0.0013
	
	#flt = float(radius)
	#isInside = (pow((second[0] - first[0]),2) + pow((second[1] - first[1]),2) < pow(flt,2))
	lon1 = first[0]
	lat1 = first[1]
	lon2 = second[0]
	lat2 = second[1]
	
	#find distance between coordinates by haversine formula
	distance = haversine(lon1, lat1, lon2, lat2)
	
	if (distance < buffer_dist):
		return True
	else:
		return False

#Accommodate bearings with direction. These ports will remain at specified state
#until updated accordingly
def motorController(bearing):
	if bearing == 'NE': #going straight
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.HIGH)
		
	elif bearing == 'E': #turn left, 1 period
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)
		
	elif bearing == 'SE': #turn left 2 periods
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)
		
	elif bearing == 'S': #turn left 3 periods
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)
		
	elif bearing == 'SW':#turn left 4 periods
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.HIGH)
		GPIO.output("P8_14", GPIO.LOW)
		
	elif bearing == 'W': #turn right 3 periods
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.LOW)
		GPIO.output("P8_14", GPIO.HIGH)
		
	elif bearing == 'NW':#turn right 2 periods
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_11", GPIO.LOW)
		GPIO.output("P8_14", GPIO.HIGH)
		
	elif bearing == 'N': #turn right 1 period
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
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
	if not ((angle_A-angle_B >= 0 and angle_A-angle_B <= 180) or (angle_A-angle_B <= -180 and angle_A-angle_B >= -360)):
		sign = -1

	if theta > 180:
		result = 360-theta
	else:
		result = theta
	
	return result*sign