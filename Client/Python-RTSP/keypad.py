import serial
import time

TTY = '/dev/ttyACM0'
BAUD = 115200

START = '@00'
END = '\r'
#"@00D000\r" port A/0 output
KEY_INPUT = '@00D1FF\r'  # port B/1 input
LED_OUTPUT = '@00D200\r' # port C/2 output
#"@00P001\r" select first column
#"@00P23F\r" write hex code for a 0
CHECK_BUTTON = '@00P1?\r' #check for button pressed
SEG_7_1 = '01'
SEG_7_1 = '02'
SEG_7_1 = '04'
SEG_7_1 = '08'

class PIO:
    def __init__(self):
        self.ser = serial.Serial(TTY, baudrate=BAUD)
    def setup_write(self, display):
        keypad.write(LED_OUTPUT) # port C/2 output
        time.sleep(0.25)
        keypad.write(START+'P0'+display) # port C/2 ou
        time.sleep(.25)
    def write(self, cmd):
        self.ser.write(cmd)
    def setup_read(self):
        self.ser.write(KEY_INPUT)
        time.sleep(.25)
    def read(self):
        self.ser.write(CHECK_BUTTON)
        key = self.ser.read(2)
        if (not "!" in str(key)):
            if(int(key) != 0): 
                return int(key)
        return -1
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
        
    
    #print ser.read(2)
    """time.sleep(1)
    keypad.write('@00P001' + END) # select first column
    keypad.write('@00P2' + keypad.ledSwitch(str(1)) + END ) # write hex code for a 0
    time.sleep(.25)
    keypad.write('@00P002' + END) # select first column
    keypad.write('@00P2' + keypad.ledSwitch(str(2)) + END ) # write hex code for a 0
    time.sleep(.25)
    keypad.write('@00P004' + END) # select first column
    keypad.write('@00P2' + keypad.ledSwitch(str(3)) + END ) # write hex code for a 0
    time.sleep(.25)
    keypad.write('@00P008' + END) # select first column
    keypad.write('@00P2' + keypad.ledSwitch(str(4)) + END ) # write hex code for a 0
    time.sleep(10)"""
    keypad.setup_read()
    
    for x in range(0, 1000):
        time.sleep(.5)
        key = keypad.read()
        if (key > 0):
            print key 
    
    keypad.setup_write(SEG_7_1)    
    
    for x in range(0, 10):
    
        print('Printing: @00P2' + keypad.ledSwitch(str(x)) + END )
        keypad.write('@00P2' + keypad.ledSwitch(str(x)) + END ) # write hex code for a 0
        time.sleep(1)
    
    keypad.close()