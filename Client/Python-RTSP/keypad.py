import serial
import time
import io
import threading

TTY = '/dev/ttyACM0'
BAUD = 115200

START = '@00'
END = '\r'
A = 0
B = 1
C = 2
OUTPUT = 0
INPUT = 1
#A - Both B - KeyPad C - 7 SEG LEDS  
PORTABC_INPUT = ['@00D0FF\r','@00D1FF\r', '@00D2FF\r']
PORTABC_OUTPUT = ['@00D000\r','@00D100\r', '@00D200\r'] 

SELECT_COLUMN = ['@00P001\r','@00P002\r','@00P004\r','@00P008\r'] #select first column
#"@00P23F\r" write hex code for a 0
CHECK_BUTTON = '@00P1?\r'


class PIO:
    def __init__(self):
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

    def port_setup(self, port, io):
        if (io == OUTPUT): 
            self.ser.write(PORTABC_OUTPUT[port])
        elif (io == INPUT):
            self.ser.write(PORTABC_INPUT[port])
        else:
            print "Invalid IO choice"
        
    def write(self,cmd):
        ##Should error check
        self.ser_io.write(unicode(cmd))
        self.ser_io.flush()
        return self.ser_io.readline()  
    
    def setup_display(self, display):
        # Clear first
        self.write('@00P200\r') 
        time.sleep(0.0001)
        # now select output display
        self.write(SELECT_COLUMN[display]) 
        time.sleep(.001)
        
    # 
    def display(self, num):
        """
        params: num[4] array of size 4 which takes numbers from 0-9 for each lcd item
        ToDo: Could just be a number 0-9999 and be broken into components but for now
        this works
        """
        x = 0
        ssd = 0
                   
        #Write values for appox 1 second
        for x in range(0, 100):
            for ssd in range (0,4):
                self.setup_display(ssd)
                self.write('@00P2' + self.ledSwitch(str(num[ssd])) + END )
                #Change this value for slower platfroms.. this is for a fast pc.. try 0.0001 for rpi to start with
                time.sleep(0.005)
                
        #Clear display at finish
        for disp in range (0,4):
            self.setup_display(disp)
            time.sleep(0.1)
                 
        
    def close(self):
        self.ser.close()
    def keypad_read(self):
        keys = [0,0,0,0]
        for i in range(0,4):
            self.write(SELECT_COLUMN[i])
            time.sleep(0.001)
            key = self.write(CHECK_BUTTON)
            time.sleep(0.001)
            #keyInit = self.ser_io.readlines()
            self.ser_io.flush()
            
            key = key.lstrip('!')
            key = key.rstrip()
                                   
            try:
                if(int(key) != 0): 
                    keys[i] = int(key)
            except:
                continue
        return keys
    def ledSwitch(self, choice):
            return {
                '0' : '3f',
                '1' : '06',
                '2' : '5B',
                '3' : '4f',
                '4' : '66',
                '5' : '6D',
                '6' : '7D',
                '7' : '07',
                '8' : '7F',
                '9' : '6F',
                'A' : '77',
                'B' : '7C',
                'C' : '39',
                'D' : '5E',
                'E' : '79',
                'F' : '71',
            }[choice]
    def keypadSwitch(self, column, value):
        if (column == 3 ):
            print "Col 1 But " + str(value) 
        if (column == 2 ):
            print "Col 2 But " + str(value)
        if (column == 1 ):
            print "Col 3 But " + str(value)
        if (column == 0 ):  
            print "Col 4 But " + str(value)


if __name__ == '__main__':
    
    pio = PIO()
    #thread = threading.Thread(target=read_from_port, args=(serial_port,))    
#    test calls for lcd write
    #pio.display([1, 2, 3, 4])
    #pio.display([0, 'C', 5, 9])
    #pio.display([5, 0, 'A', 4])
    #pio.display([1, 2, 3, 4])     
    
    while(1):
        keys = pio.keypad_read()
        print keys
        for col in range (0,4):
            print keys[col]
            if (keys[col] > 0):
                pio.keypadSwitch(col, keys[col])                                         
    
    pio.close()