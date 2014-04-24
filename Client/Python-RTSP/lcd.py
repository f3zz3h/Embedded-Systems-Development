# sudo python serial_lcd.py
import serial
import time
from collections import namedtuple

class lcd:
	def __init__(self):
		Constants = namedtuple('Constants', ['StartTopLine', 'EndTopLine', 'StartBottomLine', 'EndBottomLine'])
		self.constants = Constants(0, 15, 16, 31)
		SERIAL_PORT = "/dev/ttyAMA0"
		
		self.serialOut = serial.Serial(SERIAL_PORT, 9600) #setup for serial port
		self.botLine = ""
		self.cursorPos = self.constants.StartTopLine
	
	#function for shifting bottom line to top line and writing along the bottom line
	def pageText(self, textString):

		for letter in textString:
			self.lcdWrite(letter)
	
			#if printing to the second line, save the deails to the botLine variable for re-use
			if self.cursorPos > (self.constants.EndTopLine):
				self.botLine = self.botLine + letter
	
			#if at the end of the LCD screen, print botLine on top line and start printing to the bottom line
			if self.cursorPos == (self.constants.EndBottomLine):
				self.startAtFirstLine() #wrap to start of first line
				self.lcdWrite(self.botLine) #print current botLine on topLine
				self.lcdWrite() #clear bottom line
				self.startAtSecondLine() #goto begin second line
				self.botLine = ""
				self.cursorPos = self.constants.EndTopLine #set cursor to end of top line
	
			self.cursorPos = self.cursorPos + 1 #increase cursor number
	
			time.sleep(0.15)#delay between printing letter
	
	def startAtFirstLine(self):
		self.lcdWrite('\xFE\x80') #start at first line
		
	def clearScreen(self):
		self.lcdWrite('\xFE\x01') #clear LCD screen

	def closeConnection(self):
		self.serialOut.close

	def startAtSecondLine(self):
		self.serialOut.write('\xFE\xC0')
		
	def close(self):
		self.serialOut.close
		
	def lcdWrite(self, msg="                "):
		self.serialOut.write(msg)

	def menuSwitch (self, choice):
		return {
			"Please Enter Pin Number: " : enterPinNumber,
			"Please Enter Display Number: ": enterDisplayNumber,
			"%d: %s" % (trackNumber, trackName) : trackStatus,
		}[choice]

#USED IF THIS FILE IS LAUNCHER FROM HERE... otherwise not run
if __name__ == '__main__':
	
	myLCD = lcd()

	myLCD.clearScreen()

	while(True):
		myLCD.startAtFirstLine()
		textString = "111111111111111122222222222222223333333333333333"
		myLCD.pageText(textString) #send string and serial setup to handling function
		time.sleep(2)
		myLCD.clearScreen()

	myLCD.close
