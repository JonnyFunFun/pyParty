from models import UserProfile
from django.contrib.auth.models import User
from django.contrib import auth
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
        except UserProfile.DoesNotExist:
            # add a new user
            random_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(12))
            username = request.META['REMOTE_HOST'] or 'User-'+''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
            user = User.objects.create_user(username, None, random_password)
            user.save()
            profile = UserProfile()
            profile.user = user
            profile.hostname = hostname
            profile.save()
            request.user = user
            user = auth.authenticate(username=username, password=random_password)
            auth.login(request, user)