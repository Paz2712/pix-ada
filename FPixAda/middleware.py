from django.shortcuts import redirect
from .models import Usuarios

class AdminRedirectIfUsuariosMiddleware:
    # Una pequeña sorpresa para el usuario que intente ir a la página de admin
    # Finalmente un uso para la página de Bad Apple
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info or ''
        u = getattr(request, 'user', None)

        # Solo interceptamos URLs del admin y solo si el usuario está autenticado en la página
        if path.startswith('/pixis/admin/') and isinstance(u, Usuarios):
            return redirect('BadApple') # Magia damas y caballeros

        return self.get_response(request)
    
## Le pedí ayuda a alguien en reddit para hacer esto, tenía muchas ganas de hacer algo así xdd