from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import PrestarForm, SolicitarForm
from .models import Prestamo, Notificacion
from peticiones.models import Peticion
from usuarios.models import Usuario
from ofertas.models import Oferta

class PrestarFormView(FormView):
    form_class = PrestarForm
    success_url = reverse_lazy('peticiones')

    def form_valid(self, form):
        peticion = Peticion.objects.get(id=form.cleaned_data['peticion_id'])
        usuario = Usuario.objects.get(user = self.request.user)
        nombre_prestador = usuario.user.username
        objeto = peticion.titulo
        nombre_recibidor = peticion.usuario.user.username
        Prestamo.objects.create(prestador=nombre_prestador, objeto=objeto, recibidor=nombre_recibidor)

        notificacion = Notificacion.objects.create(usuario=peticion.usuario, contraparte=nombre_prestador, objeto=objeto, telefono=usuario.telefono)
        return super().form_valid(form)

class SolicitarFormView(FormView):
    form_class = SolicitarForm
    success_url = reverse_lazy('ofertas')

    def form_valid(self, form):
        oferta = Oferta.objects.get(id=form.cleaned_data['oferta_id'])
        usuario = Usuario.objects.get(user=self.request.user)
        Notificacion.objects.create(usuario=oferta.usuario, contraparte=usuario.user.username, objeto=oferta.titulo)
        return super().form_valid(form)

class NotificacionListView(ListView):
    template_name = 'prestamos/notificaciones.html'
    context_object_name = 'notificaciones'

    def get_queryset(self):
        usuario = Usuario.objects.get(user=self.request.user)
        notificaciones = Notificacion.objects.filter(usuario=usuario)
        return notificaciones
    
