import pygst
pygst.require('0.10')
import gst
import time
import pygtk
pygtk.require('2.0')
import gtk

# this is very important, without this, callbacks from gstreamer thread
# will messed our program up
gtk.gdk.threads_init()

def main():
    	player = gst.parse_launch('rtspsrc location = "rtsp://gold.riotnet.co.uk:8554/hk9.mp3" ! rtpmpadepay ! mad ! alsasink sync=false') 
    	player.set_state(gst.STATE_PLAYING)
    	gtk.main()


print "Hi Jeff, We are streaming you some musics for our demo"
main()
print "Thanks for listening, BYE!"

time.sleep(2)

print "FULL MARKS FOR EVERYBODY!!!"
