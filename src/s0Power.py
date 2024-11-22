#********************************************************************#
# converts the S0 impulse from an GPIO to a power value
#********************************************************************#

import RPi.GPIO as GPIO
import time
import syslog as mySysLog
import datetime
#myVerbose must be the first import
from myVerbose import *
import sendPower2Influxdb
import sendPower2VZ


mySysLog.syslog(mySysLog.LOG_INFO, "s0Power.py started")
myPrint(STARTUP,"s0Power.py with Debuglevel= '" + getVerboseName(getVerbose()) +"' started")
#******************************************#
# global variables
#******************************************#
UPDATE_TIME = 60 
INPUTNR = 2
count=0
ikeepAlive = 0
keepAliveDetected = 100
#******************************************#
# active verbose level
#******************************************#
verbose = getVerbose()
#******************************************#
#print to console, in the future to an logfile
#******************************************#
#def myPrint(level, text):
#    if verbose >= level:
#        print(str(datetime.datetime.now()) + " - " + text)

#************************************************#
# powermeter has an resolution from 1000 Imp/kWh
#************************************************#
def calcPower ():
    global count
    iPower = 0
    if (count > 0):
        iPower = (3600 * count)/ UPDATE_TIME
        if (iPower < 0):
            iPower = 0
    if verbose > 2:
        mySysLog.syslog(mySysLog.LOG_INFO, "calcPower: trigger = " + str(count) +" updateTime = " + str(UPDATE_TIME) + "s power= " + str(iPower) + "W")
    count = 0
    return iPower

#************************************************#
# keep alive entry in syslog
#************************************************#
def keepAlive():
    global ikeepAlive
    ikeepAlive+=1
    if (ikeepAlive >= keepAliveDetected):
        ikeepAlive = 0
        if (verbose > 0):
            mySysLog.syslog(mySysLog.LOG_INFO, str(keepAliveDetected) + " signal's received -> still alive ")

#************************************************#
# main routine
#************************************************#
def main():
    script=os.path.basename(__file__).split('.')[0]
    myPrint(STARTUP, (script + " is started"))

    try:
        while True:
            start = time.time()
            time.sleep(UPDATE_TIME)
            time_diff = time.time() - start
            myPrint (DEBUG, "Seconds= " + str(time_diff))
            power=calcPower()
            myPrint(INFO, "Power= " + str(power) + " W")
            sendPower2Influxdb.sendPower(power, "consume")
            sendPower2VZ.sendPower(power)
            #update influxdb with power value
    except KeyboardInterrupt:
        myPrint(WARN, (script + " stopped"))
        mySysLog.syslog(mySysLog.LOG_WARNING, "s0Power.py stopped ")        

#************************************************#
# define the threaded callback function
#************************************************#
def edgeDetected(channel):
    global count
    global e
    myPrint (DEBUG, "edge detected on GPIO " + str(channel))
    count+=1
    keepAlive()

#************************************************#
# configure GPIO 
#************************************************#
def configureInput():
    GPIO.setmode(GPIO.BCM)
    # GPIO 2 set up as input. It is internal pulled up
    GPIO.setup(INPUTNR, GPIO.IN)
    # The GPIO.add_event_detect() line below set things up so that  
    # when a falling edge is detected on port 2, regardless of whatever   
    # else is happening in the program, the function "my_callback" will be run  
    GPIO.add_event_detect(INPUTNR, GPIO.FALLING, callback=edgeDetected)

#If this file is being imported from another module, __name__ will be set to the module’s name.
#__name__ is a built-in variable which evaluates to the name of the current module.
# Using the special variable
# __name__
if __name__=="__main__":
    configureInput()
    main()