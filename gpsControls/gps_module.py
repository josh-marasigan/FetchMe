# -*- coding: utf-8 -*-
import serial
import direction
import Adafruit_BBIO.UART as UART
from time import sleep
from decimal import *

#6 decimal points to represent coordinates
getcontext().prec = 6

#Serial Port Setup w/ Baud Rate
UART.setup("UART1")
ser=serial.Serial('/dev/ttyO1',9600)

### Route going to Jester Entrance (PCL)
route = [(30.284743, -97.736801),(30.284591, -97.737299),(30.284100, -97.737347),(30.283469, -97.737409),(30.282684, -97.737479)]
temp2 = [(30.284535, -97.736424),(30.284591, -97.737299),(30.284100, -97.737347),(30.283469, -97.737409),(30.282684, -97.737479)]

### Reverse of T2 (Going back)
route2 = temp2[::-1]

### Route going to Jester Entrance (Gregory)
route3 = [(30.284535, -97.736424),(30.284591, -97.737299),(30.284100, -97.737347),(30.283469, -97.737409),(30.283411, -97.736777)]

#Directions
bearings = ["NE", "E", "SE", "S", "SW", "W", "NW", "N"]
clock_cycle = 0
route_index = 0

#Global Bearings
currentBearing = "X"
pastBearing = "X"

class GPS:
    def __init__(self):
        
        #Global Current Latitude and Longitude
        currentLat = "99.999999"
        currentLon = "-99.999999"
        
        #This sets up variables for useful commands.
        #This set is used to set the rate the GPS reports
        UPDATE_10_sec=  "$PMTK220,10000*2F\r\n" #Update Every 10 Seconds
        UPDATE_5_sec=  "$PMTK220,5000*1B\r\n"   #Update Every 5 Seconds  
        UPDATE_1_sec=  "$PMTK220,1000*1F\r\n"   #Update Every One Second
        UPDATE_200_msec=  "$PMTK220,200*2C\r\n" #Update Every 200 Milliseconds
        
        #This set is used to set the rate the GPS takes measurements
        MEAS_10_sec = "$PMTK300,10000,0,0,0,0*2C\r\n" #Measure every 10 seconds
        MEAS_5_sec = "$PMTK300,5000,0,0,0,0*18\r\n"   #Measure every 5 seconds
        MEAS_1_sec = "$PMTK300,1000,0,0,0,0*1C\r\n"   #Measure once a second
        MEAS_200_msec= "$PMTK300,200,0,0,0,0*2F\r\n"  #Meaure 5 times a second
        
        #Set the Baud Rate of GPS
        BAUD_57600 = "$PMTK251,57600*2C\r\n"          #Set Baud Rate at 57600
        BAUD_9600 ="$PMTK251,9600*17\r\n"             #Set 9600 Baud Rate
        
        #Commands for which NMEA Sentences are sent
        ser.write(BAUD_9600)
        sleep(1)
        ser.baudrate=57600
        GPRMC_ONLY= "$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n" #Send only the GPRMC Sentence
        GPRMC_GPGGA="$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n"#Send GPRMC AND GPGGA Sentences
        SEND_ALL ="$PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n" #Send All Sentences
        SEND_NOTHING="$PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n" #Send Nothing
        ser.write(UPDATE_1_sec)
        sleep(1)
        ser.write(MEAS_1_sec)
        sleep(1)
        ser.write(GPRMC_GPGGA)
        sleep(1)
        ser.flushInput()
        ser.flushInput()
        print ("GPS Initialized")
        
    def read(self):
        #Fix will be overriden if satellites acquired. '0' otherwise to prevent lock
        self.fix=0
        ser.flushInput()
        ser.flushInput()
        
        #Poll serial port for gprmc or gpgga
        print ("Polling for serial A")
        while ser.inWaiting()==0:
            pass
        
        print ("Done Polling for A")
        self.NMEA1=ser.readline()
        
        #Poll serial port for gprmc or gpgga
        print ("Polling for serial B")
        while ser.inWaiting()==0:
            pass
        
        print ("Done Polling for B")
        self.NMEA2=ser.readline()
        
        #While condition ensures NMEA1 or 2 is not empty
        NMEA1_array=self.NMEA1.split(',')
        NMEA2_array=self.NMEA2.split(',')
        
        # Default Values for testing
        '''
        print ("Parsed Coordinate Input")
        self.timeUTC='12:00'
        self.latDeg='9999.9'
        currentLat = self.latDeg
        self.latMin='-1'
        self.latHem='-1'
        self.lonDeg='9999.9'
        currentLon = self.lonDeg
        self.lonMin='-1'
        self.lonHem='-1'
        self.knots='0'
        self.altitude='0'
        self.sats='0'
        '''
        
        # Testing Purposes
        '''
        gprmcTest = '$GPRMC,204756.000,A,3017.3548,N,09744.1552,W,0.01,256.62,150217,,,D*7D'
        gpggaTest = '$GPGGA,204755.000,3017.3548,N,09744.1552,W,2,07,1.18,222.6,M,-22.5,M,0000,0000*5D'
        NMEA1_array = gprmcTest.split(',')
        NMEA2_array = gpggaTest.split(',')
        for i in NMEA1_array:
            print (i)
        '''
        
        if NMEA1_array[0]=='$GPRMC':
            print ("GPRMC PARSE START...")
            self.timeUTC=NMEA1_array[1][:-8]+':'+NMEA1_array[1][-8:-6]+':'+NMEA1_array[1][-6:-4]
            self.latDeg=NMEA1_array[3][:-7]
            
            self.currentLat = NMEA1_array[3]
            self.currentLat = self.currentLat[0:4]+self.currentLat[4+1:]
            self.currentLat = self.currentLat[0:2]+'.'+self.currentLat[2:]
            
            self.latMin=NMEA1_array[3][-7:]
            self.latHem=NMEA1_array[4]
            self.lonDeg=NMEA1_array[5][:-7]
            
            self.currentLon = NMEA1_array[5]
            self.currentLon = self.currentLon[1:]
            self.currentLon = self.currentLon[0:4]+self.currentLon[4+1:]
            self.currentLon = self.currentLon[0:2]+'.'+self.currentLon[2:]
            
            self.lonMin=NMEA1_array[5][-7:]
            self.lonHem=NMEA1_array[6]
            self.knots=NMEA1_array[7]
            print ("...PASSED GPRMC PARSE")
            
        if NMEA1_array[0]=='$GPGGA':
            print ("GPGGA PARSE START...")
            self.fix=NMEA1_array[6]
            self.altitude=NMEA1_array[9]
            self.sats=NMEA1_array[7]
            print ("...PASSED GPGGA PARSE")
            
        if NMEA2_array[0]=='$GPRMC':
            print ("GPRMC PARSE START...")
            self.timeUTC=NMEA2_array[1][:-8]+':'+NMEA1_array[1][-8:-6]+':'+NMEA1_array[1][-6:-4]
            self.latDeg=NMEA2_array[3][:-7]
            
            self.currentLat = NMEA2_array[3]
            self.currentLat = self.currentLat[0:4]+self.currentLat[4+1:]
            self.currentLat = self.currentLat[0:2]+'.'+self.currentLat[2:]
            
            self.latMin=NMEA2_array[3][-7:]
            self.latHem=NMEA2_array[4]
            self.lonDeg=NMEA2_array[5][:-7]
            
            self.currentLon = NMEA2_array[5]
            self.currentLon = self.currentLon[1:]
            self.currentLon = self.currentLon[0:4]+self.currentLon[4+1:]
            self.currentLon = self.currentLon[0:2]+'.'+self.currentLon[2:]
            
            self.lonMin=NMEA2_array[5][-7:]
            self.lonHem=NMEA2_array[6]
            self.knots=NMEA2_array[7]
            print ("...PASSED GPRMC PARSE")
            
        if NMEA2_array[0]=='$GPGGA':
            print ("GPGGA PARSE START...")
            self.fix=NMEA2_array[6]
            self.altitude=NMEA2_array[9]
            self.sats=NMEA2_array[7]
            print ("...PASSED GPGGA PARSE")

#Class for current car location
myGPS=GPS()

#Last known GPS coordinates
myPastGPS=GPS()

while(1):
    #Get current clock cycle (For turn timing)
    print ("Iteration Count: " + str(clock_cycle))
    
    #Gather location data
    print ('POLLING FOR GPA COORDINATES')
    
    myGPS.read()
    if myGPS.fix!=0:
        print ('Universal Time: ',myGPS.timeUTC)
        print ('You are Tracking: ',myGPS.sats,' satellites')
        print ('My Latitude: ',myGPS.latDeg, 'Degrees ', myGPS.latMin,' minutes ', myGPS.latHem)
        print ('My Longitude: ',myGPS.lonDeg, 'Degrees ', myGPS.lonMin,' minutes ', myGPS.lonHem)
        print ('My Speed: ', myGPS.knots)
        print ('My Altitude: ',myGPS.altitude)
        print ('CURRENT LATITUDE COORDINATE',myGPS.currentLat)
        print ('CURRENT LONGITUDE COORDINATE',myGPS.currentLon)
    
    #Calculate the car's heading traveled between the GPS polls
    if clock_cycle!=0:
        pastBearing = direction.calculate_initial_compass_bearing((myPastGPS.currentLat, myPastGPS.currentLon),(myGPS.currentLat,myGPS.currentLon))
    
    #Set current GPS as "past GPS" 
    myPastGPS = myGPS
    
    #Consintually poll for obstruction
    found_obstruction = direction.is_obstruction()
    
    #Obstruction found
    if found_obstruction:
        direction.avoid_obstruction()
    
    #Get next node in path
    if myGPS.fix!=0:
        print ("GET COORDINATES POLL")
        print (myGPS.currentLat)
        print (myGPS.currentLon)
        print ("GET COORDINATES POLL DONE")
        sleep(.1)
        latD = Decimal(myGPS.currentLat)
        lonD = Decimal(myGPS.currentLon)
        
        if direction.inRadius((latD,lonD),route[route_index]):
            if route_index == len(route)-1:
                print ('ARRIVED')
            else:
                route_index = route_index + 1
        
        #Bearing in terms of CURRENT LOCATION towards NEXT TARGET NODE
        target_node = route[route_index]
        currentBearing = direction.calculate_initial_compass_bearing((myGPS.currentLat,myGPS.currentLon),(target_node[0],target_node[1]))
        print ('Bearing in Degrees: ',currentBearing)

        #Bearing in terms of CURRENT LOCATION from PAST LOCATION
        past_node = (myPastGPS.currentLat,myPastGPS.currentLon)
        prevBearing = direction.calculate_initial_compass_bearing((past_node[0],past_node[1]),(myGPS.currentLat,myGPS.currentLon))
        print ('Bearing in Degrees: ',prevBearing)
        
        #Does the car need to turn left or right to adjust course?
        turnAngle = direction.get_angle(currentBearing, prevBearing)
        newBearing = direction.bearings(turnAngle)
        
        #Perform actual car movement
        print ('Current Moving Direction: ',newBearing)
        direction.motorController(newBearing)
    
    # Current travel node
    print ('Current Target Coordinate Node: ',route[route_index])
    print ('Number of Nodes Until Destination: ',len(route) - (route_index+1))
    clock_cycle = clock_cycle + 1
    sleep(1)
    