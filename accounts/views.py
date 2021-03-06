from global_decorators import render_to
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from admin.settings import get_setting
from accounts.survey.forms import DepartingSurvey
from accounts.forms import ProfileForm


@render_to('edit_profile.html')
def edit_profile(request):
    title = "Edit My Profile"
    icon = "edit"
    form = ProfileForm(instance=request.user.profile, initial={'username': request.user.username,
                                                               'first_name': request.user.first_name,
                                                               'last_name': request.user.last_name})
    return locals()


# shortcut
def view_profile(request):
    return HttpResponseRedirect('/accounts/user/%s' % request.user.username.lower())


@require_POST
@render_to('edit_profile.html')
def save_profile(request):
    title = "Edit My Profile"
    icon = "edit"
    if request.POST.get('save_changes'):
        form = ProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if form.is_valid():
            if request.POST.get('username', request.user.username) != request.user.username:
                # change username
                try:
                    check = User.objects.get(username=request.POST.get('username'))
                    messages.error(request, 'That username has already been taken!')
                    return locals()
                except User.DoesNotExist:
                    request.user.username = request.POST.get('username')
                    request.user.save()
            form.save()
            request.user.first_name = request.POST.get('first_name', request.user.first_name)
            request.user.last_name = request.POST.get('last_name', request.user.last_name)
            request.user.save()
            messages.success(request, 'Your profile has been updated!')
        else:
            messages.error(request, 'Unable to save changes to your profile!')
            return locals()
    return view_profile(request)


@render_to('view_profile.html')
def user(request, username):
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        messages.error(request, 'Unable to find a user by the name %s' % username)
        return HttpResponseRedirect('/')
    title = user.username
    message = user.get_full_name()
    icon = "user"
    return locals()


@render_to('list_users.html')
def list_users(request):
    title = "The Attendees"
    icon = "user"
    users = User.objects.all().order_by("id")
    return locals()


@render_to('depart_lan.html')
def departing(request):
    title = "Leaving the LAN?"
    icon = "signout"
    do_survey = get_setting('goodbye_survey') == '1'
    survey = DepartingSurvey()
    return locals()


@render_to('thanks_for_coming.html')
def do_departure(request):
    if request.method == 'POST' and get_setting('goodbye_survey') == '1':
        survey = DepartingSurvey(data=request.POST)
        try:
            survey.save()
        except:
            pass  # don't fail here
    profile = request.user.profile
    profile.departed = True
    profile.save(force_update=True)
    logout(request)
    return locals()
