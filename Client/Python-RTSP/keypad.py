import serial
import time
import io

TTY = '/dev/ttyACM0'
BAUD = 115200

START = '@00'
END = '\r'
PORTA_OUTPUT = '@00D000\r' #port A/0 output
KEY_INPUT = '@00D1FF\r'  # port B/1 input
LED_OUTPUT = '@00D200\r' # port C/2 output
SELECT_COLUMN = ['@00P001\r','@00P002\r','@00P004\r','@00P008\r'] #select first column
#"@00P23F\r" write hex code for a 0
CHECK_BUTTON = '@00P1?\r'
SEG_7 = ['01', '02', '04' ,'08']

class PIO:
    def __init__(self):
        self.ser = serial.Serial(TTY, baudrate=BAUD, timeout=1)
        self.write(PORTA_OUTPUT)
        self.write(KEY_INPUT)
        self.write(LED_OUTPUT)
    def setup_write(self, display):
        self.write('@00P2' + '00' + END ) # write hex code for a 0
        time.sleep(0.0001)
        keypad.write(START+'P0'+display+END) # port C/2 ou
        time.sleep(.001)
        
    def write(self, cmd):
        self.ser.write(cmd)
    def setup_read(self):
        self.ser_io = None
        self.ser.write(KEY_INPUT)
        time.sleep(.1)
        if(self.ser_io is None):
            self.ser_io = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser, 1),  
                               newline = '\r',
                               line_buffering = True)
        time.sleep(.1)
    def read(self):
        self.setup_read()
        keys = [0,0,0,0]
        for i in range(0,4):
            self.write(SELECT_COLUMN[i])
            time.sleep(.01)
            self.ser.write(CHECK_BUTTON)
            time.sleep(0.001)
            key = str(self.ser_io.readline())
            key = key.lstrip('!')
            key = key.rstrip()
            print key
            if(int(key) != 0): 
                keys[i] = int(key)
        return keys
    # params: num[4] array of size 4 which takes numbers from 0-9 for each lcd item
    # ToDo: Could just be a number 0-9999 and be broken into components but for now
    # this works
    def display(self, num):
        #Write values for appox 1 second
        for x in range (0, 100):
            for i in range (0,4):
                self.setup_write(SEG_7[i])
                self.write('@00P2' + self.ledSwitch(str(num[i])) + END )
                time.sleep(0.001)
        #Clear display at finish
        for i in range (0,4):
            self.setup_write(SEG_7[i])
        
        
    def close(self):
        self.ser.close()
    def ledSwitch (self, choice):
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


if __name__ == '__main__':
    
    keypad = PIO()
        
#    test calls for lcd write
    #keypad.display([1, 2, 3, 4])
    #keypad.display([0, 4, 5, 9])
    #keypad.display([5, 0, 9, 4])     
    
    while(1):
        keys = keypad.read()
        for i in range(0,4):
            if (keys[i] > 0):
                print keys[i] 
    
    keypad.close()