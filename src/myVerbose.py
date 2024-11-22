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
#with starting / !!!
iniFile= 'config/verbose.ini'

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
    #full_path = os.path.realpath(__file__)
    #print("load_config " + full_path)
    
    path = os.path.dirname(os.path.abspath(__file__))
    #print(path)
    os.chdir(path)

    #os.chdir(sys.path[0])
    #print(os.getcwd())
    #go "up", away from src
    os.chdir('../')
    #print(os.getcwd())
    config = ConfigParser()
    file_path = os.path.join(os.getcwd(), relative_path)
    #print(file_path)    

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

config = load_config(iniFile)
verbose = config.getint('debug','verbose')

#https://realpython.com/python-logging/
logging.basicConfig(filename='/var/log/myLogs/s0Power.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',level=getLogLevel(verbose))

printConfig(iniFile, config)



