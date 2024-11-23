import datetime
from configparser import ConfigParser
import os
import sys
import logging
import time
#******************************************#
# defined vebose level
#******************************************#
STARTUP = 0
ERROR = 1
WARN = 2
INFO = 3
DEBUG = 4


verbose= 2
#not with starting / !!!
iniFile = 'config/verbose.ini'
logFile = '/var/log/myLogs/s0Power.log'

#************************************************#
# configure logger with level NOTSET --> ALL
# call from logger will be controlled by verbose 
#************************************************#
logging.basicConfig(filename=logFile, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)

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
#https://www.iditect.com/faq/python/how-to-load-relative-config-file-using-configparser-from-subdirectory.html
#************************************************#
def load_config(relative_path):
    myPrint(DEBUG, "load_config " + os.path.realpath(__file__))
    path = os.path.dirname(os.path.abspath(__file__))
    myPrint(DEBUG, path)
    os.chdir(path)
    #go "up", away from src
    os.chdir('../')
    myPrint(DEBUG, os.getcwd())
    config = ConfigParser()
    file_path = os.path.join(os.getcwd(), relative_path)
    myPrint(DEBUG, file_path)    

    if (os.path.isfile(file_path)):
        config.read(file_path)
    elif os.path.isfile(file_path+".default"):
        myPrint(WARN, "default ini-file used: " + relative_path+".default") 
        config.read(file_path+".default")
    else:
        myPrint(ERROR, "ini-file not found: " + relative_path) 
        sys.exit(-1)       
    
    return config
#************************************************#
#
#************************************************#
def myPrint(level, text):
    if verbose >= level:
        #pribt to console
        print(str(datetime.datetime.now()) + ": " + getVerboseName(level) + " - "+ text)

    #logging into logFile
    if level == ERROR:
        logging.error(text)
    elif level == DEBUG:
        logging.debug(text)
    elif level == INFO:
        logging.info(text)        
    elif level == STARTUP:
        logging.info(text)
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
    if level == ERROR:
        loglevel = logging.ERROR
    elif level == DEBUG:
        loglevel = logging.DEBUG
    elif level == INFO:
        loglevel = logging.INFO
    elif level == WARN:
        loglevel = logging.WARN
    else:
        loglevel = logging.NOTSET
    return loglevel
#************************************************#
# get definitions from ini file
#************************************************#
config = load_config(iniFile)
verbose = config.getint('debug','verbose')
printConfig(iniFile, config)

#************************************************#
# define logging -  output and format
#https://realpython.com/python-logging/
#************************************************#
#logging.basicConfig(filename='/var/log/myLogs/s0Power.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',level=getLogLevel(verbose))
