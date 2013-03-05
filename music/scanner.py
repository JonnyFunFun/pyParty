from models import Music, MusicSource
from django.db import IntegrityError
from os.path import join, splitext
import id3reader
import os


def scan_media(source_id=None):
    yield """
        <html>
            <head>
                <script type="text/javascript">
                    scrollBottom = function() {
                        window.scrollTo(0, document.body.scrollHeight);
                    }
                </script>
            </head>
            <body>
    """

    music_added = 0

    if not source_id:
        sources = MusicSource.objects.all()
        for source in sources:
            yield "<div><em>Scanning <strong>%s</strong></em></div>" % source.path
            for root, dirs, files in os.walk(source.path, topdown=False):
                yield "<div>%s</div>" % root
                yield " " * 1024  # encourage incremental rendering
                for f in files:
                    f = join(root, f)
                    music_added += process_file(f, source.id) or 0
    else:
        source = MusicSource.objects.get(id=source_id)
        yield "<div><em>Scanning <strong>%s</strong></em></div>" % source.path
        for root, dirs, files in os.walk(source.path, topdown=False):
            yield "<div>%s</div>" % root
            yield " " * 1024  # encourage incremental rendering
            yield "<script type=\"text/javascript\">scrollBottom();</script>"
            for f in files:
                f = join(root, f)
                music_added += process_file(f, source.id) or 0
    yield """
                <br/><br/>
                <strong>Done!</strong><br/>
                %s music files were added or updated!
                <script type=\"text/javascript\">scrollBottom();</script>
            </body>
        </html>
    """ % music_added


def process_folder(directory):
    try:
        content = [os.path.join(directory, x) for x in os.listdir(directory)]
    except OSError:
        return

    yield directory

    dirs = sorted([x for x in content if os.path.isdir(x)])
    files = sorted([x for x in content if os.path.isfile(x)])

    for f in files:
        if not os.path.islink(f):
            process_file(f)

    for d in dirs:
        if not os.path.islink(d):
            yield process_folder(d)


def process_file(f, source_id):
    extension = splitext(f)[1].lower()
    if extension == '.mp3':
        # found a MP3!
        id3 = id3reader.Reader(f)
        album = id3.getValue('album')
        artist = id3.getValue('performer') or album
        title = id3.getValue('title')
        try:
            m = Music.objects.get(filename=f)
        except Music.DoesNotExist:
            # new one
            m = Music()
        if title is not None and artist is not None:
            m.album = album
            m.artist = artist
            m.title = title
        else:
            # determine it from the filename? TODO
            return 0  #skip for now
        m.filename = f
        m.source_id = source_id
        try:
            m.save()
            return 1
        except IntegrityError:
            # probably missing information, skip it
            pass
    return 0
