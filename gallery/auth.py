from functools import wraps
from django.shortcuts import redirect

def gallery_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('gallery_authenticated', False):
            return redirect('enter')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
