from global_decorators import render_to
from servers.models import Server
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils import simplejson as json
from servers.forms import GameServerRegistrationForm


@render_to('servers_list.html')
def index(request):
    server_set = Server.objects.filter(mod_approved=True)
    icon = "hdd"
    title = "Current Gameservers"
    return locals()


def info(request, server_id):
    try:
        server = Server.objects.get(id=server_id)
    except Server.DoesNotExist:
        return HttpResponse('{"success": false}', content_type='application/json')
    info = server.info()
    return HttpResponse(json.dumps({'success': True, 'info': info, 'alive': server.host_alive}),
                        content_type='application/json')


@render_to('simple_layouts/form_for_content.html')
def register(request):
    icon = "hdd"
    title = "Register a new Server"
    if request.method == "POST":
        server_data = request.POST.copy()
        server_data['operator'] = request.user.id
        form = GameServerRegistrationForm(data=server_data)
        if form.is_valid():
            form.save()
            messages.success(request, "Your server has been registered and is awaiting administrative approval.")
            return HttpResponseRedirect('/servers/')
        else:
            messages.error(request, "Please correct errors in your submission.")
    else:
        form = GameServerRegistrationForm(initial={'address': request.META['REMOTE_ADDR']})
    return locals()