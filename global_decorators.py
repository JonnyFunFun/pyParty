from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.messages import warning
from admin.settings import get_setting

def render_to_response(request, template_name, context_dict = {}):
    from django.template import RequestContext
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict)
    context.update(csrf(request))
    return _render_to_response(template_name, context_instance=context)

def render_to(template_name):
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if not isinstance(output, dict):
                return output
            return render_to_response(request, template_name, output)
        return wrapper
    return renderer

def require_section_enabled(section_name):
    def requirement(func):
        def wrapper(request, *args, **kw):
            if get_setting('enable_%s' % section_name) != '1':
                warning(request, "That module is not enabled.")
                return HttpResponseRedirect('/')
            return func(request, *args, **kw)
        return wrapper
    return requirement