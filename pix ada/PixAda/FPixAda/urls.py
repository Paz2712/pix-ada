from django.urls import path

from . import views

'''
De Axius:
Las 'views' servirán para crear las páginas de la app web, en este caso, en la app FPixAda podemos específicar
cómo se verán las URLs con el siguiente formato:
    path("<subURL>, views.<funciónVIEW>, name="<nombreURL>")

La URL se debería ver algo así:
http://127.0.0.1:<puerto>/FPixAda/<subURL>/

Comentaré como se vería la url de cada view abajo para claridad
Diviértete Isi
'''
urlpatterns = [
    path("", views.index, name="index"), ## http://localhost:<puerto>/FPixAda/          Esta es la página origen de la API
    path("time/", views.timePage, name="time"), ## http://localhost:<puerto>/FPixAda/time/
]