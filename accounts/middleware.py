from models import UserProfile, FLAG_ADMIN
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib import messages
from admin.settings import get_setting
from django.conf import settings
import random, string


class PyPartyAccountAndAuthenticationMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated():
            return
        hostname = request.META['REMOTE_HOST'] or request.META['REMOTE_ADDR']
        try:
            # reverse the profile back to user based on hostname
            up = UserProfile.objects.get(hostname=hostname)
            user = up.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            request.user = user
            auth.login(request, up.user)
            if request.path not in ['/favicon.ico'] and not settings.STATIC_URL in request.path:
                if up.departed:
                    up.departed = False
                    up.save()
                    messages.success(request, "Welcome back to the LAN!")
        except UserProfile.DoesNotExist:
            # if we're the first user, we're always an admin
            first_admin = (User.objects.count() == 0)
            # add a new user
            random_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(12))
            username = request.META['REMOTE_HOST'] or 'User-'+''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
            user = User.objects.create_user(username, None, random_password)
            user.save()
            profile = UserProfile()
            profile.user = user
            profile.hostname = hostname
            if first_admin:
                profile.set_flag(FLAG_ADMIN)
            profile.save()
            request.user = user
            user = auth.authenticate(username=username, password=random_password)
            auth.login(request, user)
            if first_admin:
                # redirect to admin panel for setup
                messages.success(request, "Welcome to pyParty!  As the first user, you're automatically an admin.  Please continue setting up pyParty as you normally would!")
                return HttpResponseRedirect('/admin/')
            else:
                messages.success(request, "Welcome to %s!  We set up an account for you.  There's no need for a password, you will be recognized by your computer.  Feel free to <a href='/accounts/profile/'>continue setting up your profile</a>." % get_setting('lan_name'))