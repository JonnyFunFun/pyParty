from __future__ import division
from models import Message
from datetime import datetime, timedelta
from django.conf import settings

def cleanup_old_messages():
    cutoff = datetime.now()-timedelta(settings.PARTY_CHAT_MESSAGE_PURGE/24)
    Message.objects.filter(time__lte=cutoff).delete()