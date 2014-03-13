from cStringIO import StringIO
from urlparse import urlsplit
import base64
import sys
import math
import time
import struct

class RTSPClient():
    """ Provides RTSP protocol """

    __buffer = '' # Buffer from which lines are parsed
    attach_buffer = StringIO()
    length = None

    content_length = None # length of attached content
    content_type = None # type of attached content

    rtsp_length = None # RTSP Interleaved Binary Data length

    session = None # RTSP Session

    sent_setup = False
    sent_play = False

    def sendCommand(self, command, path):
        """ Sends off an RTSP command
These appear at the beginning of RTSP headers """
        self.sendLine('%s %s RTSP/1.0' % (command, path))

    def sendHeader(self, name, value):
        """ Sends off a header, same method as HTTP headers """
        self.sendLine('%s: %s' % (name, value))

    def sendHeaders(self, dict):
        if not dict:
            return
        for key, value in dict.items():
            self.sendHeader(key, value)

    def endHeaders(self):
        """ Sends \r\n which signifies the end of the headers """
        self.sendLine('')

    def sendMethod(self, method, target='*', headers=None):
        self.sendCommand(method, target)
        self.sendHeader('CSeq', self.cseq)
        self.cseq += 1
        self.sendHeaders(headers)
        self.endHeaders()

    def dataReceived(self, data):
        """Protocol.dataReceived.
Translates bytes into lines, and calls lineReceived (or
rawDataReceived, depending on mode.)
"""
        """ Checks for the $ flag signifying RTSP Interleaved data """
        self.__buffer = self.__buffer+data

        if self.paused:
            return

        while self.__buffer:
            # Checks for $ but only in place of the firstLine and only when
            # self.length is not set
            if not self.length and self.firstLine and len(
                self.__buffer) >= 4 and self.__buffer[0] == '$':
                header, self.__buffer = self.__buffer[:4], self.__buffer[4:]
                # Header should be:
                # Magic $ (1 byte)
                # Channel (1 byte)
                # Length (2 bytes)
                self.rtsp_length = struct.unpack('!H', header[2:4])[0]
                self.length = self.rtsp_length
                if self.length == 0:
                    raise RTSPInterleavedWarning('Interleaved length was 0.', header)
                self.attach_buffer = StringIO()
                self.setRawMode()
            if self.length:
                self.__buffer = self.rawDataReceived(self.__buffer)
                continue
            try:
                line, self.__buffer = self.__buffer.split(self.delimiter, 1)
            except ValueError:
                if len(self.__buffer) > self.MAX_LENGTH:
                    line, self.__buffer = self.__buffer, ''
                    return self.lineLengthExceeded(line)
                break
            else:
                linelength = len(line)
                if linelength > self.MAX_LENGTH:
                    exceeded = line + self.__buffer
                    self.__buffer = ''
                    return self.lineLengthExceeded(exceeded)
                why = self.lineReceived(line)
                if why or self.transport and self.transport.disconnecting:
                    return why
        else:
            data=self.__buffer
            self.__buffer=''
            if data:
                self.handleResponsePart(data)

    def lineReceived(self, line):
        """ Almost exactly the same as twisted.web.http.HTTPClient """
        if self.firstLine:
            self.headers = {}
            self.firstLine = 0
            l = line.split(None, 2)
            version = l[0]
            status = l[1]
            try:
                message = l[2]
            except IndexError:
                message = ''
            self.handleStatus(version, status, message)
            return
        if line:
            key, val = line.split(':', 1)
            val = val.lstrip()
            self.handleHeader(key, val)
        else:
            # End of the headers has been reached
            self._handleEndHeaders(self.headers)
            if self.content_length is not None:
                self.setRawMode()
            self.firstLine = 1

    def connectionMade(self):
        """ Connection is established
Sends off the Options request """
        print('Connected!')
        self.headers = {}
        self.cseq = 1
        self.firstLine = 1

        self.sendNextMessage()

    # -----------------
    # Response Handlers
    # -----------------

    def handleStatus(self, version, status, message):
        """ Called when the status header is received """
        if status == '404':
            self.transport.loseConnection()
            self.factory.error(failure.Failure(error.Error(http.NOT_FOUND)))
            return
        length = len(version) + len(status) + len(message)
        if length > 50:
            self.transport.loseConnection()
            self.factory.error(
                failure.Failure(
                    RTSPStatusError(
                        'Length of status message was too long: %s' % length,
                        version)))
            return
        print('Status: %s %s %s' % (status,message,version))

    def handleHeader(self, key, value):
        """ Called when a single header is received
Stores the header in dictionary self.headers
Each dictionary value is a list and can hold multiple response values"""
        key = key.lower()

        # Store the session in self.session
        for k in ['session','etag']:
            if key == k:
                self.session = value
        # Grabs just the session, removes the timeout at the end
        if self.session:
            delim = self.session.find(';')
            if delim != -1:
                self.session = self.session[:delim]
        if key == 'content-type':
            self.content_type = value

        # Allow for multiple values per key
        l = self.headers[key] = self.headers.get(key, [])
        l.append(value)

    def sendNextMessage(self):
        """ Default method handles only the
bare minimum Setup and Play messages
Override this in sub classes to change behavior """
        if not self.sent_setup:
            self.sent_setup = True
            self.sendSetup()
            self.endHeaders()
            return True
        if not self.sent_play:
            self.sent_play = True
            self.sendPlay()
            self.endHeaders()
            return True
        return False

    def _handleEndHeaders(self, headers):
        """ Internal handleEndHeaders
Checks the server's CSeq and for content-length """
        header_file = open('headers.txt', 'ab')
        headerstr = '\r\n'.join('%s: %s' % (k,v[0]) for k,v in headers.items())
        header_file.write(headerstr)
        header_file.write('\r\n\r\n')
        header_file.close()
# print(headerstr)

        if headers.get('cseq'):
            serverCSeq = int(headers['cseq'][0])
            if serverCSeq != self.cseq - 1:
                print('Server CSeq != Client CSeq: %s != %s' %
                      (serverCSeq, self.cseq - 1))
        if headers.get('content-length'):
            self.content_length = int(headers['content-length'][0])
            self.length = self.content_length
        self.handleEndHeaders(headers)

    def handleEndHeaders(self, headers):
        """ Called when all headers have been received """
        if self.content_length is not None:
            # We call sendNextMessage after the response has been received
            return
        self.sendNextMessage()

    def handleContentResponse(self, data, content_type=None):
        """ Called when the entire content-length has been received """

    def handleResponseEnd(self, data):
        """ Called when length of data has been received """
        if self.content_length:
            self.content_length = None
            self.handleContentResponse(data, self.content_type)
            self.sendNextMessage()
            self.content_type = None
        elif self.rtsp_length:
            self.rtsp_length = None
            self.handleInterleavedData(data)
        else:
            self.handleResponsePart(data)

    def handleInterleavedData(self, data):
        """ Called when an interleaved data frame is received """

    def handleResponsePart(self, data):
        """ Called when a chunk of raw data is received
or when length of raw data has been received """

    def rawDataReceived(self, data):
        """ Called when data is received in raw data mode
Gathers self.content-length worth of data in attach_buffer
Returns what it doesn't use """
        if self.length is not None:
            self.attach_buffer.write(data)
            buff_len = self.attach_buffer.tell()
            if buff_len >= self.length:
                data = self.attach_buffer.getvalue()
                data, rest = data[:self.length], data[self.length:]
                self.handleResponseEnd(data)
                self.length = None
                self.attach_buffer = StringIO()
                return rest

    # ----------------------
    # Packet Sending Methods
    # ----------------------

    def sendOptions(self, target='*', headers=None):
        """ Requests available OPTIONS from server """
        self.sendMethod('OPTIONS', target, headers)

    def sendDescribe(self, target='*', headers=None):
        """ Asks server to describe stream in sdp format """
        self.sendMethod('DESCRIBE', target, headers)

    def sendSetup(self, target='*', headers=None):
        """ Tells the server to setup the stream """
        self.sendMethod('SETUP', target, headers)

    def sendSetParameter(self, target='*', headers=None):
        """ Tells the server to set parameters for streaming """
        self.sendMethod('SET_PARAMETER', target, headers)

    def sendPlay(self, range='0-', target='*', headers={}):
        """ Tells the server to play the stream for you """
        headers['Range'] = 'npt=%s' % range
        self.sendMethod('PLAY', target, headers)

RTSPClient()
