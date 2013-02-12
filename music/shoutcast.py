import id3reader, os, array
from models import Request, Music

# shoutcast / buffer constants
CHUNKSIZE = 32*1024
CHUNKS_IN_BUFFER = 32
MINIMUM_BYTES_IN_BUFFER = 2*CHUNKSIZE

class ShoutCastStream(object):
    fd = None

    def __init__(self):
        #self.songSource = songsource.DefaultSongSource
        self.data = array.array('B') # array to hold music data
        self.response = False # we haven't sent the initial response
        self.bytes_to_metadata = CHUNKSIZE # how many bytes are left until we need to send metadata
        # initialize this dispatcher
        self.getNextSong()

    def __iter__(self):
        return self

    # create the metadata string
    def make_metadata(self):
        text = "StreamTitle='%s';"
        if self.id3:
            text = text % self.id3.getValue('title')
        else:
            text = text % ''
        blocks = len(text) // 16 + 1
        metadata = chr(blocks) + text
        metadata = metadata.ljust(blocks * 16 + 1, chr(0)) # add 1 to include the data length byte
        return metadata.encode('ascii')

    # handle getting the next song from the song source
    def getNextSong(self):
        try:
            top_reqs = Request.objects.order_by('received_at','votes')
            if top_reqs.__len__() == 0:
                # pick a random song
                song = Music.objects.order_by('?')[0]
                fileName = song.filename
            else:
                request = top_reqs[0]
                fileName = request.song.filename
                song = request.song
                request.delete()
            # file is gone, delete it and move on to the next one
            if not os.path.exists(fileName):
                song.delete()
                return self.getNextSong()
            self.fd = open(fileName, 'rb')
            self.file_size = os.path.getsize(fileName)
            # if there is valid ID3 data, read it out of the file first,
            # so we can skip sending it to the client
            try:
                self.id3 = id3reader.Reader(self.fd)
                if isinstance(self.id3.header.size, int) and self.id3.header.size < self.file_size: # read out the id3 data
                    self.fd.seek(self.id3.header.size+1, os.SEEK_SET)
            except id3reader.Id3Error:
                self.id3 = None
            self.metadata = self.make_metadata()

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
        # send audio data
        # figure out how much data there is to send and send it
        data = self.data[0:self.bytes_to_metadata]
        data_len = len(data)
        self.bytes_to_metadata -= data_len
        yield data

        # send metadata
        if self.bytes_to_metadata <= 0:
            self.bytes_to_metadata = CHUNKSIZE
            self.metadata = self.make_metadata()
            yield self.metadata

        # get rid of the chunk we just sent - this means the buffer for a client shouldn't exceed 1M in size
        self.data = self.data[data_len:]
        if len(self.data) < MINIMUM_BYTES_IN_BUFFER:
            self.refill_buffer()

    def __del__(self):
        self.fd.close()
