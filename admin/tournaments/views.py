from global_decorators import render_to
from admin.decorators import admin_only
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from admin.tournaments.forms import SimpleTournamentForm
from django.contrib import messages
from tournaments.models import Tournament
from datetime import datetime


@render_to('admin_tourney_dashboard.html')
@admin_only
def index(request, tournament_form=None):
    icon = "trophy"
    title = "Tournament Administration Dashboard"
    if not tournament_form:
        tournament_form = SimpleTournamentForm()
    return locals()


@admin_only
@require_POST
def delete(request, tournament_id):
    try:
        tourney = Tournament.objects.get(id=tournament_id)
    except Tournament.DoesNotExist:
        return HttpResponse(simplejson.dumps({"success": False, "error": "Tournament not found"}), mimetype='application/json')
    tourney.delete()
    return HttpResponse(simplejson.dumps({"success": True}), mimetype='application/json')


@admin_only
@require_POST
def save(request):
    tournament_data = request.POST.copy()
    try:
        tournament_data['starts'] = datetime.strptime(tournament_data['starts'], "%Y-%m-%d %H:%M")
        tournament_data['ends'] = datetime.strptime(tournament_data['ends'], "%Y-%m-%d %H:%M")
    except ValueError:
        pass  # this will end up erroring out later
    form = SimpleTournamentForm(data=tournament_data)
    if form.is_valid():
        form.save()
        messages.success(request, "Announcement added successfully!")
        return HttpResponseRedirect('/admin/tournaments/')
    else:
        messages.error(request, "There was an error adding your announcement!")
        return index(request, tournament_form=form)