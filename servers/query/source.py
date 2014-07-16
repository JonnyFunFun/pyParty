# Work: getInfo(), getPlayers(), getChallenge(), getRules(), getPing()
# Support: Source Servers, GoldSrc servers, The Ship Servers
# ToDo: Bugfixes

__author__ = 'Dasister'
__site__ = 'http://21games.ru'
__description__ = 'Simple Query Class for VALVe servers'

A2S_INFO = b'\xFF\xFF\xFF\xFFTSource Engine Query\x00'
A2S_PLAYERS = b'\xFF\xFF\xFF\xFF\x55'
A2S_RULES = b'\xFF\xFF\xFF\xFF\x56'

S2A_INFO_SOURCE = chr(0x49)
S2A_INFO_GOLDSRC = chr(0x6D)

import socket
import time
import struct


class SourceQuery(object):
    def __init__(self, addr, port = 27015, timeout = 5.0):
        self.ip, self.port, self.timeout = socket.gethostbyname(addr), port, timeout
        self.sock = False
        self.challenge = False

    def disconnect(self):
        if self.sock:
            self.sock.close()
            self.sock = False

    def connect(self):
        self.disconnect()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.ip, self.port))

    def getPing(self):
        return self.getInfo()['ping']

    def getInfo(self):
        self.connect()
        self.sock.send(A2S_INFO)
        before = time.time()
        try:
            data = self.sock.recv(4096)
        except:
            raise
            #return False

        after = time.time()
        data = data[4:]

        self.result = {}

        header, data = self.getByte(data)
        self.result['ping'] = int((after - before) * 1000)
        if chr(header) == S2A_INFO_SOURCE:
            self.result['protocol'], data = self.getByte(data)
            self.result['hostname'], data = self.getString(data)
            self.result['map'], data = self.getString(data)
            self.result['gamedir'], data = self.getString(data)
            self.result['gamedesc'], data = self.getString(data)
            self.result['appid'], data = self.getShort(data)
            self.result['bumplayers'], data = self.getByte(data)
            self.result['maxplayers'], data = self.getByte(data)
            self.result['bots'], data = self.getByte(data)
            self.dedicated, data = self.getByte(data)
            if chr(self.dedicated) == 'd':
                self.result['dedicated'] = 'Dedicated'
            elif self.dedicated == 'l':
                self.result['dedicated'] = 'Listen'
            else:
                self.result['dedicated'] = 'SourceTV'

            self.os, data = self.getByte(data)
            if chr(self.os) == 'w':
                self.result['os'] = 'Windows'
            else:
                self.result['os'] = 'Linux'
            self.result['password'], data = self.getByte(data)
            self.result['secure'], data = self.getByte(data)
            if self.result['appid'] == 2400: # The Ship server
                self.result['gamemode'], data = self.getByte(data)
                self.result['witnesscount'], data = self.getByte(data)
                self.result['witnesstime'], data = self.getByte(data)
            self.result['Version'], data = self.getString(data)
            self.edf, data = self.getByte(data)
            try:
                if (self.edf & 0x80):
                    self.result['gameport'], data = self.getShort(data)
                if (self.edf & 0x10):
                    self.result['steamid'], data = self.getLongLong(data)
                if (self.edf & 0x40):
                    self.result['specport'], data = self.getShort(data)
                    self.result['specname'], data = self.getString(data)
                if (self.edf & 0x10):
                    self.result['tags'], data = self.getString(data)
            except:
                pass
        elif chr(header) == S2A_INFO_GOLDSRC:
            self.result['gameip'], data = self.getString(data)
            self.result['hostname'], data = self.getString(data)
            self.result['map'], data = self.getString(data)
            self.result['gamedir'], data = self.getString(data)
            self.result['gamedesc'], data = self.getString(data)
            self.result['players'], data = self.getByte(data)
            self.result['maxplayers'], data = self.getByte(data)
            self.result['version'], data = self.getByte(data)
            self.dedicated, data = self.getByte(data)
            if chr(self.dedicated) == 'd':
                self.result['dedicated'] = 'Dedicated'
            elif self.dedicated == 'l':
                self.result['dedicated'] = 'Listen'
            else:
                self.result['dedicated'] = 'HLTV'
            self.os, data = self.getByte(data)
            if chr(self.os) == 'w':
                self.result['os'] = 'Windows'
            else:
                self.result['os'] = 'Linux'
            self.result['password'], data = self.getByte(data)
            self.result['ismod'], data = self.getByte(data)
            if self.result['ismod']:
                self.result['URLInfo'], data = self.getString(data)
                self.result['URLDownload'], data = self.getString(data)
                data = self.getByte(data)[1] # NULL-Byte
                self.result['ModVersion'], data = self.getLong(data)
                self.result['ModSize'], data = self.getLong(data)
                self.result['ServerOnly'], data = self.getByte(data)
                self.result['ClientDLL'], data = self.getByte(data)
            self.result['secure'], data = self.getByte(data)
            self.result['bots'], data = self.getByte(data)

        return self.result

    # <------------------getInfo() End -------------------------->

    def getChallenge(self):
        if not self.sock:
            self.connect()
        self.sock.send(A2S_PLAYERS + b'0xFFFFFFFF')
        try:
            data = self.sock.recv(4096)
        except:
            return False

        self.challenge = data[5:]

        return True
    # <-------------------getChallenge() End --------------------->


    def getPlayers(self):
        if not self.sock:
            self.connect()
        if not self.challenge:
            self.getChallenge()

        self.sock.send(A2S_PLAYERS + self.challenge)
        try:
            data = self.sock.recv(4096)
        except:
            return False

        data = data[4:]

        header, data = self.getByte(data)
        num, data = self.getByte(data)
        self.result = []
        try:
            for i in range(num):
                player = {}
                data = self.getByte(data)[1]
                player['id'] = i + 1 # ID of All players is 0
                player['Name'], data = self.getString(data)
                player['Frags'], data = self.getLong(data)
                player['Time'], data = self.getFloat(data)
                player['FTime'] = time.gmtime(int(player['Time']))
                self.result.append(player)

        except:
            pass

        return self.result

    # <-------------------getPlayers() End ----------------------->

    def getRules(self):
        if not self.sock:
            self.connect()
        if not self.challenge:
            self.getChallenge()

        self.sock.send(A2S_RULES + self.challenge)
        try:
            data = self.sock.recv(4096)
            if data[0] == '\xFE':
                num_packets = ord(data[8]) & 15
                packets = [' ' for i in range(num_packets)]
                for i in range(num_packets):
                    if i != 0:
                        data = self.sock.recv(4096)
                    index = ord(data[8]) >> 4
                    packets[index] = data[9:]
                data = ''
                for i, packet in enumerate(packets):
                    data = data + packet
        except:
            return False
        data = data[4:]

        header, data = self.getByte(data)
        num, data = self.getShort(data)
        self.result = {}

        #Server sends incomplete packets. Ignore "NumPackets" value.
        while 1:
            try:
                ruleName, data = self.getString(data)
                ruleValue, data = self.getString(data)
                if ruleValue:
                    self.result[ruleValue] = ruleName
            except:
                break

        return self.result

    # <-------------------getRules() End ------------------------->

    def getByte(self, data):
        return (data[0], data[1:])

    def getShort(self, data):
        return (struct.unpack('<h', data[0:2])[0], data[2:])

    def getLong(self, data):
        return (struct.unpack('<l', data[0:4])[0], data[4:])

    def getLongLong(self, data):
        return (struct.unpack('<Q', data[0:8])[0], data[8:])

    def getFloat(self, data):
        return (struct.unpack('<f', data[0:4])[0], data[4:])

    def getString(self, data):
        s = ""
        i = 0
        while chr(data[i]) != '\x00':
            s += chr(data[i])
            i += 1
        return (s, data[i + 1:])

