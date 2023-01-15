#!/usr/bin/python
#*******************************************#
# send value to an influxdb
#  commands in influx
#  use actvalues
#  select consume from Energy
#
#*******************************************#

from influxdb import client as influxdb
import datetime
import argparse
import sys

debug = 1

#InfluxDB Connection Details
influxHost = '192.168.24.120'
influxPort = '8086'
influxUser = 'admin'
influxPasswd = '19052001'
influxdbName = 'actvalues'

def myPrint(text):
	if debug:
		print(text)

def setVerbose():
    global debug
    debug = 1

#*******************************************#
# second parameter is optinally and default for consume:)
#*******************************************#
def sendPower(power, field='consume'):
    influx_metric = [{
        'measurement': 'Energy',
        'time': datetime.datetime.utcnow(),
        'units': 'Watt',
        'fields': {
            field: float(power)
        }
    }]
    #Saving data to InfluxDB
    try:
        db = influxdb.InfluxDBClient(influxHost, influxPort, influxUser, influxPasswd, influxdbName)
        result = db.write_points(influx_metric)
        myPrint("write to db successfully = " + str(result))
        myPrint(str(influx_metric))
    finally:
        db.close()

#checkinput arguments
parser = argparse.ArgumentParser(description='only -v or --verbose supported')
parser.add_argument("-v", '--verbose', type=int, nargs='?', help='with 1 or none debug is active, with 0 = debug isn\'t active ', default=0)
parser.add_argument("-f", '--force', type=float, nargs='?', help='force actual produce power', default=None)

inputArgs = parser.parse_args()
# printing input arguments
if inputArgs.verbose is None:
    debug = 1
#print('verbose:',inputArgs.verbose)
myPrint("Debug is active")



#print('id:',inputArgs.id)
#print("args=%s" % inputArgs)
#print("args.verbose=%s" % inputArgs.verbose)
#sys.exit()

def main():
    if inputArgs.force is not None:
        myPrint("force is active")
        sendPower(inputArgs.force)
        myPrint("finished")        

if __name__=="__main__":    
    main()



