from django.contrib import admin
from .models import Usuarios, Topicos, Publicacion, perfilusuario


'''
Todo esto se va a mostrar en la página
http://localhost:8000/admin/ la cual es de uso exclusivo nuestro

Recomiendo que hagan su cuenta de superusuario. Abran la terminal en
la carpeta donde está manage.py y escriban

py manage.py createsuperuser

y completen sus datos, el correo es opcional, pero
recomiendo ponerlo, les llegará correos cada que falle algo en la página
con detalles

Listo, eres admin de la página, lamentablemente no puedo ver
sus contraseñas por estar automaticamente encriptadas, así que
se salvaron por el momento

    - Axius
'''

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = (
        "pk", "nombre", "aliasUsuario", "correo", "rol", "creado",
    )
    fields = ( 
        "nombre", "aliasUsuario", "correo", "contrasena", "rol", 
        "yanMode", "altoContraste", "creado",
    )
    list_filter = ("rol", "creado",)
    search_fields = ("nombre", "aliasUsuario", "correo")
    readonly_fields = ("creado",)
    

@admin.register(Topicos)
class TopicosAdmin(admin.ModelAdmin):
    list_display = ("nombre",)

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ( # Lo que se ve desde el menú general
        "idPublicacion", "autor", "esAnonimo", "fechaCreacion",
        "titulo"
    )
    fields = ( # Las entradas que aparecerán en el formulario
        "idPublicacion", "autor", "esAnonimo",
        "titulo", "cuerpo", "topico"
    )
    readonly_fields = ("idPublicacion",) # Cuales campos NO pueden ser editados manualmente
    list_filter = ("autor", "esAnonimo", "fechaCreacion", "topico") # Las categorías que apareceran en los filtros de búsqueda
    search_fields = ("titulo", "autor") # Lo que usará el buscador para encontrar

@admin.register(perfilusuario)
class perfilusuarioAdmin(admin.ModelAdmin):
    list_display = ('user',)
    fields = ('description', 'user')
    search_fields = ('user',)
    readonly_fields = ('user',)