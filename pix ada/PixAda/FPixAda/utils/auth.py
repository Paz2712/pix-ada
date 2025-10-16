from functools import wraps
from django.shortcuts import redirect

def anonymous_required(redirect_url='homepage'):
    # Si el usuario ya está loggeado, redirige a la página de inicio.
    # Si no ha iniciado sesion, deja pasar a la vista (login/signin).
    # Me robé el código de una discusión en un foro de django
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if getattr(request.user, 'is_authenticated', False):
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
