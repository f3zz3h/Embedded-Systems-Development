import pygst
pygst.require('0.10')
import gst
import time
import pygtk
pygtk.require('2.0')
import gtk
import rdt
import sys
from twisted.internet import reactor
from rtsp import RTSPClient, RTSPClientFactory
from twisted.python import failure, log

# this is very important, without this, callbacks from gstreamer thread
# will mess our program up
gtk.gdk.threads_init()

#Server URL including port
serverURL = 'rtsp://gold.riotnet.co.uk:8554/' #:8554/

def getFileIdFromKeypad():
    return 'hk9' + '.mp3'
def getPinFromKeypad():
    return 1007
def playAudio(fileLocation, fileName):
    	player = gst.parse_launch('rtspsrc location = serverURL + fileLocation + fileName ! rtpmpadepay ! mad ! alsasink sync=false') 
    	player.set_state(gst.STATE_PLAYING)
    	gtk.main()

if __name__ == '__main__':
    
    #Enter pin to unlock keypad
    pin = getPinFromKeypad()
    ##UNLOCK METHOD HERE
    
    #while(1)
    
    fileid = getFileIdFromKeypad()
        
    ###    
    log.startLogging(sys.stdout)
    factory = RTSPClientFactory(serverURL + fileid, 'TESTER', pin) 
    factory.protocol = rdt.RDTClient
    factory.bandwidth = 99999999999
    factory.deferred.addCallback(rdt.success).addErrback(rdt.error)
    reactor.connectTCP(factory.host, factory.port, factory)
    reactor.callLater(1, rdt.progress, factory)
    reactor.run()

    #factory.
    print "Start Steam"
    #ToDo: Add file  instead of hardcoded value over hk9.mp3
    #playAudio(dir, id)
    print "Thanks for listening, BYE!"

    time.sleep(2)
    print "FULL MARKS FOR EVERYBODY!!!"
