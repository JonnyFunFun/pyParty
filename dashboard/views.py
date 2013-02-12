# Create your views here.
from decorators import render_to
from admin.settings import get_setting

@render_to('dashboard.html')
def index(request):
    welcome_msg = get_setting('welcome_msg')
    return locals()