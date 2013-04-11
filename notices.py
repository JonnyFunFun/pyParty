from django.http import HttpResponse
from servers.models import Server
from music.models import Music
from tourneys.models import Tournament
from admin.settings import get_setting
from django.utils import simplejson as json
from datetime import datetime, timedelta


def get_notices(request):
    notices = []
    # upcoming tournament notices
    if get_setting('enable_tournaments') == '1':
        upcoming = Tournament.objects.filter(starts__lte=(datetime.now() + timedelta(hours=1)))
        if upcoming.count() == 1:
            notices.append("The tournament %s is starting within the hour" % upcoming[0].name)
        elif upcoming.count() > 1:
            notices.append("%d tournaments are starting within the hour" % upcoming.count())
    # get admin notices
    if request.user.is_admin:
        # servers needing approval
        servers_unapproved = Server.objects.filter(mod_approved=False)
        if servers_unapproved.count() is not 0:
            notices.append("%d servers require admin approval." % servers_unapproved.count())
        # jukebox is not running
        if get_setting('enable_music') == '1' and Music.currently_playing() is None:
            notices.append("No music is currently playing!")
    # and return the lot of them
    return HttpResponse(json.dumps(notices), content_type='application/json')