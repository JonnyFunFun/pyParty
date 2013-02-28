from music.models import Music
Music.objects.filter(playing=True).update(playing=False)
print "Cleared running music flag."