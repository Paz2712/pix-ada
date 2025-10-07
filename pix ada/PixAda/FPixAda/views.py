from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime


# Crea tus views
def index(request):
    __contexto = {
        'pestana': 'FPixAda',
        'tit': 'Prueba título (se llama header, pero no importa mucho)' ## El nombre fué a propósito xdd
    }
    return render(request, 'index.html', __contexto)

def timePage(request):
    return HttpResponse('ass')

'''
De Axius:
Con esto vamos a decirle a Django que renderize las páginas web.
Cada view tiene este formato:

def <view>(request):
    .
    .
    .
    return <algo>

Ese <algo> puede ser una de dos cosas:
un HttpResponse que solo muestra un texto en formato String o,
una función render() que mostrará una página hecha en html que el PABLO debería estar haciendo.

para usar return render() dale 3 parametros

    render(request, <ubicaciónHTML>, <contexto>)

request siempre irá ahí, <ubicaciónHTML> siempre empieza desde la carpeta "templates" de la API,
si quieres mostrar index.html, solo escribes 'index.html', pero si está en una sub carpeta,
escribes '<carpeta>/<archHTML>'

el contexto será todo lo interactivo que usará el HTML.
Digamos que tienes adentro un ciclo que va cambiando cierta variable, crea un diccionario con esa variable que va cambiando,
la cual será usada en el archivo HTML.
'''