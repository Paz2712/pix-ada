from django.db import models
from django.contrib.auth.hashers import make_password, check_password # No tocar, encripta las contraseñas
from django.core.exceptions import ValidationError

'''
Aquí se crea el modelo de la base de datos
No se incluye un ID, cada tabla de base de
datos de Django crea esa variable de manera automática

Para una característica de texto como nombre de usuario, comentario, etc
usar models.charField
'''

class Usuarios(models.Model): # El usuario
    nombre = models.CharField(max_length=20, unique=True) # Cada nombre de usuario será de 20 caracteres y único
    aliasUsuario = models.CharField(max_length=15) # Cada alias será de 15 caracteres y no único
    correo = models.EmailField(unique=True) # Correo, EmailField, puedes entender por qué con algo de cabeza
    contrasena = models.CharField(max_length=128) # Una clave encriptada termina con alrededor de 128 caracteres
    rolesDisponibles = [ # Diferentes roles predefinidos en tuplas
        ("adm", "Administrador"),
        ("mod", "Moderador"),
        ("usr", "Usuario"),
    ]
    rol = models.CharField(max_length=15, choices=rolesDisponibles, default="usr")

    # ---------- PREFERENCIAS ---------- #
    modoOscuro = models.BooleanField(default=False) # Modo oscuro, False por defecto
    yanMode = models.BooleanField(default=False) # Ya saben
    altoContraste = models.BooleanField(default=False) # Modo de alto contraste, para personas de visibilidad limitada

    def encriptar_contrasena(self, conInsegura): # Encripta las contraseñas
        self.contrasena = make_password(conInsegura)
    def comprobar_contrasena(self, contrasenaUsada): # Sirve a la hora de hacer el login, comprueba que la contraseña sea la misma
        return check_password(contrasenaUsada, self.contrasena)
    def save(self, *args, **kwargs):
        dominiosPermitidos = [ # Aquí rellenen con los dominios permitidos de la u
            'usm.cl',
            'inf.utfsm.cl'
        ]
        correosPermitidos = [ # Aquí rellenen con sus correos personales
            'altamiranoaxius@proton.me',
        ]
        # El if de abajo comprueba que el correo termine en "@usm.cl" o que sea uno admitido, en caso del correo personal de nosotros (admins)
        if self.correo not in correosPermitidos and not any(self.correo.endswith('@'+dominio) for dominio in dominiosPermitidos):
            raise ValidationError("Correo no permitido, recuerda usar tu correo institucional")
        
        # El if de abajo encripta las contraseñas apenas se hagan
        if not self.contrasena.startswith('pbkdf2_'):
            self.encriptar_contrasena(self.contrasena)
        
        # Los alias empezarán con un @
        if not self.aliasUsuario.startswith("@"):
            self.aliasUsuario = "@"+self.aliasUsuario
        super().save(*args, **kwargs) # Guarda los cambios antes de crear la entrada en la base de datos

    def __str__(self):
        return self.nombre
    

class Topicos(models.Model):
    nombre = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.nombre
    

class Publicacion(models.Model):
    idPublicacion = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=50)
    autor = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True)
    # El autor es una Foreign Key (uno a muchos) porque un usuario puede ser autor de
    # multiples publicaciones. Si se elimina el autor, pasa a tomar el valor "None"
    fechaCreacion = models.DateField(auto_now_add=True, null=True, blank=True)
    cuerpo = models.TextField()
    topico = models.ManyToManyField(Topicos, blank=True)
    esAnonimo = models.BooleanField(default=False)

    def __str__(self):
        return str(self.idPublicacion) + " " + self.titulo

