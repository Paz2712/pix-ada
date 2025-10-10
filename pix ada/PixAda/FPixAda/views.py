from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

'''
Aporte de Maca: sobre las funciones para crear una views
una views es una de las vistas que tiene la pagina, pero más espesificamente es la función que se ejecuta 
cuando alguien estra a una pagina de tu sitio web.
 + que significa que una función retorne render(request, 'index.html', __contexto).
 render: función de django que arma una pag web usando los templates html y a veces datos extras.
 request: es como la petición del usuario (por ejemplo, cuando alguien entra a una URL o hace clic en un botón).
 nombre.html: este es el nombre del archivo html que debe de estar en templates.

 estas funciones se activan cuando las llaman desde urls.py en donde se retorna una pagina armada (render) 
 que a partir de la petición del usuario (request) abra la plantilla html, y si hay datos extras se coloca en el
 tercer parametro.
 
 OSEA: return render(request, 'inicio.html')
 le dice a Django:
“Cuando alguien entre a esta página, muéstrale el archivo inicio.html”.
'''
# Crea tus views
def index(request):
    return render(request, 'index.html')

def algo(request):
    yanMode = request.GET.get('dyslexia', 'false') # El nombre es un placeholder
    displayMode = request.GET.get('displayMode', 'light')
    variables = {
        'dyslexia': yanMode,
        'displayMode': displayMode
    }
    return render(request, 'algo.html', variables)

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
def badApple(request):
    return render(request, 'ba.html')