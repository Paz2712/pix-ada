from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from django.middleware.csrf import get_token

from .forms import RegistroUsuariosForm, LoginUsuariosForm
from .models import Usuarios

SESSION_KEY = "usuario_id"

def sesionLogin(request, usuario: Usuarios):
    request.session.flush()
    request.session.cycle_key()
    # flush + cycle_key mitiga la sesión anterior, si es que quedó una

    request.session[SESSION_KEY] = usuario.id
    request.session["usuario_alias"] = usuario.aliasUsuario
    request.session["usuario_nombre"] = usuario.nombre
    request.session["usuario_rol"] = usuario.rol
    request.session["usuario_tz"] = timezone.now().isoformat() # Obtiene la zona horaria del usuario y hora de login

    request.session.set_expiry(0)
    # Expira la sesión al cerrar el navegador

def sesionLogout(request):
    # Elimina la sesion actual
    request.session.flush()

def obtenerUsuario(request):
    uid = request.session.get(SESSION_KEY)
    if not uid:
        return None
    try:
        return Usuarios.objects.get(pk=uid)
    except Usuarios.DoesNotExist:
        return None

def loginRequerido(funcionView):
    # Protege las páginas de nuestra app web con mi desastrosos login
    # Lo unico bueno es que nos permite personalizar casi todo, pero es un dolor de huevos
    def _wrapped(request, *args, **kwargs):
        # El código no es mío, se lo robé a alguien en stackoverflow y lo modifiqué ligeramente
        usuario = obtenerUsuario(request)
        if usuario is None:
            messages.info(request, "Para continuar, inicia sesión")
            return redirect("login")
