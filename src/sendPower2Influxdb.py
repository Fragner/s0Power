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
import os
from configparser import ConfigParser
from myVerbose import *


iniFile= 'config/power2Influxdb.ini'

#************************************************#
# definitions from ini file
# InfluxDB Connection Details
#************************************************#
config = load_config(iniFile)

server = config.get('influx','server')
port = config.get('influx', 'port')
user = config.get('influx','user')
passwd = config.get('influx', 'passwd')
dbName = config.get('influx', 'dbName')
printConfig(iniFile, config)

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
        db = influxdb.InfluxDBClient(server, port, user, passwd, dbName)
        result = db.write_points(influx_metric)
        myPrint(INFO,"write to inflxudb successfully = " + str(result))
        myPrint(DEBUG,str(influx_metric))
    finally:
        db.close()


def main():
    #checkinput arguments
    parser = argparse.ArgumentParser(description='only -v or --verbose supported')
    parser.add_argument("-v", '--verbose', type=int, nargs='?', help='with 1 or none debug is active, with 0 = debug isn\'t active ', default=0)
    parser.add_argument("-f", '--force', type=float, nargs='?', help='force actual produce power', default=None)

    inputArgs = parser.parse_args()
    # printing input arguments
    if inputArgs.verbose is not None:
        setVerbose(inputArgs.verbose)
    #print('verbose:',inputArgs.verbose)
    myPrint(DEBUG, "Debug is active")

    if inputArgs.force is not None:
        myPrint(DEBUG,"force is active")
        sendPower(inputArgs.force)
        myPrint(DEBUG,"finished")        

if __name__=="__main__":    
    main()



