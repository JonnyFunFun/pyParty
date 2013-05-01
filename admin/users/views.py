from global_decorators import render_to
from accounts.models import UserProfile, FLAG_ADMIN, FLAG_OP, FLAG_VIP
from admin.decorators import admin_only
from django.contrib import messages
from django.http import HttpResponseRedirect
from admin.users.forms import AdminProfileForm
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST


@admin_only
@render_to('accounts_list.html')
def index(request):
    title = "Accounts"
    icon = "user"
    accounts = UserProfile.objects.all()
    return locals()


@admin_only
@render_to("accounts_edit.html")
def edit(request, user_id):
    try:
        profile = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        messages.error(request, "Unable to find a user with ID %s" % user_id)
        return HttpResponseRedirect('/admin/users/')
    title = "Edit %s" % profile.user.username
    icon = "users"
    form = AdminProfileForm(instance=profile, initial={'username': profile.user.username,
                                                       'first_name': profile.user.first_name,
                                                       'last_name': profile.user.last_name,
                                                       'admin': profile.admin,
                                                       'op': profile.operator,
                                                       'vip': profile.vip})
    form.helper.form_action = "/admin/users/%s/save/" % user_id
    return locals()


@admin_only
@render_to("accounts_delete.html")
def delete(request, user_id):
    try:
        profile = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        messages.error(request, "Unable to find a user with ID %s" % user_id)
        return HttpResponseRedirect('/admin/users/')
    title = "Edit %s" % profile.user.username
    icon = "users"
    if request.POST.get('axn') == 'delete':
        # do it!
        profile.user.delete()
        messages.success(request, "The user %s has been deleted!" % profile.user.username)
        return HttpResponseRedirect("/admin/users/")
    elif request.POST.get('axn') == 'cancel':
        return HttpResponseRedirect("/admin/users/")
    return locals()


@admin_only
@require_POST
@render_to("accounts_edit.html")
def save(request, user_id):
    try:
        profile = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        messages.error(request, "Unable to find a user with ID %s" % user_id)
        return HttpResponseRedirect('/admin/users/')
    title = "Edit %s" % profile.user.username
    icon = "users"
    if request.POST.get('save_changes'):
        form = AdminProfileForm(data=request.POST, files=request.FILES, instance=profile)
        form.helper.form_action = "/admin/users/%s/save/" % user_id
        if form.is_valid():
            if request.POST.get('username', profile.user.username) != profile.user.username:
                # change username
                try:
                    check = User.objects.get(username=request.POST.get('username'))
                    messages.error(request, 'That username has already been taken!')
                    return locals()
                except User.DoesNotExist:
                    profile.user.username = request.POST.get('username')
                    profile.user.save()
            form.save()
            # flags
            if request.POST.get('admin', 'off') == 'on' and not profile.admin:
                profile.set_flag(FLAG_ADMIN)
            if request.POST.get('op', 'off') == 'on' and not profile.operator:
                profile.set_flag(FLAG_OP)
            if request.POST.get('vip', 'off') == 'on' and not profile.vip:
                profile.set_flag(FLAG_VIP)
            profile.save()
            # first/last name
            profile.user.first_name = request.POST.get('first_name', profile.user.first_name)
            profile.user.last_name = request.POST.get('last_name', profile.user.last_name)
            profile.user.save()
            messages.success(request, 'The profile has been updated!')
        else:
            messages.error(request, 'Unable to save changes to the profile!')
            return locals()
    return HttpResponseRedirect("/admin/users/")