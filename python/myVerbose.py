import datetime
from configparser import ConfigParser
import os
import sys
import logging
#******************************************#
# defined vebose level
#******************************************#
STARTUP = 0
ERROR = 1
WARN = 2
INFO = 3
DEBUG = 4


verbose= 0
os.chdir(sys.path[0])
#************************************************#
#
#************************************************#
def getVerboseName(level):
    if level == ERROR:
        levelName = "ERROR"
    elif level == DEBUG:
        levelName = "DEBUG"
    elif level == INFO:
        levelName = "INFO"
    elif level == STARTUP:
        levelName = "STARTUP"
    else:
        levelName = "WARN"
    return levelName

#************************************************#
#
#************************************************#
def myPrint(level, text):
    if verbose >= level:
        print(str(datetime.datetime.now()) + ": " + getVerboseName(level) + " - "+ text)

    if level == ERROR:
        logging.error(text)
    elif level == DEBUG:
        logging.debug(text)
    elif level == INFO:
        logging.info(text)        
    elif level == STARTUP:
        logging.critical(text)
    else:
        logging.warning(text)  
    
#************************************************#
#
#************************************************#
def printConfig(iniFile, config):
    myPrint(STARTUP, "iniFile:  " + iniFile)
    for each_section in config.sections():
        myPrint(STARTUP,"SECTION: " +each_section)
        for (each_key, each_val) in config.items(each_section):
            myPrint(STARTUP, "   " + each_key + "= " + each_val)
#************************************************#
#
#************************************************#
def getVerbose():
    return verbose
#************************************************#
#
#************************************************#
def setVerbose(level):
    global verbose
    verbose = level
#************************************************#
#
#************************************************#
def getLogLevel(level):
    #WARN is the default
    if level == ERROR:
        loglevel = logging.ERROR
    elif level == DEBUG:
        loglevel = logging.DEBUG
    elif level == INFO:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARN
    return loglevel
#************************************************#
# definitions from ini file
#************************************************#
config = ConfigParser()
iniFile= 'verbose.ini'
config.read(iniFile)
verbose = config.getint('debug','verbose')

#https://realpython.com/python-logging/
logging.basicConfig(filename='/var/log/myLogs/s0Power.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',level=getLogLevel(verbose))

printConfig(iniFile, config)



