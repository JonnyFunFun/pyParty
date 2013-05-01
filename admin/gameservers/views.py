from global_decorators import render_to
from admin.decorators import admin_only
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_POST
from servers.models import Server
from forms import GameServerForm
import simplejson as json


@render_to('gameserver_list.html')
@admin_only
def index(request, form=None):
    servers = Server.objects.all()
    icon = "hdd"
    title = "Server Administration"
    return locals()


@admin_only
@render_to('simple_layouts/form_for_content.html')
def add(request, form=None):
    if form is None:
        form = GameServerForm()
    icon = "hdd"
    title = "Add a new server"
    return locals()


@admin_only
@render_to('simple_layouts/form_for_content.html')
def edit(request, server_id, form=None):
    try:
        edit_server = Server.objects.get(id=server_id)
    except Server.DoesNotExist:
        messages.error(request, "Unable to find server with id %d to edit" % server_id)
        return HttpResponseRedirect('/admin/servers/')
    if form is None:
        form = GameServerForm(instance=edit_server)
        form.helper.form_action = "/admin/servers/%s/save/" % server_id
    icon = "hdd"
    title = "Update server #%d" % form.instance.id
    return locals()


@admin_only
@require_POST
def save(request, server_id):
    if server_id:
        try:
            server = Server.objects.get(id=server_id)
        except Server.DoesNotExist:
            messages.error(request, "Unable to find server with id %s to edit" % server_id)
            return HttpResponseRedirect('/admin/servers/')
        form = GameServerForm(data=request.POST, instance=server)
    else:
        form = GameServerForm(data=request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Changes saved scucessfully!!" if server_id else "Server added!")
        return HttpResponseRedirect('/admin/servers/')
    else:
        messages.error(request, "Please correct your errors and try again.")
    if form.instance.pk is None:
        return add(request, form=form)
    return edit(request, form.instance.pk, form=form)


@admin_only
@require_POST
def delete(request, server_id):
    try:
        server = Server.objects.get(id=server_id)
    except Server.DoesNotExist:
        return HttpResponse(json.dumps({"success": False, "error": "Server not found"}), content_type='application/json')
    server.delete()
    return HttpResponse(json.dumps({"success": True}), content_type='application/json')


@admin_only
@require_POST
def alive(request, server_id):
    try:
        try:
            server = Server.objects.get(id=server_id)
        except Server.DoesNotExist:
            return HttpResponse(json.dumps({"success": False, "error": "Server not found"}), content_type='application/json')
        return HttpResponse(json.dumps({"success": True, "status": server.host_alive}), content_type='application/json')
    except:
        return HttpResponse(json.dumps({"success": False, "error": "Unknown"}), content_type='application/json')


@admin_only
def approve(request, server_id):
    try:
        server = Server.objects.get(id=server_id)
        server.mod_approved = True
        server.save()
        messages.success(request, "Server %s approved." % server_id)
    except Server.DoesNotExist:
        messages.error(request, "Unable to find the server with id %s" % server_id)
    return HttpResponseRedirect('/admin/servers/')