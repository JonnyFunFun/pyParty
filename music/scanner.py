from models import Music, MusicSource
import id3reader, os

def scan_media():
    sources = MusicSource.objects.all()
    for source in sources:
        yield process_folder(source.path)

def process_folder(directory):
    yield directory
    try:
        content = [os.path.join(directory, x) for x in os.listdir(directory)]
    except OSError:
        return

    dirs = sorted([x for x in content if os.path.isdir(x)])
    files = sorted([x for x in content if os.path.isfile(x)])

    for f in files:
        if not os.path.islink(f):
            process_file(f)

    for d in dirs:
        if not os.path.islink(d):
            yield process_folder(d)

def process_file(file):
    try:
        # found a MP3!
        id3 = id3reader.Reader(file)
        try:
            Music.objects.get(filename=file)
        except Music.DoesNotExist:
            album = id3.getValue('album')
            artist = id3.getValue('artist')
            title = id3.getValue('title')
            m = Music()
            m.album = album
            m.artist = artist
            m.title = title
            m.filename = file
            m.save()
    except:
        pass
