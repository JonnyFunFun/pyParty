from global_decorators import render_to
from accounts.models import UserProfile
from admin.decorators import admin_only

@admin_only
@render_to('accounts_list.html')
def index(request):
    title = "Accounts"
    icon = "users"
    accounts = UserProfile.objects.all()
    return locals()