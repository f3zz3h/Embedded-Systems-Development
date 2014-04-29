import rtsp, lcd, keypad

class client:
    def makePin(self, pinArr):
        """
        Take pinarray[4] and return str pin
        """
        keys = pinArr[0]
        for i in range(1,4):
            keys = keys * 10
            #now add new key value
            keys += pinArr[i]
        return str(keys)        
            
    
        
if __name__ == '__main__':
    clientMain = client()        
    clientRTSP = rtsp.RTSP()
    #clientLCD = lcd.LCD()
    clientKeypad = keypad.PIO()
     
    while(True):
            authorized = None
            pin = None
            
            #Enter pin to unlock keypad
            while(authorized is not True):
                #clientLCD.writeLCD(lcd.ENTER_PIN)
                num = clientKeypad.readWriteKeypad()
       
                for i in range(0,250):
                    clientKeypad.display(num)
                pin = clientMain.makePin(num)    
                       
                if (pin):
                    authorized = clientRTSP.auth( pin)      
            
            while(authorized is True): 
                ### TO GET BACK TO PIN ENTRY WE NEED SOME NEW LOGIC! 
                #clientLCD.writeLCD(lcd.ENTER_PIN)
                fid = clientKeypad.readWriteKeypad()
       
                for i in range(0,250):
                    clientKeypad.display(fid)
                fileid = clientMain.makePin(fid)   
                
                fileDir = clientRTSP.request(pin)
                try:
                    if (fileDir is None):
                        "Print invalid track, try again"
                        continue
                except:
                    print "Unable to compare to none"
                    continue
                #clientLCD.writeLCD(lcd.PLAY)
                clientRTSP.playAudio(fileDir, str(fileid)+'.mp3')
                
    #clientLCD.close