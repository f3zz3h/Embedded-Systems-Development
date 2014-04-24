#!/usr/bin/env python

import pygst
pygst.require('0.10')
import gst
import time
import pygtk
pygtk.require('2.0')
import gtk
import sys
import getpass
import telnetlib

# this is very important, without this, callbacks from gstreamer thread
# will mess our program up
gtk.gdk.threads_init()

#Server URL including port
serverURL = 'gold.riotnet.co.uk' #:8554/
serverPORT = '8554'
rtspURL = 'rtsp://'+serverURL+':'+serverPORT+'/'
def readKeypad(numberOfChars):
    keys = 0
    for i in (1, numberOfChars):
        #read keypad
        #Times current value by 10 to move left by one
        keys = keys * 10
        #now add new key value
        keys += i
    return keys        
        
def getFileIdFromKeypad():
    return 99 #'hk9' + '.mp3' ##99
def getPinFromKeypad():
    ## READING FROM KEYPAD HERE
    #return (str)1007
    return str(input("Enter pin:"))
def auth(tn, pin):
    tn.write("AUTH * RTSP/1.0\r\n")
    tn.write("CSeq: 2\r\n")
    tn.write("Pin: " + pin + "\r\n\r\n")
    print tn.read_until("!", 2)
    success = True
    return success
def request(tn, pin):   
    tn.write("REQUEST * RTSP/1.0\r\n")
    tn.write("CSeq: 2\r\n")
    tn.write("Pin: " + pin + "\r\n\r\n")
    tn.read_until("URL: ",2)
    retval = tn.read_until("\r\n", 2)
    if retval:
        return retval
    else:
        print "invalid response"
        return -1 
def writeLCD(msg):
    print msg
def playAudio(fileLocation, fileName ):
        print fileLocation
    	player = gst.parse_launch('rtspsrc location = '+ rtspURL + fileLocation + fileName + ' ! rtpmpadepay ! mad ! alsasink sync=false') 
    	player.set_state(gst.STATE_PLAYING)
    	gtk.main()

if __name__ == '__main__':
    
    tn = telnetlib.Telnet(serverURL,serverPORT)
    while(True):
        authorized = None
        pin = None
        
        #Enter pin to unlock keypad
        while(authorized is not True):
            writeLCD("Please enter a pin")
            pin = getPinFromKeypad()
            if (pin):
                authorized = auth(tn, pin)      
        
        while(authorized is True):  
            fileid = getFileIdFromKeypad()
            
            fileDir = request(tn, pin)
                     
            print "Starting Steam"
            playAudio(fileDir, str(fileid) + '.mp3')
        
        
        