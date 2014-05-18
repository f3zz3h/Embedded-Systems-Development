__author__ = "Luke Hart"
__copyright__ = "Copyright 2014, The Jeff Museum"
__credits__ = ["Luke Hart","Joe Ellis", "Chris Sewell", "Matt Ribbins",
               "Sebastian Beaven", "Joshua Webb", "Andrew Bremmer"]
__license__ = "GPL"
__version__ = "0.9"
__maintainer__ = "Luke Hart"
__email__ = "luke2.hart@live.uwe.ac.uk"
__status__ = "Development"

import serial
import time
import io
import math


#Defined values 
TTY = '/dev/ttyACM0'
BAUD = 115200
START = '@00'
END = '\r'
A = 0
B = 1
C = 2
OUTPUT = 0
INPUT = 1

#Input / Output - A - Both B - KeyPad C - 7 SEG LEDS  
PORTABC_INPUT = ['@00D0FF\r','@00D1FF\r', '@00D2FF\r']
PORTABC_OUTPUT = ['@00D000\r','@00D100\r', '@00D200\r'] 

#Select column
SELECT_COLUMN = ['@00P001\r','@00P002\r','@00P004\r','@00P008\r'] 
CHECK_BUTTON = '@00P1?\r'

#Button defined names
BACK = 10
DOWN = 11
ACCEPT = 12
REWIND = 13
STOP = 0
PLAY = 14
FFWD = 15
VOLUP = 6
VOLDOWN = 9
PAUSE = 8
MUTE = 1
KEYPAD = [[ 1 ,2 ,3 ,10 ],
          [ 4 ,5 ,6 ,11 ],
          [ 7 ,8 ,9 ,12 ],
          [ 13,0 ,14,15 ]]


class PIO:
    """
    The pio class handles the IO through the BMCM USB-PIO
    to the keypad and 7segment display array.
    """
    def __init__(self):
        """
        Intialize the serial port and create a TextIO serial IO port
        which allows readline based on the PIO EOL of /r
        """
        self.ser = serial.Serial(TTY, baudrate=BAUD, timeout=1)
        self.port_setup(A, OUTPUT)
        time.sleep(0.2)
        self.port_setup(B, INPUT)
        time.sleep(0.2)
        self.port_setup(C, OUTPUT)
        time.sleep(0.2)
        
        self.ser_io = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser, 1),  
                              newline = '\r',
                             line_buffering = True)
        self.ser_io.readlines()   

    def port_setup(self, port, io):
        """
        Set ports to input output based on param io
        """
        if (io == OUTPUT): 
            self.ser.write(PORTABC_OUTPUT[port])
        elif (io == INPUT):
            self.ser.write(PORTABC_INPUT[port])
        
    def write(self,cmd):
        """
        Write cmd param to the serial port and return the
        response to the writing unedited
        """
        self.ser_io.flush()
        self.ser_io.write(unicode(cmd))
        
        retval = self.ser_io.readline()
        
        self.ser_io.flush()
        return retval
    
    def setup_display(self, display):
        """
        Clear the seven seg display and select
        the appropriate column for displaying based from
        the display param 
        """
        # Clear first
        self.write('@00P200\r') 
        
        # now select output display
        self.write(SELECT_COLUMN[display]) 
        

    def display(self, num):
        """
        params: num[4] array of size 4 which takes numbers from 0-9 for each lcd item
        ToDo: Could just be a number 0-9999 and be broken into components but for now
        this works
        """

        #for x in range(0, 10):
        for ssd in range (0,4):
            self.setup_display(ssd)
            self.write('@00P2' + self.ledSwitch(str(num[ssd])) + END )         
                
        #Clear display at finish
        for disp in range (0,4):
            self.setup_display(disp)
              
    def close(self):
        """
        Close the serial connections
        """
        self.ser_io.close()
        self.ser.close()
        
    def keypad_read(self):
        """
        Get and array of 4 numbers representing the cols 
        on the keypad and return them.
        """
        keys = [0,0,0,0]
        #loop for each column
        for i in range(0,4):
            self.write(SELECT_COLUMN[i])
            
            key = self.write(CHECK_BUTTON)
            
            #Strip white space and preceeding !        
            key = key.lstrip('!')
            key = key.rstrip()

            #Check key isnt 0      
            if(int(key) != 0): 
                keys[i] = int(key)
        return keys
    def ledSwitch(self, choice):
        """
        Decimal to 7 segment displays value, switch based on 
        the param choice and return the hex value
        """
        return {
            '0' : '3f', '1' : '06', '2' : '5B',
            '3' : '4f', '4' : '66', '5' : '6D',
            '6' : '7D', '7' : '07', '8' : '7F',
            '9' : '6F', 'A' : '77', 'B' : '7C',
            'C' : '39', 'D' : '5E', 'E' : '79',
            'F' : '71', '.' : '80', ' ' : '00'
        }[choice]
    def keypadSwitch(self, column, value):
        """
        Return a keypad value from the keypad table
        """
        try: 
            keyPress = KEYPAD[int(math.log(value,2))][column]              
            return keyPress
        except:
            return None
        
    def readWriteKeypad(self, numberOfValues=4, numOnly=True):
        """
        Read keypad one number at a time and display each value
        """
        output = [' ',' ',' ',' ']
        #Loop once for each number required
        for sseg in range(0,numberOfValues):
            output[sseg] = '.'
            #Clear any left overs from previous run!         
            self.ser_io.readlines()      
            gotNum = False 
            while(gotNum == False):
                #get col values and check each for a key press
                keys = self.keypad_read()
                for col in range (0,4):
                    #Make sure a button and only one button is pressed
                    if ((keys[col] > 0) and (keys[col] < 9)):
                        if (( ((keys[col] % 2) == 0) or (keys[col] == 1) ) and (keys[col] != 6) ):
                                output[sseg] = self.keypadSwitch(col, keys[col])
                                if (numOnly == True):
                                    if ((output[sseg] >= 0) and (output[sseg] < 10)):
                                        gotNum = True                
                                        break  
                                    else:
                                        output[sseg] = '.'
                                else:
                                    gotNum = True
                                    break
                    self.display(output)
        return output