from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse_lazy
from .models import Oferta
from .forms import OfertaForm, OfertaDeleteForm
from usuarios.models import Usuario

class OfertaListView(ListView):
    template_name='ofertas/lista_ofertas.html'
    model = Oferta
    context_object_name = 'ofertas'

class OfertaFormView(FormView):
    form_class = OfertaForm
    template_name = 'ofertas/crear_oferta.html'
    success_url = reverse_lazy('ofertas')

    def form_valid(self, form):
        usuario = Usuario.objects.get(user=self.request.user)
        imagen = form.cleaned_data['imagen']
        titulo = form.cleaned_data['titulo']
        descripcion = form.cleaned_data['descripcion']
        Oferta.objects.create(usuario=usuario, titulo=titulo, descripcion=descripcion, imagen=imagen)
        return super().form_valid(form)

class OfertaShowView(TemplateView):
    template_name = 'ofertas/mostrar_oferta.html'

    def get(self, request, *args, **kwargs):
        try:
            oferta_id = kwargs['oferta_id']
            if not Oferta.objects.filter(id=oferta_id).exists():
                raise Exception('La oferta no existe')
            return super(OfertaShowView, self).get(request, kwargs['oferta_id'])
        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(request, 'base/error.html', context)

    def get_context_data(self, **kwargs):
        oferta_id = self.kwargs['oferta_id']
        context = super().get_context_data(**kwargs)
        oferta = Oferta.objects.get(id=oferta_id)
        context['oferta'] = oferta
        return context

class OfertaUpdateView(FormView):
    form_class = OfertaForm
    template_name = 'ofertas/editar_oferta.html'
    success_url = reverse_lazy('ofertas')
    oferta_id = None

    def get(self, request, *args, **kwargs):
        try:
            oferta_id = kwargs['oferta_id']
            if not Oferta.objects.filter(id=oferta_id).exists():
                raise Exception('La oferta no existe')
            return super(OfertaUpdateView, self).get(request, kwargs['oferta_id'])
        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(request, 'base/error.html', context)

    def form_valid(self, form):
        self.oferta_id = self.kwargs['oferta_id']
        usuario = Usuario.objects.get(user=self.request.user)
        oferta = Oferta.objects.get(id=self.kwargs['oferta_id'])
        imagen = form.cleaned_data['imagen']
        titulo = form.cleaned_data['titulo']
        descripcion = form.cleaned_data['descripcion']
        oferta.imagen = imagen
        oferta.titulo = titulo
        oferta.descripcion = descripcion
        oferta.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        oferta_id = self.kwargs['oferta_id']
        context = super().get_context_data(**kwargs)
        oferta = Oferta.objects.get(id=oferta_id)
        context['oferta'] = oferta
        return context

    def get_success_url(self):
        return reverse('mostrar_oferta', kwargs={'oferta_id':self.oferta_id})

class MisOfertasView(TemplateView):
    template_name = 'ofertas/mis_ofertas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = Usuario.objects.get(user=self.request.user)
        ofertas = Oferta.objects.filter(usuario=usuario)
        context['ofertas'] = ofertas
        return context

class OfertaDeleteView(FormView):
    form_class = OfertaDeleteForm
    success_url = reverse_lazy('mis_ofertas')
    
    def form_valid(self, form):
        try:
            oferta_id = form.cleaned_data['oferta_id']
            if Oferta.objects.filter(id=oferta_id).exists():
                oferta = Oferta.objects.get(id=oferta_id)
                if oferta.usuario == Usuario.objects.get(user=self.request.user):
                    oferta.delete()
                    return super().form_valid(form)
            else:
                raise Exception('La oferta no existe o no eres el dueño')
        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(request, 'base/error.html', context)
