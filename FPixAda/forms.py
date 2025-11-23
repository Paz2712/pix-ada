from django import forms
from django.core.exceptions import ValidationError
from .models import Usuarios, Publicacion, Topicos, perfilusuario, Comentario

# Formularios :D
# Cuando use clean o similar, es para hacer validaciones o normalizaciones de algo ANTES de guardar
# Como añadir @ en los aliases o validar los caracteres en este
class RegistroUsuariosForm(forms.ModelForm):
    contrasena1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(),
        # Contraseña 1, widget=forms.PasswordInput se encarga de esconder el input del usuario de la pantalla
    )
    contrasena2 = forms.CharField(
        label='Repita la contraseña',
        widget=forms.PasswordInput(),
        # Donde el usuario debe confirmar su contraseña
    )

    class Meta: # Metadatos, los campos que se mostrarán y se usarán de la database
        model = Usuarios
        fields = ('nombre', 'aliasUsuario', 'correo')
    
    def clean(self):# validación de la contraseña antes de guardarla en la base de datos
        cleaned = super().clean()
        p1 = cleaned.get('contrasena1') # No es Persona 1
        p2 = cleaned.get('contrasena2') # No es Persona 2
        if p1 and p2 and p1 != p2:
            self.add_error('contrasena2', 'Las contraseñas deben ser iguales')
        return cleaned
    def save(self, commit=True):
        user = super().save(commit=False)
        user.contrasena = self.cleaned_data['contrasena1'] # Guarda la contraseña donde debe, en Usuarios.contrasena
        if commit:
            user.save()
        return user
    
class LoginUsuariosForm(forms.Form): # no cambia la base de datos
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(),
    )

class publicacionesForm(forms.ModelForm): # si agrega o modifica la base de datos  
    class Meta:
        model = Publicacion
        fields = ("titulo", "cuerpo", "topico", "esAnonimo" )
        widgets = {
            'titulo': forms.TextInput(), # Texto corto
            'cuerpo': forms.Textarea(), # Texto largo
            'topico': forms.RadioSelect(attrs={'required': 'true'}) , # Selección múltiple
            'esAnonimo': forms.CheckboxInput(), # Si o no
        }
    
class perfilusuarioform(forms.ModelForm): #permite que el usuario elija un archivo de su pc y la suba a su perfil
    class Meta:
        model = perfilusuario # el nombre de la clase creada en el models.py que tiene que ver con esto 
        #fields = ("alias", "descripcion", "foto" ) #las cosas que tienen que ir :p
        fields= ('description',)

class apelarForm(forms.Form):
    motivo = forms.CharField(
        widget=forms.Textarea()
    )