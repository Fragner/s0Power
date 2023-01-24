#************************************************#
#
# send power via curl post to vz
# example: url ="http://192.168.24.120:80/volkszaehler/htdocs/middleware.php/data/fd3aec80-ed45-11e3-834a-11f2a80cada3.json?ts=ts=1636135781457&value=60")
#
#************************************************#
import requests
from time import time
import sys
import os
from configparser import ConfigParser
import inputArgs
from myVerbose import *


user_agent="s0Power.py 0.3 - smarthome"

#As initialized upon program startup, the first item of this list, path[0], is the directory containing the script that was used to invoke the Python interpreter
os.chdir(sys.path[0])
#************************************************#
# definitions from ini file
#************************************************#
config = ConfigParser()
iniFile= 'power2VZ.ini'
config.read(iniFile)
server = config.get('vz','server')
path = config.get('vz', 'path')
channel = config.get('vz','channel')

printConfig(iniFile, config)
#myPrint(STARTUP, "ini-File :  " + iniFile)
#myPrint(INFO,"Sections: " + config.sections())
#for each_section in config.sections():
#    myPrint(STARTUP, "Section:=" + each_section)
#    for (each_key, each_val) in config.items(each_section):
#        myPrint(STARTUP, each_key + "= " + each_val)
 
#************************************************#
# send power via curl post to vz
#************************************************#
def sendPower(value):
    milliseconds = int(time() * 1000)
    iValue = int(value)
    url = server + path + "data/" + channel+ ".json?ts="+ str(milliseconds)+ "&value=" + str(iValue)
    headers = {
    'User-Agent': user_agent
    }
    resp = requests.post(url,headers=headers)
    if (resp.status_code == 200):
        myPrint(INFO, "write to volkzszaehler successfully = " + str(url))
    myPrint (DEBUG, resp.status_code)
    myPrint (DEBUG, resp.content)
    myPrint (DEBUG, resp)

#************************************************#
# main routine
#************************************************#
def main():
    if inputArgs.inputArgs.verbose is None:
        setDebug(inputArgs.inputArgs.verbose)
    if inputArgs.inputArgs.force is not None:
        myPrint(DEBUG, "force is active")
        sendPower(inputArgs.inputArgs.force)
        myPrint(INFO, "finished")
    else:
        myPrint(INFO,"noting to do")
#    value= 880
 #   if (len(sys.argv) > 1):
#        value= sys.argv[1]
#    sendPower(value)

#************************************************#
# call main only, when file started alone --> eg, by cli
# not when imported into an other file
#************************************************#
if __name__=="__main__":
    main()