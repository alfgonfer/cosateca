from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import PrestarForm, SolicitarForm, PrestarNotificacionForm
from .models import Prestamo, Notificacion
from peticiones.models import Peticion
from usuarios.models import Usuario
from ofertas.models import Oferta
from datetime import datetime, timezone

class PrestarFormView(FormView):
    form_class = PrestarForm
    success_url = reverse_lazy('peticiones')

    def form_valid(self, form):
        peticion = Peticion.objects.get(id=form.cleaned_data['peticion_id'])
        usuario = Usuario.objects.get(user = self.request.user)
        nombre_prestador = usuario.user.username
        objeto = peticion.titulo
        nombre_recibidor = peticion.usuario.user.username
        prestamo, creado = Prestamo.objects.get_or_create(prestador=nombre_prestador, objeto=objeto, recibidor=nombre_recibidor)
        if not creado:
            if (datetime.now(timezone.utc) - prestamo.fecha_prestamo).days > 7:
                Prestamo.objects.get_or_create(prestador=nombre_prestador, objeto=objeto, recibidor=nombre_recibidor)

        notificacion, creado = Notificacion.objects.get_or_create(usuario=peticion.usuario, contraparte=nombre_prestador, objeto=objeto, telefono=usuario.telefono)
        if not creado:
            if (datetime.now(timezone.utc) - notificacion.fecha_notificacion).days > 7:
                Notificacion.objects.create(usuario=peticion.usuario, contraparte=nombre_prestador, objeto=objeto, telefono=usuario.telefono)
        return super().form_valid(form)

class SolicitarFormView(FormView):
    form_class = SolicitarForm
    success_url = reverse_lazy('ofertas')

    def form_valid(self, form):
        oferta = Oferta.objects.get(id=form.cleaned_data['oferta_id'])
        usuario = Usuario.objects.get(user=self.request.user)
        notificacion, creado = Notificacion.objects.get_or_create(usuario=oferta.usuario, contraparte=usuario.user.username, objeto=oferta.titulo, oferta_id=oferta.id)
        if not creado:
            if (datetime.now(timezone.utc) - notificacion.fecha_notificacion).days > 7:
                Notificacion.objects.create(usuario=oferta.usuario, contraparte=usuario.user.username, objeto=oferta.titulo, oferta_id=oferta.id)
        return super().form_valid(form)

class NotificacionListView(ListView):
    template_name = 'prestamos/notificaciones.html'
    context_object_name = 'notificaciones'

    def get_queryset(self):
        usuario = Usuario.objects.get(user=self.request.user)
        notificaciones = Notificacion.objects.filter(usuario=usuario)
        return notificaciones
    
class PrestarNotificacionFormView(FormView):
    form_class = PrestarNotificacionForm
    success_url = reverse_lazy('notificaciones')

    def form_valid(self, form):
        oferta = Oferta.objects.get(id=form.cleaned_data['oferta_id'])
        objeto = oferta.titulo
        usuario = Usuario.objects.get(user=self.request.user)
        nombre_prestador = usuario.user.username
        user = User.objects.get(username=form.cleaned_data['nombre_recibidor'])
        recibidor = Usuario.objects.get(user=user)
        prestamo, creado = Prestamo.objects.get_or_create(prestador=nombre_prestador, objeto=objeto, recibidor=recibidor.user.username)
        if not creado:
            if (datetime.now(timezone.utc) - prestamo.fecha_prestamo).days > 7:
                Prestamo.objects.create(prestador=nombre_prestador, objeto=objeto, recibidor=recibidor.user.username)

        notificacion, creado = Notificacion.objects.get_or_create(usuario=recibidor, contraparte=nombre_prestador, objeto=objeto, telefono=usuario.telefono)
        if not creado:
            if (datetime.now(timezone.utc) - notificacion.fecha_notificacion).days > 7:
                Notificacion.objects.create(usuario=recibidor, contraparte=nombre_prestador, objeto=objeto, telefono=usuario.telefono)
        return super().form_valid(form)

class PrestamosListView(ListView):
    template_name = 'prestamos/prestamos.html'
    context_object_name = 'prestamos'
    model = Prestamo
