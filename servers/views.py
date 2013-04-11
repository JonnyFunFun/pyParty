from global_decorators import render_to
from models import Server
from django.http import HttpResponse
from django.utils import simplejson as json


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