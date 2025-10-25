from django.db import models
from django.contrib.auth.hashers import make_password, check_password, identify_hasher # No tocar, encripta las contraseñas
from django.core.exceptions import ValidationError # Un error bien bonito que ocurre si no hacen lo que pedimos (lo uso para el correo)
from django.core.validators import RegexValidator # Es un validador del que me enamoré, me hace la vida más facil


'''
Aquí se crea el modelo de la base de datos
No se incluye un ID, cada tabla de base de
datos de Django crea esa variable de manera automática

Para un atributo de texto como nombre de usuario, comentario, etc
usar models.charField y especifiquen un máximo de largo con (max_length=<el número que quieran como pow(10, 99)>)
Para un atributo que requiera de SI o NO,
usar models.BooleanField y especifiquen un valor por defecto con (default=<True o False>)
'''
## El usuario
class Usuarios(models.Model):
    # Isidora, Pablo, Santi, probablemente Benja y Maca, este es el resultado de 3 noches sin dormir e investigación
    # intensa. Intenté documentar y explicar todo lo que hice, por qué, entre muchas otras cosas con tal de
    # que puedan editarlo a su gusto. Disfruten, o lloren ante el orden o desorden de mi código, solo quiero dormir

    # ----- Identificadores ----- #
    nombre = models.CharField(
        max_length=20, 
        unique=True,
        # Nombre de usuario, debe ser único, se usará para el login, o al menos eso entendí de ustedes, yo solo escribo código (Axius :D)
    )
    aliasUsuario = models.CharField(
        max_length=15,
        unique=True,
        # Alias de usuario, busco que empiece con @ o # para diferenciarlo del nombre, si no quieren que sea unico, borren la linea 23
    )
    correo = models.EmailField(
        unique=True,
        # Aquí irá el correo, por supuesto, único. Tiene que ser institucional o en whitelist.
    )
    contrasena = models.CharField(
        max_length=128,
        # Contraseña, la longitud es estupidamente larga porque así es encriptada
    )

    # ----- Roles ----- #
    rolesDisponibles = [ # Diferentes roles predefinidos en tuplas
        ("adm", "Administrador"),
        ("mod", "Moderador"),
        ("usr", "Usuario"),
    ]
    rol = models.CharField(
        max_length=15, 
        choices=rolesDisponibles, 
        default="usr",
        # El rol que tendrá el (por defecto) usuario, manualmente en la pestaña de admins podemos cambiarlo
    )

    # ----- Necesario para usar funciones login de Django ----- #

    # Me rindo, usaré las funciones de Django para hacer el login
    # Requiere estos dos campos, por si luego quiero integrarlo con la ventana de admin (solo nosotros lo veremos, no el usuario promedio)
    # Lo robé del tutorial de Mozilla
    # Quiero un café

    is_active = models.BooleanField(default=True) # Comprueba si el usuario está activo, lo desactivamos en lugar de eliminarlo, para evitar conflictos en la DB
    is_staff = models.BooleanField(default=False) # Comprueba si es uno de nosotros (nunca lo serán xdd)
    last_login = models.DateTimeField(null=True, blank=True)

    
    @property # @property define propiedades que SI O SI debe tener la DB de los usuarios para que sea Django-Friendly
    def is_authenticated(self):
        # Para @Login_required y request.user.is_authenticated
        return True
    @property
    def is_anonymous(self): # Ignorar, Django me obliga a ponerlo para el login. Las publicaciones serán anonimas (no usuarios)
        return False


    # ----- Preferencias de usuario ----- #
    modoOscuro = models.BooleanField(default=False) # Modo oscuro, False por defecto
    yanMode = models.BooleanField(default=False) # Ya saben
    altoContraste = models.BooleanField(default=False) # Modo de alto contraste, para personas de visibilidad limitada

    # ----- Validadores / Helpers ----- #
    validadorAlias = RegexValidator(
        regex=r'^@?[A-Za-z0-9_]{3,14}$',
        # Se que no se entiende una chota, así que explico:
        # "^" marca el inicio del string
        # "@?" indica que puede haber un @ opcional al inicio (termino añadiendolo a la fuerza)
        # "[A-Za-z0-9_]" dice el rango de cosas que pueden haber, de la "a" a la "z" en minusculas y mayusculas, números y guiónes bajos
        # "{3,14}" la cantidad de caracteres mínima y máxima, en este caso de entre 3 y 14, sin contar el @, así es añadido y cumple el límite de 15
        # "$" marca el final del string
        # Por eso me encanta, automatiza el desastre que tengo, aunque se vea desastroso de configurar
    )
    def encriptar_contrasena(self, conInsegura: str):
        # Encripta las contraseñas, conInsegura: str se asegura de que conInsegura sea SOLAMENTE un string
        self.contrasena = make_password(conInsegura)
    def comprobar_contrasena(self, contrasenaUsada: str):
        # Función para el login, comprueba que una contraseña normal sea igual que una encriptada
        return check_password(contrasenaUsada, self.contrasena)
    
    def clean(self):
        # La función clean sirve para hacer validaciones antes de que se guarden los cambios
        # Si añadimos mas excepciones, añadanlas aquí, y elijan que error tira
        dominiosPermitidos = [
            'usm.cl',
            'inf.utfsm.cl',
            # Whitelist de dominios, si saben de otros que use la u, bienvenidos sean
        ]
        correosPermitidos = [
            'altamiranoaxius@proton.me',
            'lopezvegamaca@gmail.com',
            'joaco345vz@gmail.com', # El joaco se ofreció de mod, anda ahí por si acaso su correo
            # Whitelist de correos, pongan sus correos personales aquí para que puedan usarlos normalmente
        ]
        if self.correo not in correosPermitidos and not any(self.correo.lower().endswith('@'+dominio.lower()) for dominio in dominiosPermitidos):
            # Tira error si el correo no está en la whitelist o si no tiene el dominio correcto
            raise ValidationError("You lost the game dude") # xddd
        if self.aliasUsuario and not self.aliasUsuario.startswith('@'):
            # Comprueba que:
            # 1. Exista un alias (con que en aliasUsuario haya un string debería tirar True, si no hay nada tira False)
            # 2. El alias NO empiece con un @
            self.aliasUsuario = '@'+self.aliasUsuario
        self.validadorAlias(self.aliasUsuario)
        # Esta cosa valida el alias con regex, si no cumple lo solicitado, tira un muy bonito error
        # No volveré a explicar que hace regex, ya les expliqué antes y cómo configurarlo
        
    def save(self, *args, **kwargs):
        # La función save guarda la clase
        # Aquí añadimos que cambios extras queremos que se guarden también
        # *args y **kwargs utiliza una tupla y un diccionario con todo lo que Django pase por save para usarlo
        self.full_clean() # Ejecuta todas las validaciones de la función clean

        # Ahora vamos a asegurarnos que la contraseña esté encriptada con try
        # try nos permite ejecutar una función y hacer que ocurra algo si ocurre algo específico
        try:
            identify_hasher(self.contrasena)
            # Tira ValueError si la contraseña no está encriptada
        except ValueError:
            # Si esto ocurre, se encripta la contraseña
            self.encriptar_contrasena(self.contrasena)
        super().save(*args, **kwargs) # Guarda los cambios antes de crear la entrada en la base de datos

    def __str__(self):
        return self.nombre
    # Util para debug, cómo, no se aún, pero una discusión de stackoverflow lo recomendó
    

class Topicos(models.Model):
    nombre = models.CharField(
        max_length=15, 
        unique=True,
        # Nombre del tópico, de 15 caracteres de largo y único (no quiero ver más de un Silkpost)
    )

    def __str__(self): 
        return self.nombre
    # Sigo sin saber como se usa esto, nadie quiere decirme cómo
    

class Publicacion(models.Model):
    idPublicacion = models.BigAutoField(
        primary_key=True,
        # Nuestra primary key, todo el resto tiene de primary key un id por defecto, aquí especifico una
        # para que se vea en la página de admin
    )
    titulo = models.CharField(
        max_length=50,
        # El título de la publicación, de 50 caracteres de largo
    )
    autor = models.ForeignKey(
        Usuarios, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        # Autor, es una foreign key (muchos-a-uno) ya que muchas publicaciones pueden ser de un usuario
        # Al eliminarse el usuario vinculado al autor, este queda en None, sin eliminar la publicación
    )
    fechaCreacion = models.DateTimeField(
        auto_created=True, 
        auto_now_add=True,
        null=True, 
        blank=True,
        # La fecha de creación se crea automáticamente al crear la publicación creadamente creada xdddd
        # Mátame, ese chiste fué malísimo, peor que los de la maca  
    )
    cuerpo = models.TextField(
        max_length=500
        # El contenido, está en duda aún el tamaño máximo, no se si limitarlo a 500 o ponerle un número ridiculamente alto
        # O ridiculamente bajo, por las risas
    )
    topico = models.ManyToManyField(
        Topicos, 
        blank=True
        # El tópico, tiene una relación muchos-a-muchos (multiples tópicos pueden ser de multiples publicaciones)
        # Puede estar en blanco
    )
    esAnonimo = models.BooleanField(
        default=False
        # Después veo esta variable para saber si mostrar o no el alias del usuario al crear una publicación
        # Por defecto no es anonima
    )
    def __str__(self):
        return str(self.idPublicacion) + " " + self.titulo
    # Ayuda...

class Comentario(models.Model):
    autor = models.ForeignKey(
        Usuarios,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        # El autor del comentario
    )
    publicacion = models.ForeignKey(
        Publicacion,
        on_delete=models.CASCADE,
        # La publicación del comentario
        # models.CASCADE indica que si la publicación se elimina, el comentario se va con ella
    )
    cuerpo = models.CharField(
        max_length=200,
        # El contenido del comentario, está en duda su tamaño
    )
