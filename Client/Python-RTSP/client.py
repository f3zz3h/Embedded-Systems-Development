__author__ = "Luke Hart"
__copyright__ = "Copyright 2014, The Jeff Museum"
__credits__ = ["Luke Hart","Joe Ellis", "Chris Sewell", "Matt Ribbins",
               "Sebastian Beaven", "Joshua Webb", "Andrew Bremmer"]
__license__ = "GPL"
__version__ = "0.9"
__maintainer__ = "Luke Hart"
__email__ = "luke2.hart@live.uwe.ac.uk"
__status__ = "Development"

import threading
import rtsp, lcd, keypad

class client:
    def makePin(self, pinArr):
        """
        Take pinarray[4] and return str pin
        """
        #First number from array
        keys = pinArr[0]
        #Loop for rest of numbers in array
        for i in range(1,4):
            #Move number left making space for next number
            keys = keys * 10
            #now add new key value
            keys += pinArr[i]
        return str(keys)        
        
if __name__ == '__main__':
    """
    Starting point for the client application which contains the
    primary system loop.
    """
    
    #Instantiate client classes
    clientMain = client()        
    clientRTSP = rtsp.RTSP()
    clientLCD = lcd.LCD()
    clientKeypad = keypad.PIO()
    
    #Overall system loop. Will never exit unless system shutdown 
    while(True):
            authorized = None
            pin = None
            
            #Loop until a Valid pin is received to use the device
            while(authorized is not True):
                clientLCD.writeLCD(lcd.ENTER_PIN)
                
                #Aquire pin number from keypad
                num = clientKeypad.readWriteKeypad() 
       
                #Display finished number for quarter of a second
                for i in range(0,250):
                    clientKeypad.display(num)
                
                #Convert our array into a string value 
                pin = clientMain.makePin(num)    
                authorized = True
                #Attempt to authorize client device       
                if (pin):
                    authorized = clientRTSP.auth( pin)      
            
            #Loop until Deauthorized
            while(authorized is True): 
                
                #Out LCD message
                clientLCD.writeLCD(lcd.ENTER_DISPLAY_NUMBER)
                
                #Get file id from keypad
                fid = clientKeypad.readWriteKeypad()
       
                #Display number on keypad for quarter of a second
                for i in range(0,250):
                    clientKeypad.display(fid)
                
                #Make array a string    
                fileid = clientMain.makePin(fid)   
                
                #Request audio location
                fileDir = clientRTSP.request(pin)
                
                #Check a valid directory is received
                try:
                    if (fileDir is None):
                        "Print invalid track, try again"
                        continue
                except:
                    print "Unable to compare to none"
                    continue
                #Write LCD with status and start playing streamed audio
                clientLCD.writeLCD(lcd.PLAY)
                thread = threading.Thread(target=clientRTSP.controlFunc(),args=(clientKeypad,))
                thread.start()
                clientRTSP.playAudio(fileDir, str(fileid)+'.mp3')
                thread.join()
