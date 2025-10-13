from django import forms
from django.contrib.auth.forms import AuthenticationForm

# Formularios :D

class FormularioLogin(AuthenticationForm):
    nombre = forms.CharField(max_length=20, label="Nombre de Usuario (no alias)")
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
