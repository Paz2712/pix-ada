from django.urls import path
from . import views

'''
De Axius:
Las 'views' servirán para crear las páginas de la app web, en este caso, en la app FPixAda podemos específicar
cómo se verán las URLs con el siguiente formato:
    path("<subURL>, views.<funciónVIEW>, name="<nombreURL>")

La URL se debería ver algo así:
http://127.0.0.1:<puerto>/<subURL>/

Comentaré como se vería la url de cada view abajo para claridad
Diviértete Isi
'''
urlpatterns = [ 
    path("", views.index, name="homepage"), ## http://localhost:8000/  Esta es la página origen de la API
    path("ohno/", views.badApple, name="BadApple"), ## http://localhost:8000/ohno/ Bad apple :D
    path("termycond/", views.contrato, name='termsConditions'), ## http://localhost:8000/EULA/
    path("signin/", views.signinUsuario, name='signin'), ## http://localhost:8000/signin/
    path("login/", views.loginUsuario, name="login"), ## http://localhost:8000/login/
    path("logout/", views.logoutUsuario, name='logout'), ## http://localhost:8000/logout/
    path('foro/', views.foroView, name='foro'), ## http://localhost:8000/foro/
    #path('foro/publicacion/<str:')
    path("foro/crear/", views.crearPubView, name='crearPub'), ## http://localhost:8000/foro/crear/
    path('toadmin/', views.toAdmin, name='redirectAdmin'), ## http://localhost:8000/toadmin/
    path("perfil/<str:userPK>", views.edicion_perfil, name= "perfil"), ## http://127.0.0.1:8000/editarperfil/
]
'''
De Maca: (que hace la función path() y que es urlpatterns)
path() → es una función de Django que crea una “ruta” (URL) dentro del proyecto.

su estructura como puso el axius es:
path("direccion/", funcion_a_ejecutar, name="nombre_opcional")

1- Se espesifica en que subpagina está, si no se pone nada significa que es la pag. principal 
2- Luego viene la función a ejecutar: (tiene que estar definida en el arcibo de views.py) 
se coloca el nombre del archibo en donde esta la función (views.) junto con el nombre de la función (esta en views.py).
------esa función lo que hace es decirle a django que muestre lo indicado por la función------
3- Solo un nombre interno que sirve para referirte a esta URL desde otras partes del proyecto (por ejemplo, en plantillas HTML).

-------------------------------------------------------------------------------
(urlpatterns) 
es una lista que Django usa para saber qué función ejecutar cuando alguien entra a una URL específica.
Piensa en ella como un “mapa de rutas” de tu sitio web.
Cada vez que alguien escribe una dirección (por ejemplo, localhost:8000/testLmao/), Django mira en 
esta lista para decidir qué vista mostrar.

'''
