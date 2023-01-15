#************************************************#
#
# send power via curl post to vz
# example: url ="http://192.168.24.120:80/volkszaehler/htdocs/middleware.php/data/fd3aec80-ed45-11e3-834a-11f2a80cada3.json?ts=ts=1636135781457&value=60")
#
#************************************************#
import requests
from time import time
import sys
import inputArgs


user_agent="s0Power2vz.py 0.1 - smarthome"

debug= 0
milliseconds = int(time() * 1000)
#print("now= "+ str(milliseconds))
#************************************************#
# definitions --> ToDo: move to an ini file
#************************************************#
# Hostaddress WITH port, FQDN or IP of your VZ - normaly this should be 'http://localhost:80'
server = "http://192.168.24.120:80"# --> send it to a remote host
# Path to the VZ middleware.php script, WITH preposed and trailing slash */
#path = "middleware.php";
path = "/volkszaehler/htdocs/middleware.php/";
#channel
channel = "fd3aec80-ed45-11e3-834a-11f2a80cada3" # power consumption
#************************************************#
#************************************************#
def setDebug():
    global debug
    debug = 1

def myPrint(text):
	if debug:
		print(text)

#************************************************#
# send power via curl post to vz
#************************************************#
def sendPower(value):
    url = server + path + "data/" + channel+ ".json?ts="+ str(milliseconds)+ "&value=" + str(value)
    headers = {
    'User-Agent': user_agent
    }
    resp = requests.post(url,headers=headers)
    myPrint (resp.status_code)
    myPrint (resp.content)
    myPrint (resp)

#************************************************#
# main routine
#************************************************#
def main():
    global debug
    if inputArgs.inputArgs.verbose is None:
        setDebug()
    if inputArgs.inputArgs.force is not None:
        myPrint("force is active")
        sendPower(inputArgs.inputArgs.force)
        myPrint("finished")
    else:
        myPrint("noting to do")
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