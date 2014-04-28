import serial
import time

TTY = '/dev/ttyACM0'
BAUD = 115200

START = '@00'
END = '\r'
PORTA_OUTPUT = '@00D000\r' #port A/0 output
KEY_INPUT = '@00D1FF\r'  # port B/1 input
LED_OUTPUT = '@00D200\r' # port C/2 output
#"@00P001\r" select first column
#"@00P23F\r" write hex code for a 0
CHECK_BUTTON = '@00P1?\r' #check for button pressed
SEG_7_1 = '01'
SEG_7_2 = '02'
SEG_7_3 = '04'
SEG_7_4 = '08'

class PIO:
    def __init__(self):
        self.ser = serial.Serial(TTY, baudrate=BAUD)
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
        self.ser.write(KEY_INPUT)
        time.sleep(.1)
    def read(self):
        self.ser.write(CHECK_BUTTON)
        key = self.ser.read(2)
        if (not "!" in str(key)):
            key = str(key).rsplit('\r')
            if(int(key[0]) != 0): 
                return int(key[0])
        return -1
    def display(self, num1, num2, num3, num4):
        for x in range (0, 100):
            self.setup_write(SEG_7_1)
            self.write('@00P2' + self.ledSwitch(str(num1)) + END )
            time.sleep(0.001) 
            
            self.setup_write(SEG_7_2)
            self.write('@00P2' + self.ledSwitch(str(num2)) + END )
            time.sleep(0.001)
            
            self.setup_write(SEG_7_3)
            self.write('@00P2' + self.ledSwitch(str(num3)) + END ) 
            time.sleep(0.001)
            
            self.setup_write(SEG_7_4)
            self.write('@00P2' + self.ledSwitch(str(num4)) + END ) 
            time.sleep(0.001)
            
        
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
    keypad.display(1, 2, 3, 4)
    keypad.display(0, 4, 5, 9)
    keypad.display(5, 0, 9, 4)
    
   
    
    """ for x in range(0, 100):
        time.sleep(.1)
        key = keypad.read()
        if (key > 0):
            print key 
    
    """

    
    keypad.close()