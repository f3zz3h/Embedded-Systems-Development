# sudo python serial_lcd.py
import serial
import time

class lcd:
	def __init__(self):
		SERIAL_PORT = "/dev/ttyAMA0"
		serialOut = serial.Serial(SERIAL_PORT, 9600) #setup for serial port
		self.clearScreen()
	
	#function for shifting bottom line to top line and writing along the bottom line
	def pageText(self, textString):
		botLine = ""
		cursorPos = 0
	
		for letter in textString:
			self.serialOut.write(letter)
	
			#if printing to the second line, save the deails to the botLine variable for re-use
			if cursorPos > 15:
				botLine = botLine + letter
	
			#if at the end of the LCD screen, print botLine on top line and start printing to the bottom line
			if cursorPos == 31:
				self.serialOut.write('\xFE\x80') #wrap to start of first line
				self.serialOut.write(botLine) #print current botLine on topLine
				self.serialOut.write("                ") #clear bottom line
				self.serialOut.write('\xFE\xC0') #goto begin second line
				botLine = ""
				cursorPos = 15 #set cursor to beginning of second line
	
			cursorPos = cursorPos + 1 #move cursor
	
			time.sleep(0.15)#delay between printing letter
	
	def startAtFirstLine(self):
		self.serialOut.write('\xFE\x80') #start at first line
		
	def clearScreen(self):
		self.serialOut.write('\xFE\x01') #clear LCD screen

	def closeConnection(self):
		self.serialOut.close
		
	def menuSwitch (self, choice):
		return {
			"test" : test,
			"test1": test1,
		
	
		}[choice]
	
# USED IF THIS FILE IS LAUNCHER FROM HERE... otherwise not run
if __name__ == '__main__':
	
	myLCD = lcd()

	while(True):

		#setup for menu selection
		if menuSelection == "test":
			textString = "test"
		elif menuSelection == "test1":
			textString = "test2"
		else menuSelection == "test2":
			textString = "test2"

		pageText(textString, serialOut) #send string and serial setup to handling function
		


