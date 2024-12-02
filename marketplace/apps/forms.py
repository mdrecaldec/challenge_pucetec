from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Producto

class RegisterForm(UserCreationForm):
    cedula = forms.CharField(max_length=10, required=True, label="Cédula")
    nombres_apellidos = forms.CharField(max_length=150, required=True, label="Nombres y Apellidos")
    email = forms.EmailField(required=True, label="Correo Electrónico")
    
    class Meta:
        model = User
        fields = ['username', 'cedula', 'nombres_apellidos', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name, user.last_name = self.cleaned_data['nombres_apellidos'].split(" ", 1)  # Divide nombres y apellidos
        user.profile.cedula = self.cleaned_data['cedula']  # Supone que tienes un modelo `Profile` relacionado
        if commit:
            user.save()
        return user


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'categoria', 'accion', 'precio', 'imagen']