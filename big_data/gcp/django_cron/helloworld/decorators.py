from django.core.exceptions import PermissionDenied

def request_is_cron(function):
    def wrap(request, *args, **kwargs):
        if request.META.get('HTTP_X_APPENGINE_CRON') !=  None:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
