from django.http import HttpResponseRedirect
from django.contrib.messages import error


def admin_only(function):
    def wrap(request, *args, **kwargs):

        profile = request.user.get_profile()
        if profile.admin is True:
            return function(request, *args, **kwargs)
        else:
            error(request, "You do not have permission to access that resource.")
            return HttpResponseRedirect('/')

    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap