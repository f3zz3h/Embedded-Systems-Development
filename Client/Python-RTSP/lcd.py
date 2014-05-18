__author__ = "Sebastian Beaven, Luke Hart"
__copyright__ = "Copyright 2014, The Jeff Museum"
__credits__ = ["Luke Hart","Joe Ellis", "Chris Sewell", "Matt Ribbins",
               "Sebastian Beaven", "Joshua Webb", "Andrew Bremmer"]
__license__ = "GPL"
__version__ = "0.9"
__maintainer__ = "Sebastian Beaven"
__email__ = "sebs..."
__status__ = "Development"

import serial
import time
from collections import namedtuple

#Define values for LCD switch
ENTER_PIN = 1
INVALID_PIN = 2
ACCEPTED_PIN = 3
ENTER_DISPLAY_NUMBER = 4
INVALID_DISPLAY_NUMBER = 5
FETCH_DISPLAY_NUMBER = 6
TRACK_STATUS = 7
PLAY = 8
PAUSE = 9
STOP = 10
FAST_FORWARD = 11
REWIND = 12
VOLUP = 13
VOLDOWN =14

class LCD:
	def __init__(self):
		"""
		Setup serial port for writing to LCD screen on rpi
		"""
		Constants = namedtuple('Constants', ['StartTopLine', 'EndTopLine', 'StartBottomLine', 'EndBottomLine', 'EndOfMemCap'])
		self.constants = Constants(0, 15, 16, 31, 39)
		SERIAL_PORT = "/dev/ttyAMA0"
		
		self.serialOut = serial.Serial(SERIAL_PORT, 9600) #setup for serial port
		self.botLine = ""
		self.cursorPos = self.constants.StartTopLine
	
	def topLineScroll(self, textString):
		"""
		Make top line scroll 
		"""
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
	
	def pageText(self, textString):
		"""
		function for shifting bottom line to top line 
		and writing along the bottom line
		"""
		self.clearScreen()
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
	
			time.sleep(0.01)#delay between printing letter
	
	def scrollLeftOne(self):
		"""
		Scroll on char left
		"""
		self.lcdWrite('\xFE\x18')

	def startAtFirstLine(self):
		"""
		Set cursor to first line
		"""
		self.lcdWrite('\xFE\x80') #start at first line
		
	def clearScreen(self):
		"""
		Clear screen
		"""
		self.lcdWrite('\xFE\x01') #clear LCD screen

	def startAtSecondLine(self):
		"""
		Move to start writing at second line
		"""
		self.serialOut.write('\xFE\xC0')
		
	def close(self):
		"""
		Close serial connection
		"""
		self.serialOut.close
		
	def lcdWrite(self, msg="                "):
		"""
		Write to lcd screen, default a blank line
		"""
		self.serialOut.write(msg)

	def menuSwitch (self, choice):
		"""
		Return string based on choice
		"""
		return {
			ENTER_PIN : "Please Enter PinNumber:",
			ACCEPTED_PIN : "Pin Number      Accepted",
			INVALID_PIN : "Pin Number      Declined",
			ENTER_DISPLAY_NUMBER : "Please Enter    Display Number:",
			INVALID_DISPLAY_NUMBER : "Invalid Display Number",
			FETCH_DISPLAY_NUMBER : "Fetching DisplayTrack",
		#	TRACK_STATUS : "%d: %s" % (trackNumber, trackName),
			PLAY : "Playing",
			PAUSE : "Paused",
			STOP : "Stopped",
			FAST_FORWARD : "Fast Forward",
			REWIND : "Rewind",
            VOLUP : "Volume ++",
            VOLDOWN : "Volume --"
		}[choice]
		
	def writeLCD(self, choice):
		"""
		A structured write LCD
		"""
		self.clearScreen()
		self.cursorPos = 0
		self.botLine = ""
		self.startAtFirstLine()
		textString = self.menuSwitch(choice)
		self.pageText(textString)
		#self.topLineScroll(textString) #send string and serial setup to handling function
		time.sleep(0.5)
