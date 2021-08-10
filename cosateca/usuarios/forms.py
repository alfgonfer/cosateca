from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_integer
from .models import Usuario


class RegistroForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de usuario'}),max_length=30)
    email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Contraseña'}),min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Repite la contraseña'}),min_length=8)
    telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Teléfono'}), min_length=9, max_length=9)

    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        telefono = self.cleaned_data.get('telefono')
        if password1 != password2:
            msg = 'Las contraseñas deben de coincidir.'
            self._errors['password1'] = self.error_class([msg])
            del self.cleaned_data['password1']
            del self.cleaned_data['password2']
        if User.objects.filter(username=username).exists():
            msg = 'El nombre de usuario no está disponible.'
            self._errors['username'] = self.error_class([msg])
            del self.cleaned_data['username']
        if User.objects.filter(email=email).exists():
            msg = 'El e-mail introducido ya se encuentra registrado.'
            self._errors['email'] = self.error_class([msg])
            del self.cleaned_data['email']
        if telefono.isnumeric() == False:
            msg = 'Introduce un número de teléfono correcto'
            self._errors['telefono'] = self.error_class([msg])
            del self.cleaned_data['telefono']
        if Usuario.objects.filter(telefono=telefono).exists():
            msg = 'El teléfono introducido ya se encuentra registrado.'
            self._errors['telefono'] = self.error_class([msg])
            del self.cleaned_data['telefono']           
        return self.cleaned_data