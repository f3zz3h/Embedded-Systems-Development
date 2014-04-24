# sudo python serial_lcd.py
import serial
import time

class lcd:
	def __init__(self):
		SERIAL_PORT = "/dev/ttyAMA0"
		self.serialOut = serial.Serial(SERIAL_PORT, 9600) #setup for serial port
		self.botLine = ""
		self.cursorPos = 0
	
	#function for shifting bottom line to top line and writing along the bottom line
	def pageText(self, textString):
		self.botLine = ""
		self.cursorPos = 0

		for letter in textString:
			self.serialOut.write(letter)
	
			#if printing to the second line, save the deails to the botLine variable for re-use
			if self.cursorPos > 15:
				self.botLine = self.botLine + letter
	
			#if at the end of the LCD screen, print botLine on top line and start printing to the bottom line
			if self.cursorPos == 31:
				self.startAtFirstLine #wrap to start of first line
				self.serialOut.write(self.botLine) #print current botLine on topLine
				self.serialOut.write("                ") #clear bottom line
				self.startAtSecondLine #goto begin second line
				self.botLine = ""
				self.cursorPos = 15 #set cursor to beginning of second line
	
			self.cursorPos = self.cursorPos + 1 #move cursor
	
			time.sleep(0.15)#delay between printing letter
	
	def startAtFirstLine(self):
		self.serialOut.write('\xFE\x80') #start at first line
		
	def clearScreen(self):
		self.serialOut.write('\xFE\x01') #clear LCD screen

	def closeConnection(self):
		self.serialOut.close

	def startAtSecondLine(self):
		self.serialOut.write('\xFE\xC0')
		
	def close(self):
		self.serialOut.close

	def menuSwitch (self, choice):
		return {
			"test" : test,
			"test1": test1,
		
	
		}[choice]
	
# USED IF THIS FILE IS LAUNCHER FROM HERE... otherwise not run
if __name__ == '__main__':
	
	myLCD = lcd()
	
#	while(True):

		#setup for menu selection
#		if menuSelection == "test":
#			textString = "test"
#		elif menuSelection == "test1":
#			textString = "test2"
#		else menuSelection == "test2":
#			textString = "test2"
	myLCD.clearScreen()

	while(True):
		myLCD.startAtFirstLine()
		textString = "111111111111111122222222222222223333333333333333"
		myLCD.pageText(textString) #send string and serial setup to handling function
		time.sleep(5)
		myLCD.clearScreen()

	myLCD.close
