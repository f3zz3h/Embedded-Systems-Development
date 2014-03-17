# Copyright (C) 2008 David Bern
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# To do:
#   fix avg packet size computation for file header
#   find bug where the program just spits out stopping factory and doesn't
#     return the deferred callback/errback
#
# Modified by Group D?
#     Removed unused methods.
#     Added custom RTSP requests

from twisted.web import client
from twisted.internet import defer, reactor
from twisted.python import failure, log
from twisted.protocols import basic
from twisted.python.util import InsensitiveDict
from cStringIO import StringIO
from optparse import OptionParser
from urlparse import urlsplit
import base64
import sys
import struct
import re
import math
import time
import hashlib
from md5 import md5
from rmff import *
from rtsp import RTSPClient, RTSPClientFactory
from sdpp import Sdpplin
from asmrp import Asmrp


# http://blogmag.net/blog/read/38/Print_human_readable_file_size
def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

# http://lists.mplayerhq.hu/pipermail/mplayer-dev-eng/2008-March/056903.html
def rn5_auth(username, realm, password, nonce, uuid):
    MUNGE_TEMPLATE ='%-.200s%-.200s%-.200sCopyright (C) 1995,1996,1997 RealNetworks, Inc.'
    authstr ="%-.200s:%-.200s:%-.200s" % (username, realm, password)
    first_pass = hashlib.md5(authstr).hexdigest()

    munged = MUNGE_TEMPLATE % (first_pass, nonce, uuid)
    return hashlib.md5(munged).hexdigest()
    print first_pass
class RealChallenge(object):
    XOR_TABLE = [ 0x05, 0x18, 0x74, 0xd0, 0x0d, 0x09, 0x02, 0x53, 0xc0, 0x01,
                  0x05, 0x05, 0x67, 0x03, 0x19, 0x70, 0x08, 0x27, 0x66, 0x10,
                  0x10, 0x72, 0x08, 0x09, 0x63, 0x11, 0x03, 0x71, 0x08, 0x08,
                  0x70,    0x02, 0x10, 0x57, 0x05, 0x18, 0x54 ]
    def AV_WB32(d):
        """ Used by RealChallenge() """
        d = d.decode('hex')
        return list(struct.unpack('%sB' % len(d), d))
    def compute(rc1):
        """ Translated from MPlayer's source
        Computes the realchallenge response and checksum """
        buf = list()
        buf.extend( RealChallenge.AV_WB32('a1e9149d') )
        buf.extend( RealChallenge.AV_WB32('0e6b3b59') )

        rc1 = rc1.strip()

        if rc1:from md5 import md5
from rmff import *
from rtsp import RTSPClient, RTSPClientFactory
from sdpp import Sdpplin
from asmrp import Asmrp
            if len(rc1) == 40: rc1 = rc1[:32]
            if len(rc1) > 56: rc1 = rc1[:56]
            buf.extend( [ ord(i) for i in rc1 ] )
            buf.extend( [ 0 for i in range(0, 56 - len(rc1)) ] )

        # xor challenge bytewise with xor_table
        for i in range(0, len(RealChallenge.XOR_TABLE)):
            buf[8 + i] ^= RealChallenge.XOR_TABLE[i];

        sum = md5( ''.join([ chr(i) for i in buf ]) )

        response = sum.hexdigest() + '01d0a8e3'

        chksum = list()
        for i in range(0, 8):
            chksum.append(response[i * 4])
        chksum = ''.join(chksum)

        return (response, chksum)
    compute = staticmethod(compute)
    AV_WB32 = staticmethod(AV_WB32)

class RDTClient(RTSPClient):
    data_received = 0
    out_file = None
    prev_timestamp = None
    prev_stream_num = None
    streamids = []
    setup_streamids = []
    ended_streamids = []

    sent_options = False
    sent_describe = False
    sent_parameter = False
    sent_bandwidth = False
    sent_realchallenge2 = False
    sent_rn5_auth = False
    sent_auth = False
    rn5_authdata = None

    EOF = 0xff06
    LATENCY_REPORT = 0xff08

    def handleEndHeaders(self, headers):
        if headers.get('realchallenge1'):
            self.realchallenge1 = headers['realchallenge1'][0]
        elif headers.get('www-authenticate', [''])[0].startswith('RN5'):
            ##hack: resent describe header with auth
            self.sent_describe = False
            print 'RN5 Authendication'
            self.rn5_authdata ={}
            for authdate in headers['www-authenticate'][0][3:].split(','):
                key, value = authdate.split('=')
                ##remove "
                self.rn5_authdata[key.strip()] = value[1:-1]

        if self.content_length is None:
            self.sendNextMessage()

    def handleSdp(self, data):
        """ Called with SDP Response data
        Uses the SDP response to construct the file header """
        sdp = Sdpplin(data)
        header = rmff_header_t()
        try: abstract = sdp['Abstract']
        except KeyError: abstract = ''
        header.fileheader = rmff_fileheader_t(4 + sdp['StreamCount'])
        try: title = sdp['Title']
        except KeyError: title = ''
        try: author = sdp['Author']
        except KeyError: author = ''
        try: copyright = sdp['Copyright']
        except KeyError: copyright = ''
        header.cont = rmff_cont_t(title, author,
                                  copyright, abstract)
        header.data = rmff_data_t(0, 0)

        duration = 0
        max_bit_rate = 0
        avg_bit_rate = 0
        max_packet_size = 0
        avg_packet_size = None

        self.streammatches = {}

        # the rulebook is sometimes truncated and spread across the streams
        # not sure if this is common, or even the correct way to handle it
        rulebook = ''.join([s['ASMRuleBook'] for s in sdp.streams])
        symbols = {'Bandwidth':self.factory.bandwidth,'OldPNMPlayer':'0'}
        rulematches, symbols = Asmrp.asmrp_match(rulebook, symbols)
        # Avg packet size seems off

        for s in sdp.streams:
            self.streammatches[s['streamid']] = rulematches
            mlti = self.select_mlti_data(s['OpaqueData'], rulematches[0])

            # some streams don't have the starttime, but do have endtime
            # and other meta data
            try: start_time = s['StartTime']
            except: start_time = 0

            mdpr = rmff_mdpr_t(s['streamid'], s['MaxBitRate'],
                               s['AvgBitRate'], s['MaxPacketSize'],
                               s['AvgPacketSize'], start_time,
                               s['Preroll'], s.duration,
                               s['StreamName'], s['mimetype'], mlti)
            header.streams.append(mdpr)
            if s.duration > duration:
                duration = s.duration
            if mdpr.max_packet_size > max_packet_size:
                max_packet_size = mdpr.max_packet_size
            max_bit_rate += mdpr.max_bit_rate
            avg_bit_rate += mdpr.avg_bit_rate
            if avg_packet_size is None:
                avg_packet_size = mdpr.avg_packet_size
            else:
                avg_packet_size = (avg_packet_size + mdpr.avg_packet_size)/2
        header.prop = rmff_prop_t(max_bit_rate, avg_bit_rate,
                                  max_packet_size, avg_packet_size,
                                  0, duration, 0, 0, 0, sdp['StreamCount'],
                                  sdp['Flags'])
        return header

    def heartbeat(self):
        target = '%s://%s:%s' % (self.factory.scheme,
                                 self.factory.host,
                                 self.factory.port)
        headers = {}
        headers['User-Agent'] = self.factory.agent
        headers['PlayerStarttime'] = self.factory.PLAYER_START_TIME
        headers['CompanyID'] = self.factory.companyID
        headers['GUID'] = self.factory.GUID
        headers['RegionData'] = '0'
        headers['ClientID'] = self.factory.clientID
        headers['Pragma'] = 'initiate-session'
        self.sendOptions('*', headers)
        reactor.callLater(30, self.heartbeat)

    def handleContentResponse(self, data, content_type):
        """ Called when the entire content-length has been received
        Expect to receive type application/sdp """
        f = open('sdp.txt', 'w')
        f.write(data)
        f.close()
        if content_type == 'application/sdp':
            print 'Correct content found'
            print 'Process with gstreamer'
            reactor.callLater(30, self.heartbeat)
            self.out_file = open(self.factory.filename, 'wb')
            self.header = self.handleSdp(data)
            self.streamids = [i for i in range(self.header.prop.num_streams)]
            self.subscribe = ''
            for i,rules in self.streammatches.items():
                for r in rules:
                    self.subscribe += 'stream=%s;rule=%s,' % (i,r)
            self.subscribe = self.subscribe[:-1] # Removes trailing comma
            self.out_file.write(self.header.dump())
            self.num_packets = 0
            self.data_size = 0

 
    def handleInterleavedData(self, data):
        """ Called when an interleaved data frame is received """
        self.data_received += len(data)
        self.factory.data_received = self.data_received

        # Each Interleaved packet can have multiple RDT packets
        while len(data) > 0:
            # Here we check packet_flags to see if the RDT header includes
            # the length of the RDT packet. If it does, we try to handle
            # multiple RDT packets.
            packet_flags = struct.unpack('B', data[0])[0]
            packet_type = struct.unpack('!H', data[1:3])[0]

            if packet_type == self.EOF:
                self.handleRDTPacket(data)
                return
            len_included = packet_flags & 0x80 == 0x80
            if len_included:
                packet_length = struct.unpack('!H', data[3:5])[0]
                packet, data = data[:packet_length], data[packet_length:]
                self.handleRDTPacket(packet)
            else:
                # If no length is given, assume remaining data is one packet
                self.handleRDTPacket(data)
                break

    # ----------------------
    # Packet Sending Methods
    # ----------------------

    def _sendOptions(self, headers={}):
        target = '%s://%s:%s' % (self.factory.scheme,
                                 self.factory.host,
                                 self.factory.port)
        headers['User-Agent'] = self.factory.agent
        headers['ClientChallenge'] = self.factory.CLIENT_CHALLENGE
        headers['PlayerStarttime'] = self.factory.PLAYER_START_TIME
        headers['CompanyID'] = self.factory.companyID
        headers['GUID'] = self.factory.GUID
        headers['RegionData'] = '0'
        headers['ClientID'] = self.factory.clientID
        headers['Pragma'] = 'initiate-session'
        self.sendOptions(target, headers)

    def _sendDescribe(self, headers={}):
        target = '%s://%s:%s%s' % (self.factory.scheme,
                                   self.factory.host,
                                   self.factory.port,
                                   self.factory.path)
        headers['Accept'] = 'application/sdp'
#        headers['Bandwidth'] = str(self.factory.bandwidth)
        headers['GUID'] = self.factory.GUID
        headers['RegionData'] = '0'
        headers['ClientID'] = self.factory.clientID
        headers['SupportsMaximumASMBandwidth'] = '1'
        headers['Language'] = 'en-US'
        headers['Require'] = 'com.real.retain-entity-for-setup'
        ##rn5 auth
        if self.rn5_authdata:
            authstring ='RN5 '
            self.rn5_authdata['username'] = self.factory.username
            self.rn5_authdata['GUID'] = '00000000-0000-0000-0000-000000000000'
            self.rn5_authdata['response'] = \
                    rn5_auth(nonce=self.rn5_authdata['nonce'],
                             username=self.factory.username,
                             password=self.factory.password,
                             uuid=self.rn5_authdata['GUID'],
                             realm=self.rn5_authdata['realm'])
            ## a string like 'RN5 username="foo",realm="bla"...'
            headers['Authorization'] = 'RN5 ' + ', '.join(
                ['%s="%s"' % (key, val) for key,val in self.rn5_authdata.items()])

        if not self.rn5_authdata and self.factory.username is not None:
            authstr = '%s:%s' % (self.factory.username,
                                 self.factory.password
                                 if self.factory.password else '')
            authstr = base64.b64encode(authstr)
            headers['Authorization'] = 'Basic %s' % authstr
        self.sendDescribe(target, headers)

    def _sendSetup(self, headers={}, streamid=0):
        target = '%s://%s:%s%s/streamid=%s' % (self.factory.scheme,
                                               self.factory.host,
                                               self.factory.port,
                                               self.factory.path,
                                               streamid)
        headers['If-Match'] = self.session
        headers['Transport'] = 'x-pn-tng/tcp;mode=play,rtp/avp/tcp;unicast;mode=play'
        self.sendSetup(target, headers)

    def _sendSetParameter(self, key, value, headers=None):
        target = '%s://%s:%s%s' % (self.factory.scheme, self.factory.host,
                                   self.factory.port, self.factory.path)
        if headers is None:
            headers = {}
        headers['Session'] = self.session
        headers[key] = value
        self.sendSetParameter(target, headers)

    def _sendPlay(self, range='0-', headers={}):
        target = '%s://%s:%s%s' % (self.factory.scheme,
                                   self.factory.host,
                                   self.factory.port,
                                   self.factory.path)
        if self.session:
            headers['Session'] = self.session
        #self.sendPlay(range, target, headers)

    def _sendRequest(self, pin, headers={}):
        target = '%s://%s:%s%s' % (self.factory.scheme,
                                   self.factory.host,
                                   self.factory.port,
                                   self.factory.path)
        headers['Pin'] = pin
        self.sendRequest(target, headers)
        
    def _sendAuth(self, pin, headers={}):
        target = '%s://%s:%s%s' % (self.factory.scheme,
                                   self.factory.host,
                                   self.factory.port,
                                   self.factory.path)
        headers['Pin'] = pin
        self.sendAuth(target, headers)

    def sendNextMessage(self):
        """ This method goes in order sending messages to the server:
        OPTIONS, DESCRIBE, AUTH, REQUEST, PLAY
        Returns True if it sent a packet, False if it didn't """
        if not self.sent_options:
            print 'Sending options'
            self.sent_options = True
            self._sendOptions()
            return True
        if not self.sent_describe:
            print 'Sending describe'
            self.sent_describe = True
            self._sendDescribe()
            return True
        if len(self.streamids) > len(self.setup_streamids):
            headers = {}
            if not self.sent_realchallenge2:
                self.sent_realchallenge2 = True
                challenge_tuple = RealChallenge.compute(self.realchallenge1)
                headers['RealChallenge2'] = '%s, sd=%s' % challenge_tuple
            # Gets a streamid that hasn't been setup yet
            s = [s for s in self.streamids if s not in self.setup_streamids][0]
            self.setup_streamids.append(s)
            self._sendSetup(streamid=s, headers=headers)
            return True
        if not self.sent_parameter:
            self.sent_parameter = True
            self._sendSetParameter('Subscribe', self.subscribe)
            return True
        if self.sent_describe: #and not self.sent_auth():
            print 'Sending auth pin: %d' % self.factory.pin 
            self.sent_auth = True
            self._sendAuth(self.factory.pin)
            return True
        if self.sent_auth:
            print 'Sending request'
            self._sendRequest(self.factory.pin)
            return True
        if not self.sent_play:
            print 'Sending play'
            self.sent_play = True
            self._sendPlay()
            return True  
        return False

def success(result):
    if result == 0:
        print('Success!')
    else:
        print('Result: %s' % result)
    reactor.stop()

def error(failure):
    print('Failure!: %s' % failure.getErrorMessage())
    reactor.stop()

def progress(factory):
    print('Downloaded %s' % sizeof_fmt(factory.data_received))
    reactor.callLater(1, progress, factory)

#Only call this is script run from this file
if __name__ == '__main__':
    parser = OptionParser()
    print parser
    parser.add_option('-u', '', dest='url', help='url to download',
                      metavar='URL')
    parser.add_option('-f', '', dest='file', help='file to save to',
                      metavar='FILENAME')
    options, args = parser.parse_args()
    if options.url is None:
        print('You must enter a url to download\n')
        parser.print_help()
        exit()
    if not options.file:
        options.file = re.search('[^/]*$', options.url).group(0)
    if not options.file or len(options.file) < 1:
        print('Invalid file name specified\n')
        parser.print_help()
        exit()

    log.startLogging(sys.stdout)
    #print "Options:" + options.url
    factory = RTSPClientFactory(options.url, options.file)
    factory.protocol = RDTClient
    factory.bandwidth = 99999999999
    factory.deferred.addCallback(success).addErrback(error)
    reactor.connectTCP(factory.host, factory.port, factory)
    reactor.callLater(1, progress, factory)
    reactor.run()
