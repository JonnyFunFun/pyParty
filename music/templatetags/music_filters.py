from django import template
from music.models import Request


register = template.Library()


@register.filter
def has_requested(user, music):
    try:
        req = Request.objects.get(fulfilled=False, song=music)
    except Request.DoesNotExist:
        return False
    return req.requestvote_set.filter(requester=user).count() != 0