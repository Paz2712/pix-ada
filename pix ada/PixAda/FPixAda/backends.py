from django.contrib.auth.backends import BaseBackend
from .models import Usuarios

class UsuariosBackend(BaseBackend):
    # Autentica al usuario con Usuario.nombre (username) y Usuario.contrasena (encriptada)
    def authenticate(self, request, username = None, password = None, **kwargs):
        if username == None or password == None:
            return None
        
        try: # Intentará obtener un nombre de usuario que coincida con el entregado
            user = Usuarios.objects.get(nombre=username)
        except Usuarios.DoesNotExist: # Si no existe, le dice "nu uh"
            return None
        if user.is_active and user.comprobar_contrasena(password):
            return user # Finalmente retornará correctamente el usuario si es activo y la contraseña es la correcta
        return None
    
    def get_user(self, user_id):
        try: # Intentará retornar una primary key (cualquiera) que coincida con user_id
            return Usuarios.objects.get(pk=user_id)
        except Usuarios.DoesNotExist: # Sinó, no :D
            return None
        
    