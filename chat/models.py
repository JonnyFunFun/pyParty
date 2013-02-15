from django.db import models
from django.contrib.auth.models import User
from django.utils import formats
from django.template import defaultfilters

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)

    @property
    def chatbox_element(self):
        return """
            <div class="chat-out" data-id="%s">
                <span class="chat-time">%s</span>
                <strong class="chat-user color-%s">%s: </strong>
                <div class="chat-text">%s</div>
            </div>
            """ % (self.id,
                   self.time.strftime("%I:%M%p").lower(),
                   self.user.get_profile().chat_color,
                   self.user.username,
                   self.message)