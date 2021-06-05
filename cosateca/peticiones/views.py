from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Peticion
from .forms import PeticionForm, PeticionDeleteForm
from usuarios.models import Usuario

class PeticionListView(ListView):
    template_name='peticiones/lista_peticiones.html'
    model = Peticion
    context_object_name = 'peticiones'

@method_decorator(login_required, name='dispatch')
class PeticionCreateView(FormView):
    form_class = PeticionForm
    template_name = 'peticiones/crear_peticion.html'
    success_url = reverse_lazy('peticiones')

    def form_valid(self, form):
        usuario = Usuario.objects.get(user=self.request.user)
        titulo = form.cleaned_data['titulo']
        descripcion = form.cleaned_data['descripcion']
        Peticion.objects.create(usuario=usuario, titulo=titulo, descripcion=descripcion)
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class PeticionUpdateView(FormView):
    form_class = PeticionForm
    template_name = 'peticiones/editar_peticion.html'
    success_url = reverse_lazy('peticiones')

    def get(self, request, *args, **kwargs):
        try:
            peticion_id = kwargs['peticion_id']
            if not Peticion.objects.filter(id=peticion_id).exists():
                raise Exception('La oferta no existe')
            return super(PeticionUpdateView, self).get(request, kwargs['peticion_id'])
        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(request, 'base/error.html', context)

    def form_valid(self, form):
        self.peticion_id = self.kwargs['peticion_id']
        usuario = Usuario.objects.get(user=self.request.user)
        peticion = Peticion.objects.get(id=self.kwargs['peticion_id'])
        titulo = form.cleaned_data['titulo']
        descripcion = form.cleaned_data['descripcion']
        peticion.titulo = titulo
        peticion.descripcion = descripcion
        peticion.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        peticion_id = self.kwargs['peticion_id']
        context = super().get_context_data(**kwargs)
        peticion = Peticion.objects.get(id=peticion_id)
        context['peticion'] = peticion
        return context

@method_decorator(login_required, name='dispatch')
class MisPeticionesView(TemplateView):
    template_name = 'peticiones/mis_peticiones.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = Usuario.objects.get(user=self.request.user)
        peticiones = Peticion.objects.filter(usuario=usuario)
        context['peticiones'] = peticiones
        return context

@method_decorator(login_required, name='dispatch')
class PeticionDeleteView(FormView):
    form_class = PeticionDeleteForm
    success_url = reverse_lazy('mis_peticiones')
    
    def form_valid(self, form):
    
        peticion_id = form.cleaned_data['peticion_id']
        if Peticion.objects.filter(id=peticion_id).exists():
            peticion = Peticion.objects.get(id=peticion_id)
            if peticion.usuario == Usuario.objects.get(user=self.request.user):
                peticion.delete()
                return super().form_valid(form)
        else:
            raise Exception('La petición no existe o no eres el dueño')
