# sudo python serial_lcd.py
import serial
import time
from collections import namedtuple
ENTER_PIN = 1
INVALID_PIN = 2
ACCEPTED_PIN = 3
ENTER_DISPLAY = 4
INVALID_DISPLAY = 5
FETCH_DISPLAY = 6
TRACK_STATUS = 7

class lcd:
	def __init__(self):
		Constants = namedtuple('Constants', ['StartTopLine', 'EndTopLine', 'StartBottomLine', 'EndBottomLine', 'EndOfMemCap'])
		self.constants = Constants(0, 15, 16, 31, 39)
		SERIAL_PORT = "/dev/ttyAMA0"
		
		self.serialOut = serial.Serial(SERIAL_PORT, 9600) #setup for serial port
		self.botLine = ""
		self.cursorPos = self.constants.StartTopLine
	
	def topLineScroll(self, textString):
		nextString = ""
		cursorPos = self.constants.StartTopLine
		firstPass = True #test to see if in first 16 chars

		for letter in textString:
			if firstPass == False:
				self.scrollLeftOne() #scroll left one space at ezch letter

			self.lcdWrite(letter)

			if cursorPos == self.constants.EndTopLine:
				self.lcdWrite('\xFE\x90') #move to row 1 column 2
				firstPass = False #goes into scrolling mdoe after row is filled for first time

			if cursorPos == self.constants.EndBottomLine:
				self.lcdWrite('\xFE\xA0') #move to row 1 column 3

			if cursorPos == self.constants.EndOfMemCap:
				cursorPos = -1 #start over, only 40 chars in memory
				self.startAtFirstLine()
		
			cursorPos = cursorPos + 1
			time.sleep(0.2)
	

	#function for shifting bottom line to top line and writing along the bottom line
	def pageText(self, textString):

		for letter in textString:
			self.lcdWrite(letter)
	
			#if printing to the second line, save the deails to the botLine variable for re-use
			if self.cursorPos > self.constants.EndTopLine:
				self.botLine = self.botLine + letter
	
			#if at the end of the LCD screen, print botLine on top line and start printing to the bottom line
			if self.cursorPos == self.constants.EndBottomLine:
				self.startAtFirstLine() #wrap to start of first line
				self.lcdWrite(self.botLine) #print current botLine on topLine
				self.lcdWrite() #clear bottom line
				self.startAtSecondLine() #goto begin second line
				self.botLine = ""
				self.cursorPos = self.constants.EndTopLine #set cursor to end of top line
	
			self.cursorPos = self.cursorPos + 1 #increase cursor number
	
			time.sleep(0.15)#delay between printing letter
	
	def scrollLeftOne(self):
		self.lcdWrite('\xFE\x18')

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
			ENTER_PIN : "Please Enter Pin Number: ",
			ACCEPTED_PIN : "Pin Number Accepted",
			INVALID_PIN : "Pin Number Declined",
			ENTER_DISPLAY : "Please Enter Display Number: ",
			INVALID_DISPLAY : "Invalid Display Number, Please Try Again",
			FETCH_DISPLAY : "Fetching Display Track",
		#	TRACK_STATUS : "%d: %s" % (trackNumber, trackName),
		}[choice]

#USED IF THIS FILE IS LAUNCHER FROM HERE... otherwise not run
if __name__ == '__main__':
	
	myLCD = lcd()
	myLCD.clearScreen()

	while(True):
		myLCD.startAtFirstLine()
		textString = myLCD.menuSwitch(INVALID_DISPLAY)
		#myLCD.pageText(textString)
		myLCD.topLineScroll(textString) #send string and serial setup to handling function
		time.sleep(0.5)
		myLCD.clearScreen()

	myLCD.close
