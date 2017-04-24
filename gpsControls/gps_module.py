# -*- coding: utf-8 -*-
import serial
import direction
import gpsTestSignal as getGPS
import Adafruit_BBIO.UART as UART
from threading import Thread
from time import sleep
from decimal import *

#6 decimal points to represent coordinates
getcontext().prec = 6

#Serial Port Setup w/ Baud Rate
UART.setup("UART1")
ser=serial.Serial('/dev/ttyO1',9600)

### Test Route (RLM Bridge)
testRoute = [(30.289288, -97.735943),(30.289471, -97.735932),(30.289571, -97.735924)]
demoRoute = [(30.173654,-97.441429),(30.173654,-97.441455)]

testRoute2 = [(30.173539,-97.441455),(30.173613,-97.441459)]

### Route going to Jester Entrance (PCL)
route = [(30.284743, -97.736801),(30.284591, -97.737299),(30.284100, -97.737347),(30.283469, -97.737409),(30.282684, -97.737479)]
temp2 = [(30.284535, -97.736424),(30.284591, -97.737299),(30.284100, -97.737347),(30.283469, -97.737409),(30.282684, -97.737479)]

### Reverse of T2 (Going back)
route2 = temp2[::-1]

RLM2 = [(30.173472,-97.441573),(30.173716,-97.441460)]

### Route going to Jester Entrance (Gregory)
route3 = [(30.284535, -97.736424),(30.284591, -97.737299),(30.284100, -97.737347),(30.283469, -97.737409),(30.283411, -97.736777)]

routeRLM = [(30.173359,-97.442115),(30.173266,-97.442186)]

#Directions
bearings = ["NE", "E", "SE", "S", "SW", "W", "NW", "N"]
clock_cycle = 0
route_index = 0

#Flag to kill multithreads
finishProgram = False
found_obstruction = False

#Event flags
flip = False

#Global Bearings
newBearing = "X"
pastBearing = "X"
NMEA1_global = ""
NMEA2_global = ""
caseFlag=False

class GPS:
    #Global Current Latitude and Longitude
    currentLat = "99.999999"
    currentLon = "-99.999999"
    
    def __init__(self):
        
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
        '''
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
        '''
        #ser.write(GPRMC_GPGGA)
        #sleep(1)
        #ser.flushInput()
        ser.flushInput()
        print ("GPS Initialized")
    
    def read(self):
        #Fix will be overriden if satellites acquired. '0' otherwise to prevent lock
        self.fix=0
        ser.flushInput()
        ser.flushInput()
        sleep(.4)
        
        #Poll serial port for gprmc or gpgga
        #print "Polling for serial A..."
        sleep(.5)
        NMEA1_global = getGPS.poll()
        #print (NMEA1_global)
        self.NMEA1=NMEA1_global
        
        #Poll serial port for gprmc or gpgga
        #print "Polling for serial B..."
        sleep(.5)
        NMEA2_global = getGPS.poll()
        confirmNMEA2 = NMEA2_global.split(',')
        
        #print (NMEA2_global)
        self.NMEA2=NMEA2_global
        
        #While condition ensures NMEA1 or 2 is not empty
        NMEA1_array=self.NMEA1.split(',')
        NMEA2_array=self.NMEA2.split(',')
        
        if NMEA1_array[0]=='$GPRMC':
            
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
            self.currentLon = '-'+self.currentLon[0:2]+'.'+self.currentLon[2:]
            
            self.lonMin=NMEA1_array[5][-7:]
            self.lonHem=NMEA1_array[6]
            self.knots=NMEA1_array[7]
            
        if NMEA1_array[0]=='$GPGGA':
            
            self.fix=NMEA1_array[6]
            self.altitude=NMEA1_array[9]
            self.sats=NMEA1_array[7]
        
        if NMEA2_array[0]=='$GPRMC':
            
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
            self.currentLon = '-'+self.currentLon[0:2]+'.'+self.currentLon[2:]
            
            self.lonMin=NMEA2_array[5][-7:]
            self.lonHem=NMEA2_array[6]
            self.knots=NMEA2_array[7]
            
        if NMEA2_array[0]=='$GPGGA':
            self.fix=NMEA2_array[6]
            self.altitude=NMEA2_array[9]
            self.sats=NMEA2_array[7]

#Class for background thread running motor
class MotorThread(object):
    def __init__(self, interval=.2):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        
        #Thread for motor control continuous
        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
    
    def run(self):
        print ("BACKGROUND MOTOR THREAD RUNNING")
        while finishProgram==False:
            global newBearing
            global caseFlag
            if caseFlag:
                flagcount = 0
                while flagcount < 8000:
                    direction.alwaysRun(newBearing)
                    flagcount = flagcount + 1
                
                
                newBearing='N'
                print newBearing, "Now headed"
                caseFlag=False
            
            else:
                print "Standard Direction"
                count = 0
                while count < 12000:
                    ber = "N"
                    direction.alwaysRun(ber)
                    count = count + 1

#Class for background thread polling obstructions
class BackgroundThread(object):
    def __init__(self, interval=.2):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        
        #Thread for avoidance detection
        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
    
    def run(self):
        #Until the var has arrived, keep polling for obstructions
        print ("BACKGROUND SENSORS THREAD RUNNING")
        while not finishProgram:
            print "POLL OBSTRUCTION"
            #Insert Obstacle Avoidance Poll, set global flag true
            
            #direction.wait_pin_change(direction.is_obstruction())
            direction.wait_pin_change()
            found_obstruction = direction.is_obstruction()
            
            #Act upon detection
            if found_obstruction:
                print "Obstruction Found..."
                
                #Thread for avoidance action
                actUpon = Thread(target=direction.avoid_obstruction(), args=())
                actUpon.daemon = True
                actUpon.start()
            
            else:
                print "Obstruction Not Found..."
            
            #Keep Polling
            sleep(self.interval)

#Class for current car location
myGPS=GPS()

#Last known GPS coordinates
myPastGPS=GPS()

#Multithread for collision avoidance loop and motor
motorMovementThread = MotorThread()
#backgroundObstructionThread = BackgroundThread()

#Test Route for debug only
while(1):
    route = RLM2
    #LED Heartbeat
    if clock_cycle%2==0:
        flip = True
        direction.heartbeat(flip)
    else:
        flip = False
        direction.heartbeat(flip)

    #Get current clock cycle (For turn timing)
    print ""
    print "Iteration Count: " + str(clock_cycle)
    print ""
    
    #Calculate the car's heading traveled between the GPS polls
    '''
    if clock_cycle!=0:
        pastBearing = direction.calculate_initial_compass_bearing((myPastGPS.currentLat, myPastGPS.currentLon),(myGPS.currentLat,myGPS.currentLon))
    '''

    #Set current GPS as "past GPS" to compare with current to target coordinate
    if clock_cycle==0:
        myPastGPS = myGPS
    
    #Obstruction found, pause thread until dealt with
    #if found_obstruction:
    while found_obstruction:
        #Wait until background thread finishes
        sleep(1)

    #Get next node in path
    myGPS.read()
    if myGPS.fix!=0:
        print("")
        print ("Current Latitude... ",myGPS.currentLat)
        print ("Current Longitude...",myGPS.currentLon)
        print("")
        
        if myGPS.currentLat=='.':
            myGPS.currentLat='0.0'
        
        if myGPS.currentLon=='-.':
            myGPS.currentLon='0.0'
        
        latD = Decimal(myGPS.currentLat)
        lonD = Decimal(myGPS.currentLon)
        
        if direction.inRadius((latD,lonD),route[route_index]):
            if route_index == len(route)-1:
                print 'ARRIVED'
                finishProgram = True
                
                #Exit thread
                break
            else:
                route_index = route_index + 1
        
        #Bearing in terms of CURRENT LOCATION towards NEXT TARGET NODE
        target_node = route[route_index]
        currentBearing = direction.calculate_initial_compass_bearing((myGPS.currentLat,myGPS.currentLon),(target_node[0],target_node[1]))
        
        print ""
        print 'Current Bearing in Degrees... ',currentBearing
        
        #Bearing in terms of CURRENT LOCATION from PAST LOCATION
        if clock_cycle==0:
            past_node = (myPastGPS.currentLat,myPastGPS.currentLon)
        
        print past_node[0],past_node[1],"..........",myGPS.currentLat,myGPS.currentLon
        prevBearing = direction.calculate_initial_compass_bearing((past_node[0],past_node[1]),(myGPS.currentLat,myGPS.currentLon))
        
        print("")
        print 'Past Bearing in Degrees... ',prevBearing
        print 'Current Bearing in Degrees... ',currentBearing
        
        #Does the car need to turn left or right to adjust course?
        turnAngle = direction.get_angle(prevBearing,currentBearing)
        #pastBearing = currentBearing
        
        #Turn only for 3 seconds
        tempBearing = direction.bearings(turnAngle)
        print caseFlag
        print "Want to Head... ",tempBearing, " Actually Heading... " ,newBearing
        if tempBearing != 'N':
            #newBearing = tempBearing
            #newBearing = 'N'
            newBearing = tempBearing
            caseFlag=True
        else:
            newBearing = tempBearing
            caseFlag=False
        
        #Perform actual car movement
        print ""
        print 'Current Moving Direction... ',newBearing
        #direction.motorController(newBearing)
        
    #Current travel node
    print ""
    print 'Current Target Coordinate Node: ',route[route_index]
    print 'Number of Nodes Until Destination: ',len(route) - (route_index)
    
    clock_cycle = clock_cycle + 1
    past_node = (myGPS.currentLat,myGPS.currentLon)
    myPastGPS = myGPS

    #Update navigation every 2 seconds
    sleep(2)
    
