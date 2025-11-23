## Lineas 2-3, se encargan de renderizar cosas en la página o redirigir
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Lineas 5-6, funciones predefinidas de login de la mano de Django

import time
from transformers import pipeline

from .forms import LoginUsuariosForm, RegistroUsuariosForm, publicacionesForm, perfilusuarioform, apelarForm
from .utils.auth import anonymous_required
from .models import Publicacion, Comentario, Topicos, perfilusuario, Usuarios

moderador = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-offensive")
traductor = pipeline("translation", model="Helsinki-NLP/opus-mt-es-en")

def revisarTexto(contenido):
    traducir = traductor(contenido)[0]['translation_text']
    resultado = moderador(traducir)
    print(f'Texto original: {contenido} \nTexto traducido: {traducir} \n')
    print(resultado)
    return resultado


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
                pagSiguinte = request.POST.get('next') or request.GET.get('next') or '/'
                return redirect(pagSiguinte)
            formulario.add_error(None, 'Usuario o contraseña inválidos')
    else:
        formulario = LoginUsuariosForm()
    variables = {
        'form': formulario,
        'next': request.GET.get('next', '')
    }
    return render(request, 'iniciarSesion.html', variables)


def logoutUsuario(request: HttpRequest):
    logout(request) # Limpia la sesión
    return redirect('login')


def index(request):
    userID = request.user
    loggeado = userID.is_authenticated
    variables = {
        'usuario': userID,
        'loggeado': loggeado,
        'rol': userID.rol if loggeado else None
    }
    return render(request, 'index.html', variables)


def toAdmin(request: HttpRequest):
    if request.user.rol == 'adm':
        logout(request)
        return redirect(reverse('admin:index'))
    return redirect('BadApple')


def contrato(request):
    return render(request, 'contrato.html')


@login_required(login_url='login')
def foroView(request):
    userID = request.user
    publicacionesForo = Publicacion.objects.all().filter(ofensivo=False)
    publicacionesOrden = publicacionesForo.order_by('-fechaCreacion')
    variables = {
        'usuario': userID,
        'rol': userID.rol,
        'foro': publicacionesOrden,
        'page': 'foro',
        'minForo': len(publicacionesOrden) >= 25 # Lo pongo para saber si hay más de 25 publicaciones en el foro
    }
    return render(request, 'foro.html', variables)


@login_required(login_url='login')
def crearPubView(request):
    userID = request.user

    if request.method == 'POST': # Siempre va
        formulario = publicacionesForm(request.POST) # Se define el formulario
        if formulario.is_valid():
            titulo = formulario.cleaned_data['titulo'] # Extrae el titulo
            cuerpo = formulario.cleaned_data['cuerpo'] # Extrae el cuerpo
            revision = f"{titulo}. {cuerpo}" # Une titulo y cuerpo
            mod_resultado = revisarTexto(revision) # Entrega al modelo IA el titulo y cuerpo
            mod_flag = mod_resultado[0]['label'] # Obtiene el resultado
            mod_score = mod_resultado[0]['score'] # Obtiene el puntaje
            publicacion = formulario.save(commit=False) # Guarda el formulario sin aplicar a la B.D.
            publicacion.autor = request.user # Añade autor manualmente
            if mod_flag == 'offensive': # Si el post resulta ofensivo.......
                publicacion.ofensivo = True # Setea ofensivo manualmente
                publicacion.save() # Guarda a la B.D.
                archivo = open("logModeracion.txt", "a") # Abre el LOG de moderación en modo "append"
                archivo.write(f"{str(publicacion.idPublicacion)}, {str(request.user.nombre)}, {str(mod_score)}, \n") # Añade al LOG el id de publicación, autor y puntaje
                archivo.close() # Cierra el LOG de moderación
                return redirect('publicacion', publicacion.idPublicacion)
            publicacion.save() # Guarda a la B.D. si no resulta ofensivo
            return redirect('foro')
    else:
        formulario = publicacionesForm()
    variables = {
        'form': formulario,
        'usuario': userID,
        'rol': userID.rol,
    }
    return render(request, 'crearPub.html', variables)


def postView(request, postID):
    publicacion = get_object_or_404(Publicacion, idPublicacion=postID)
    if not publicacion.ofensivo: # Si el post no esta flageado, lo mandará a la visualización normal
        variables = {
            'publicacion': publicacion,
            'usuario': request.user,
        }
        return render(request, 'publicacion.html', variables)

    elif publicacion.ofensivo and not publicacion.enRevision and publicacion.autor == request.user:
        if request.method == 'POST':
            form = apelarForm(request.POST)
            if form.is_valid():
                publicacion.enRevision = True
                publicacion.motivoRevision = form.cleaned_data['motivo']
                publicacion.save()
                # notify site admins about the appeal
                subject = f"Apelación de publicación #{publicacion.idPublicacion}"
                message = (
                    f"El usuario {getattr(request.user, 'nombre', request.user)} "
                    f"ha apelado la eliminación de la publicación {publicacion.idPublicacion}.\n\n"
                    f"Motivo de apelación:\n{publicacion.motivoRevision}\n\n"
                    f"URL: {request.build_absolute_uri(reverse('publicacion', args=[publicacion.idPublicacion]))}"
                )
                recipients = [email for _, email in getattr(settings, 'ADMINS', [])]
                if not recipients:
                    default_from = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
                    if default_from:
                        recipients = [default_from]
                if recipients:
                    try:
                        send_mail(subject, message, getattr(settings, 'DEFAULT_FROM_EMAIL', None), recipients, fail_silently=True)
                    except Exception as e:
                        print(f"Error sending appeal email: {e}")
                return redirect('foro')
        else:
            form = apelarForm()
        variables = {
            'publicacion': publicacion,
            'usuario': request.user,
            'form': form,
        }
        return render(request, 'apelar.html', variables)

    elif publicacion.ofensivo and not publicacion.enRevision and publicacion.autor != request.user:
        raise Http404('El post viola las normas de la comunidad y se encuentra eliminado')

    else:
        raise Http404('Post en revisión')




def badApple(request):
    '''when te das cuenta de que puedes programar
    lo que sea:'''
    return render(request, 'ba.html')


@login_required(login_url='login')
def edicion_perfil(request, userPK):
    userID= request.user
    perfilActual = get_object_or_404(perfilusuario, user__pk=userPK)
    esUsuarioActual = perfilActual.user == userID
    if request.method == 'POST' and esUsuarioActual:
        form = perfilusuarioform(request.POST, instance=perfilActual)
        if form.is_valid():
            form.save()
            return redirect('perfil', str(userPK))
    else:
        form = perfilusuarioform(instance=perfilActual)
    variables = {
        'form': form,
        'usuario': userID,
        'nombreUsr': perfilActual.user.nombre,
        'aliasUsr': perfilActual.user.aliasUsuario,
        'perfilUsr': perfilActual,
        'esUsuarioActual': esUsuarioActual,
    }
    return render(request, 'perfilUsuario.html', variables)


def preguntasfrecuentes(request):
    return render(request,"preguntasfrecente.html")


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
