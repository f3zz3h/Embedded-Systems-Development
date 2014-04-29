import pygst
pygst.require('0.10')
import gst
import pygtk
pygtk.require('2.0')
import gtk
import telnetlib

# this is very important, without this, callbacks from gstreamer thread
# will mess our program up

class RTSP:
    def __init__(self):
        #Server URL including port
        self.serverURL = 'gold.riotnet.co.uk' #:8554/
        self.serverPORT = '8554'
        self.tn = telnetlib.Telnet(self.serverURL,self.serverPORT)

    def auth(self, pin):
        self.tn.write("AUTH * RTSP/1.0\r\n")
        self.tn.write("CSeq: 2\r\n")
        self.tn.write("Pin: " + pin + "\r\n\r\n")
        #print 
        self.tn.read_until("!", 2)
        
        return True
    def request(self, pin):   
        self.tn.write("REQUEST * RTSP/1.0\r\n")
        self.tn.write("CSeq: 2\r\n")
        self.tn.write("Pin: " + pin + "\r\n\r\n")
        self.tn.read_until("URL: ",2)
        retval = self.tn.read_until("\r\n", 2)
        if retval:
            return retval.rstrip()
        else:
            print "invalid response"
            return None

    def playAudio(self,fileLocation, fileName ):
        gtk.gdk.threads_init() 
        rtspURL = 'rtsp://'+self.serverURL+':'+ self.serverPORT+'/'
        player = gst.parse_launch('rtspsrc location = '+ rtspURL + fileLocation + 
                                  fileName + ' ! rtpmpadepay ! mad ! alsasink sync=false') 
        player.set_state(gst.STATE_PLAYING)
        gtk.main()
    