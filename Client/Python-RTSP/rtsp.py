__author__ = "Luke Hart"
__copyright__ = "Copyright 2014, The Jeff Museum"
__credits__ = ["Luke Hart","Joe Ellis", "Chris Sewell", "Matt Ribbins",
               "Sebastian Beaven", "Joshua Webb", "Andrew Bremmer"]
__license__ = "GPL"
__version__ = "0.9"
__maintainer__ = "Luke Hart"
__email__ = "luke2.hart@live.uwe.ac.uk"
__status__ = "Development"

import pygst
pygst.require('0.10')
import gst
import pygtk
pygtk.require('2.0')
import gtk
import telnetlib

class RTSP:
    """
    The RTSP class handles Auth, Deauth and File Location
    aquisition. It also contains the gstreamer call for streaming
    the audio, the only true RTSP usage.
    """
    def __init__(self):
        """
        Setup telnet ports and connection
        """
        self.serverURL = 'gold.riotnet.co.uk' #:8554/
        self.serverPORT = '8554'
        self.tn = telnetlib.Telnet(self.serverURL,self.serverPORT)

    def auth(self, pin):
        """
        Authorize a handset based on pin entered into the keypad
        and return True/False if success/fail
        """
        #Build telnet request and send to server
        self.tn.write("AUTH * RTSP/1.0\r\n")
        self.tn.write("CSeq: 2\r\n")
        self.tn.write("Pin: " + pin + "\r\n\r\n")

        #Get server response 
        retval = self.tn.read_until("!", 1)
        
        #Return true false based on retval
        if ('OK' in retval):
            return True
        else:
            return False

    def request(self, pin):   
        """
        Request file location based on keypad pin entry representing
        a display number.
        """
        #Build telnet request
        self.tn.write("REQUEST * RTSP/1.0\r\n")
        self.tn.write("CSeq: 2\r\n")
        self.tn.write("Pin: " + pin + "\r\n\r\n")
        #Read response till the start of the url and ignore it
        self.tn.read_until("URL: ",1)
        #Read rest of response store in retval as this is our directory
        retval = self.tn.read_until("\r\n", 1)
        #Return the url stripped of any whitespace and newline chars
        if retval:
            return retval.rstrip()
        else:
            return None

    def playAudio(self,fileLocation, fileName ):
        """
        Use gstreamer to play an audio file
        Params: fileLocation - url from request
                fileName - pin from request
        """
        #Create gtk thread
        gtk.gdk.threads_init()
        #Create rtsp url for passing to gstreamer 
        rtspURL = 'rtsp://'+self.serverURL+':'+ self.serverPORT+'/'
        #create a grestreamer player and with correct pipeline
        player = gst.parse_launch('rtspsrc location = '+ rtspURL + fileLocation + 
                                  fileName + ' ! rtpmpadepay ! mad ! alsasink sync=false')
        #Set state to playing 
        player.set_state(gst.STATE_PLAYING)
        #start gtk thread
        gtk.main()
    