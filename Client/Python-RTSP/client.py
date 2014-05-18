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
import time

class client:
    def makePin(self, pinArr):
        """
        Take pinarray[4] and return str pin
        """
        #First number from array
        keys = str(pinArr[0])
        #Loop for rest of numbers in array
        for i in range(1,4):
            #Move number left making space for next number
            keys += str(pinArr[i])
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
                for i in range(0,20):
                    clientKeypad.display(num)
                
                #Convert our array into a string value 
                pin = clientMain.makePin(num)    
                authorized = True
                print pin
        
                #Attempt to authorize client device       
                if (pin):
                    authorized = clientRTSP.auth(pin)
                    
                if (authorized):
                    clientLCD.writeLCD(lcd.ACCEPTED_PIN)
                else:
                    clientLCD.writeLCD(lcd.INVALID_PIN)
            
            #Loop until Deauthorized
            while(authorized is True): 
                
                #Out LCD message
                clientLCD.writeLCD(lcd.ENTER_DISPLAY_NUMBER)
                
                #Get file id from keypad
                fid = clientKeypad.readWriteKeypad()
       
                #Display number on keypad for quarter of a second
                for i in range(0,20):
                    clientKeypad.display(fid)
                
                #Make array a string    
                fileid = clientMain.makePin(fid)   
                
                #Request audio location
                fileDir = clientRTSP.request(pin)
                
                print fileDir
                #Check a valid directory is received
                try:
                    if (fileDir is None):
                        continue
                except:
                    clientLCD.writeLCD(lcd.INVALID_DISPLAY_NUMBER)
                    continue
                
                clientLCD.writeLCD(lcd.FETCH_DISPLAY_NUMBER)
                
                #Write LCD with status and start playing streamed audio
                thread = threading.Thread(target=clientRTSP.controlFunc,args=(clientKeypad,clientLCD,))
                thread.start()
                if (clientRTSP.playAudio(fileDir, str(fileid)+'.mp3') == False):
                    clientLCD.writeLCD(lcd.INVALID_DISPLAY_NUMBER)
                thread.join()
