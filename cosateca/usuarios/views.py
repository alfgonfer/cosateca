from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView as auth_view
from django.contrib.auth.models import User
from .forms import RegistroForm
from django.urls import reverse_lazy
from .models import Usuario

class InicioView(TemplateView):
    template_name = 'inicio/inicio.html'

class LoginView(auth_view):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

class RegistroView(FormView):
    template_name='usuarios/registro.html'
    form_class = RegistroForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        email = form.cleaned_data['email']
        telefono = form.cleaned_data['telefono']
        if password1 == password2:
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                usuario = Usuario(user=user, telefono=telefono)
                usuario.save()
                return super().form_valid(form)
            else:
                context = self.get_context_data(form=form)
                return self.render_to_response(context)
        else:
            context = self.get_context_data(form=form)
            return self.render_to_response(context)
