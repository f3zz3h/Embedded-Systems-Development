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
import threading
from subprocess import Popen,PIPE
import sys
import keypad
import lcd
import time

TENSECS = 10000000000
VOLMAX = 400
VOLMIN = -3000
VOLMUTE = -10000
gtk.gdk.threads_init()

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
        self.test = False
        self.volume = 0
        self.player = gst.element_factory_make("playbin", "player")
        fakesink = gst.element_factory_make('fakesink', "my-fakesink")
        self.player.set_property("video-sink", fakesink)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect('message',self.onmessage)

        log = Popen(['amixer', 'set', 'PCM','--', str(self.volume)],stdout=PIPE)

    def onmessage(self,bus,message):
        if message.type == gst.MESSAGE_EOS:
            self.index += 1
        if message.type == gst.MESSAGE_TAG:
            dogs = message.parse_tag()
        
    def controlFunc(self, playbackControls, display):
        time.sleep(3)
        print "Thread reached"
        print self.test
        if self.test:
            print "Playing"
            display.writeLCD(lcd.PLAY)
        #Wait till stream begins playing before allowing playback controls
        #while (self.player.get_state() != gst.STATE_PLAYING):
        #    print "gst state is not playing"
        #    time.sleep(0.5)
        
        while self.test:
            print "Playback controls"  
            chArr = playbackControls.readWriteKeypad(1,False)
            ch = chArr[0]
            if ch==keypad.REWIND:
                display.writeLCD(lcd.REWIND)
                pos = self.player.query_position(gst.FORMAT_TIME, None)[0]
                if pos >= TENSECS:   
                    pos -= TENSECS
                else:
                    pos = 0
                self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, pos)
                time.sleep(0.25)
                display.writeLCD(lcd.PLAY)
            elif ch==keypad.FFWD:
                display.writeLCD(lcd.FAST_FORWARD)
                pos = self.player.query_position(gst.FORMAT_TIME, None)[0]
                length = self.player.query_duration(gst.FORMAT_TIME, None)[0]
                
                if pos+TENSECS >= length:
                    pos = length
                else:
                    pos += TENSECS
                self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, pos)
                time.sleep(0.25)
                display.writeLCD(lcd.PLAY)
            elif ch==keypad.STOP:
                display.writeLCD(lcd.STOP)
                self.player.set_state(gst.STATE_NULL)
                test=False
                time.sleep(0.2)
                gtk.main_quit()
            elif ch==keypad.VOLUP: #vol up
                self.volume += 100
                if self.volume > VOLMAX:
                    self.volume = VOLMAX
                display.writeLCD(lcd.VOLDOWN,str(self.volume))
                log = Popen(['amixer', 'set', 'PCM','--', str(self.volume)],stdout=PIPE)
                time.sleep(0.25)
                display.writeLCD(lcd.PLAY)
            elif ch==keypad.VOLDOWN: # vol down
                self.volume -= 100
                if self.volume < VOLMIN:
                    self.volume = VOLMIN
                display.writeLCD(lcd.VOLDOWN,str(self.volume))
                log = Popen(['amixer', 'set', 'PCM','--', str(self.volume)],stdout=PIPE)
                time.sleep(0.25)
                display.writeLCD(lcd.PLAY)
            elif ch==keypad.MUTE: # vol down
                display.writeLCD(lcd.MUTE)
                log = Popen(['amixer', 'set', 'PCM','--', str(VOLMUTE)],stdout=PIPE)                
            elif ch==keypad.PAUSE: #pause
                display.writeLCD(lcd.PAUSE)
                if self.player.get_state()[1] == gst.STATE_PLAYING:
                    self.player.set_state(gst.STATE_PAUSED)
            elif ch==keypad.PLAY: #play
                display.writeLCD(lcd.PLAY)
                if self.player.get_state()[1] == gst.STATE_PAUSED:
                    self.player.set_state(gst.STATE_PLAYING)
                
                
            if (self.player.get_state()[1] == gst.STATE_NULL):
                test = False
                time.sleep(0.2)
                gtk.main_quit()
            time.sleep(.05)

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
        
        #Create rtsp url for passing to gstreamer 
        rtspURL = 'rtsp://'+self.serverURL+':'+ self.serverPORT+'/'
        #create a grestreamer player and with correct pipeline
        self.player = gst.parse_launch('rtspsrc location = '+ rtspURL + fileLocation + 
                                  fileName + ' ! rtpmpadepay ! mad ! alsasink sync=false')
        #Set state to playing
        self.player.set_state(gst.STATE_PLAYING)
        
        if (self.player.get_state()[1] != gst.STATE_PLAYING):
            self.test = False
            return False
        self.test = True
        #start gtk thread
        gtk.main()