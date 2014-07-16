from admin.decorators import admin_only
from django.views.decorators.http import require_POST
from announcements.models import Announcement
from admin.news.forms import AnnouncementForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson


@admin_only
@require_POST
def delete(request, news_id):
    try:
        news = Announcement.objects.get(id=news_id)
    except Announcement.DoesNotExist:
        return HttpResponse(simplejson.dumps({"success": False, "error": "News article not found"}), mimetype='application/json')
    news.delete()
    return HttpResponse(simplejson.dumps({"success": True}), mimetype='application/json')


@admin_only
@require_POST
def save(request):
    announcement_data = request.POST.copy()
    announcement_data['author'] = request.user.id
    form = AnnouncementForm(data=announcement_data)
    if form.is_valid():
        form.save()
        messages.success(request, "Announcement added successfully!")
    else:
        messages.error(request, "There was an error adding your announcement!")
    return HttpResponseRedirect('/admin/')


@admin_only
def index(request):
    return HttpResponseRedirect('/admin/')