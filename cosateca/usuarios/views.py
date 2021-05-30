from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView as auth_view

class InicioView(TemplateView):
    template_name = 'inicio/inicio.html'

class LoginView(auth_view):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True
