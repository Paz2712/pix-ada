from django import forms
from django.core.exceptions import ValidationError
from .models import Usuarios

# Formularios :D
# Cuando use clean o similar, es para hacer validaciones o normalizaciones de algo ANTES de guardar
# Como añadir @ en los aliases o validar los caracteres en este
class RegistroUsuariosForm(forms.ModelForm):
    contrasena1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        min_length=8
        # Contraseña, de mínimo 8 caracteres. Lo que pone en widget esconde el texto en el navegador
    )
    contrasena2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
        # Se repite la contraseña, también se esconde el texto de este campo
    )

    class Meta:
        # Define el modelo y campos de este que se usarán, no se incluye contraseña porque ese campo se definió arriba
        model = Usuarios
        fields = [
            "nombre",
            "aliasUsuario",
            "correo",
        ]
    
    def clean_nombre(self):
        # Normalizar y valida el nombre, eliminando espacios innecesarios con strip()
        return self.cleaned_data["nombre"].strip()
    def clean_aliasUsuario(self):
        # Normaliza el alias, eliminando espacios innecesarios
        # El modelo lo validará, añadiendo el @ si no lo había y usando mi amado Regex
        return self.cleaned_data["aliasUsuario"].strip()
    def clean_correo(self):
        # Por si acaso, se normaliza el correo, por si el imbécil pone espacios
        # El modelo comprobará que sea de la universidad sin minas
        return self.cleaned_data["correo"].strip()
    def clean(self):
        cleaned = super().clean()
        con1 = cleaned.get("contrasena1")
        con2 = cleaned.get("contrasena2")
        if con1 and con2 and con1 != con2:
            raise ValidationError("Las contraseñas no coinciden")
        return cleaned
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.encriptar_contrasena(self.cleaned_data["contrasena1"])
        if commit:
            usuario.save()
        return usuario


class LoginUsuariosForm(forms.Form):
    # Formulario de login, usará el nombre de usuario, no alias ni correo, para la autenticación
    # (14-10-25) En teoría debería funcionar
    nombre = forms.CharField(
        label="Usuario",
        # Aquí va el nombre de usuario (no alias ni correo, no se les olvide)
    )
    contrasena = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
        # Campo de concentración, digo contraseña. Se esconde al usuario
    )

    def clean(self):
        cleaned = super().clean()
        nombre = cleaned.get("nombre")
        contrasena = cleaned.get("contrasena")
        if nombre:
            # El nombre escrito es normalizado con strip()
            nombreInput = cleaned.get["nombre"].strip()
        if nombre and contrasena:
            try:
                # Intenta buscar un usuario que exista con ese nombre
                usuario = Usuarios.objects.get(nombre=nombreInput)
            except Usuarios.DoesNotExist:
                # Si no existe, levanta un error de validación
                raise ValidationError("Credenciales inválidas: El usuario no existe")
            if not usuario.comprobar_contrasena(contrasena):
                # Si el usuario existe (por eso se usa usuario.comprobar_contrasena) PERO la contraseña no coincide
                # Levanta otro error
                raise ValidationError("Credenciales inválidas: Contraseña incorrecta")
            self.usuario = usuario
        return cleaned
