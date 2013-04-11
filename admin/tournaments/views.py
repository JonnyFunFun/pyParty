from global_decorators import render_to
from admin.decorators import admin_only


@render_to('admin_tourney_dashboard.html')
@admin_only
def index(request):
    icon = "trophy"
    title = "Tournament Administration Dashboard"
    return locals()