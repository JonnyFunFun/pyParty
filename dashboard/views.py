# Create your views here.
from global_decorators import render_to
from admin.settings import get_setting

@render_to('dashboard.html')
def index(request):
    message = get_setting('welcome_msg')
    title = "Dashboard"
    icon = "home"
    return locals()