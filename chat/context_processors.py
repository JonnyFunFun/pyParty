from models import Message
from janitor import cleanup_old_messages

def chat_box_messages(context):
    cleanup_old_messages()
    return {'chat_messages': Message.objects.order_by("time")}