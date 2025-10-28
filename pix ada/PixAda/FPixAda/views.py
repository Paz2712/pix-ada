## Lineas 2-3, se encargan de renderizar cosas en la página o redirigir
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.urls import reverse
# Lineas 5-6, funciones predefinidas de login de la mano de Django
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import LoginUsuariosForm, RegistroUsuariosForm, publicacionesForm
from .utils.auth import anonymous_required
from .models import Publicacion, Comentario, Topicos

from random import randint

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
# ---------- Signin y Login ---------- #
@anonymous_required(redirect_url='homepage')
def signinUsuario(request: HttpRequest):
    if request.method == 'POST':
        formulario = RegistroUsuariosForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            login(request, usuario, backend='FPixAda.backends.UsuariosBackend')
            request.session.set_expiry(1800) ## La sesión durará 30[s] * 60 para convertirlo en 30 minutos
            return redirect('homepage')
    else:
        formulario = RegistroUsuariosForm()
    variables = {   
        'form': formulario,
    }
    return render(request, 'registrarse.html', variables)

@anonymous_required(redirect_url='homepage')
def loginUsuario(request: HttpRequest):
    if request.method == 'POST':
        formulario = LoginUsuariosForm(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data['username']
            contrasena = formulario.cleaned_data['password']
            usuario = authenticate(request, username=nombre, password=contrasena, backend='FPixAda.backends.UsuariosBackend')
            if usuario is not None:
                login(request, usuario, backend='FPixAda.backends.UsuariosBackend')
                request.session.set_expiry(30*60) # La sesión durará 30[s] * 60 para convertirlo en 30 minutos
                return redirect('homepage')
            formulario.add_error(None, 'Usuario o contraseña inválidos')
    else:
        formulario = LoginUsuariosForm()
    return render(request, 'iniciarSesion.html', {'form': formulario})

def logoutUsuario(request: HttpRequest):
    logout(request) # Limpia la sesión
    return redirect('login')

# ---------- Other Shit ---------- #
def index(request):
    userID = request.user
    loggeado = userID.is_authenticated
    variables = {
        'usuario': userID,
        'loggeado': loggeado,
        'rol': userID.rol if loggeado else None
    }
    return render(request, 'index.html', variables)

@login_required(login_url='login')
def algo(request):
    userID = request.user
    loggeado = userID.is_authenticated
    variables = {
        'usuario': userID,
        'loggeado': loggeado,
        'rol': userID.rol,
        'page': 'test'
    }   
    return render(request, 'algo.html', variables)


def toAdmin(request: HttpRequest):
    logout(request)
    return redirect(reverse('admin:index'))


def contrato(request):
    return render(request, 'contrato.html')

@login_required(login_url='login')
def foroView(request):
    userID = request.user
    publicacionesForo = Publicacion.objects.all().order_by('-fechaCreacion')
    variables = {
        'usuario': userID,
        'rol': userID.rol,
        'foro': publicacionesForo,
        'page': 'foro',
        'minForo': len(publicacionesForo) >= 25 # Lo pongo para saber si hay más de 10 publicaciones en el foro
    }
    return render(request, 'foro.html', variables)

@login_required(login_url='login')
def crearPubView(request):
    userID = request.user
    if request.method == 'POST':
        formulario = publicacionesForm(request.POST)
        if formulario.is_valid():
            publicacion = formulario.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()
            formulario.save_m2m() # Guarda modelo Many to Many, osea, los topicos
            nuevoTopico = formulario.cleaned_data.get('nuevoTopico')
            if nuevoTopico:
                topico_obj, created = Topicos.objects.get_or_create(nombre=nuevoTopico)
                publicacion.topico.add(topico_obj)
            return redirect('foro')
    else:
        formulario = publicacionesForm()
    variables = {
        'form': formulario,
        'usuario': userID,
        'rol': userID.rol,
    }
    return render(request, 'crearPub.html', variables)

def qanda(request):
    return render(request, "giasfelfebrehber.html", )


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
# ---------- :D ---------- #
def badApple(request):
    '''when te das cuenta de que puedes programar
    lo que sea:'''
    return render(request, 'ba.html')


def Prueba(request):
    lista = [0, 1, 2, 3, "no 4", 5]
    chance= randint(-1,9)
    variables = { 
        'coin': chance,
        'lista': lista,
    }
    return render(request, "prueba.html", variables)

def gambling(request):
    import random 
    dado= random.randint(1,20)
    dot = {"punto": dado
    }
    return (request, "prueba.html", dot)

def indexnuevo(request):
    return render(request, 'indexnuevo.html')
