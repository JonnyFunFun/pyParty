from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseBadRequest
from chat.models import Message
import simplejson as json

@require_POST
def sync(request):
    last_message = request.POST.get('last',None)
    if last_message is None:
        messages = Message.objects.all()
    else:
        messages = Message.objects.filter(id__gt=last_message)
    ret = []
    for message in messages:
        ret.append(message.chatbox_element)
    return HttpResponse(json.dumps({'success': True, 'messages': ret}), content_type='application/json')


@require_POST
def post(request):
    message = request.POST.get('message',None)
    if message is None:
        return HttpResponseBadRequest
    new_msg = Message()
    new_msg.message = message
    new_msg.user = request.user
    new_msg.save()
    return HttpResponse(json.dumps({'success': True, 'child': new_msg.chatbox_element}), content_type='application/json')