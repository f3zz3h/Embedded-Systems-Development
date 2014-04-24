# sudo python serial_lcd.py
#

import serial
import time

SERIAL_PORT = "/dev/ttyAMA0"

#function for shifting bottom line to top line and writing along the bottom line
def pageText(textString, serialOut):
	botLine = ""
	cursorPos = 0

	for letter in textString:
		serialOut.write(letter)

		#if printing to the second line, save the deails to the botLine variable for re-use
		if cursorPos > 15:
			botLine = botLine + letter

		#if at the end of the LCD screen, print botLine on top line and start printing to the bottom line
		if cursorPos == 31:
			serialOut.write('\xFE\x80') #wrap to start of first line
			serialOut.write(botLine) #print current botLine on topLine
			serialOut.write("                ") #clear bottom line
			serialOut.write('\xFE\xC0') #goto begin second line
			botLine = ""
			cursorPos = 15 #set cursor to beginning of second line

		cursorPos = cursorPos + 1 #move cursor

		time.sleep(0.15)#delay between printing letter

def main():
	serialOut = serial.Serial(SERIAL_PORT, 9600) #setup for serial port
	time.sleep(2)
	serialOut.write('\xFE\x01')

	while(True):
		time.sleep(0.5)
		serialOut.write('\xFE\x80') #start at first line

		#setup for menu selection
		if menuSelection == "test":
			textString = "test"
		elif menuSelection == "test1":
			textString = "test2"
		else menuSelection == "test2":
			textString = "test2"

		pageText(textString, serialOut) #send string and serial setup to handling function
		time.sleep(2)
		serialOut.write('\xFE\x01') #clear LCD screen

	serialOut.close

if __name__ == '__main__':
	main()
