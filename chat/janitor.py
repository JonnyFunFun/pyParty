from models import Message
from datetime import datetime, timedelta

def cleanup_old_messages():
    cutoff = datetime.now()-timedelta(1)
    Message.objects.filter(time__lte=cutoff).delete()