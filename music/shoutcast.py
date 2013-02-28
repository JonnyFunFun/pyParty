from models import Music
from django.core.urlresolvers import resolve
import id3reader
import os
import array
import logging


# shoutcast / buffer constants
CHUNKSIZE = 32 * 1024
CHUNKS_IN_BUFFER = 32
MINIMUM_BYTES_IN_BUFFER = 4 * CHUNKSIZE


class ShoutCastStream(object):
    fd = None

    def __init__(self, request):
        self.data = array.array('B')  # array to hold music data
        self.request = request
        self.url = self.request.path
        self.response = False # we haven't sent the initial response
        self.response_data = [
            "ICY 200 OK\r\n",
            "icy-notice1:<BR>This stream requires\r\n",
            "icy-notice2:Winamp, or another streaming media player<BR>\r\n",
            "icy-name:pyParty ShoutCast\r\n",
            "icy-genre:Mixed\r\n",
            "icy-url:%s\r\n" % self.url,
            "icy-pub:1\r\n",
            "icy-br:128\r\n\r\n"
        ]
        print "Starting streaming to %s (%s)" % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_USER_AGENT'))
        self.getNextSong()

    def __iter__(self):
        return self

    # handle getting the next song from the song source
    def getNextSong(self):
        try:
            song, request = Music.next_song_and_request()
            # file is gone, delete it and move on to the next one
            fileName = song.filename
            if not os.path.exists(fileName):
                song.delete()
                return self.getNextSong()
            if request:
                request.fulfilled = True
                request.save()
            Music.objects.filter(playing=True).update(playing=False)
            song.playing = True
            song.save()
            print "Next song to play: %s" % fileName
            self.fd = open(fileName, 'rb')
            self.file_size = os.path.getsize(fileName)
            # if there is valid ID3 data, read it out of the file first,
            # so we can skip sending it to the client
            try:
                self.id3 = id3reader.Reader(self.fd)
                if isinstance(self.id3.header.size, int) and self.id3.header.size < self.file_size: # read out the id3 data
                    self.fd.seek(self.id3.header.size + 1, os.SEEK_SET)
            except id3reader.Id3Error:
                self.id3 = None

        except StopIteration:
            fileName = None
            self.fd = None
        except IOError:
            self.fd = None

    # refill the buffer
    def refill_buffer(self):
        try:
            if self.fd: # could be None
                for i in range(0, CHUNKS_IN_BUFFER):
                    self.data.fromfile(self.fd, CHUNKSIZE)
        except EOFError:
            self.fd.close()
            self.getNextSong()

    def next(self):
        if not self.response:
            data = array.array("B")
            for i in self.response_data:
                for elem in i:
                    data.append(ord(elem))
            self.response = True
        else:
            # send audio data
            # figure out how much data there is to send and send it
            data = self.data[0:CHUNKSIZE]
            data_len = len(data)
            # get rid of the chunk we just sent - this means the buffer for a client shouldn't exceed 1M in size
            self.data = self.data[data_len:]
            if len(self.data) < MINIMUM_BYTES_IN_BUFFER:
                self.refill_buffer()
        return data.tostring()

    def __del__(self):
        self.fd.close()
        Music.objects.filter(playing=True).update(playing=False)
        print "Shoutcast stream closed."
