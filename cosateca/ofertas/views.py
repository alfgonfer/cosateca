from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Oferta, Comentario
from .forms import OfertaForm, OfertaDeleteForm, ComentarForm, BuscarForm
from usuarios.models import Usuario

class OfertaListView(ListView):
    template_name='ofertas/lista_ofertas.html'
    model = Oferta
    context_object_name = 'ofertas'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        buscar_form = BuscarForm
        context['buscar_form'] = buscar_form
        return context

    def get_queryset(self):
        texto = self.request.GET.get('texto', '')
        provincia = self.request.GET.get('provincia', '')
        lista_ofertas = Oferta.objects.all()
        ofertas =  []
        for oferta in lista_ofertas:
            if texto != '' and provincia != '':
                if (texto.lower() in oferta.titulo.lower() or texto.lower() in oferta.descripcion.lower()) and provincia == oferta.provincia:
                    ofertas.append(oferta)
            elif texto != '':
                if texto.lower() in oferta.titulo.lower() or texto.lower() in oferta.descripcion.lower():
                    ofertas.append(oferta)
            elif provincia != '':
                if provincia == oferta.provincia:
                    ofertas.append(oferta)
            else:
                ofertas.append(oferta)
            
        return ofertas
        

@method_decorator(login_required, name='dispatch')
class OfertaCreateView(FormView):
    form_class = OfertaForm
    template_name = 'ofertas/crear_oferta.html'
    success_url = reverse_lazy('ofertas')

    def form_valid(self, form):
        usuario = Usuario.objects.get(user=self.request.user)
        imagen = form.cleaned_data['imagen']
        titulo = form.cleaned_data['titulo']
        descripcion = form.cleaned_data['descripcion']
        provincia = form.cleaned_data['provincia']
        Oferta.objects.create(usuario=usuario, titulo=titulo, descripcion=descripcion, imagen=imagen, provincia=provincia)
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
        comentarios = Comentario.objects.filter(oferta=oferta)
        context['comentarios'] = comentarios
        context['oferta'] = oferta
        return context

@method_decorator(login_required, name='dispatch')
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
        provincia = form.cleaned_data['provincia']
        descripcion = form.cleaned_data['descripcion']
        oferta.imagen = imagen
        oferta.titulo = titulo
        oferta.provincia = provincia
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

@method_decorator(login_required, name='dispatch')
class MisOfertasView(TemplateView):
    template_name = 'ofertas/mis_ofertas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = Usuario.objects.get(user=self.request.user)
        ofertas = Oferta.objects.filter(usuario=usuario)
        context['ofertas'] = ofertas
        return context

@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class ComentarFormView(FormView):
    form_class = ComentarForm
    oferta_id = None

    def form_valid(self, form):
        self.oferta_id = self.kwargs['oferta_id']
        oferta = Oferta.objects.get(id=self.oferta_id)
        usuario = Usuario.objects.get(user=self.request.user)
        texto = form.cleaned_data['texto']
        Comentario.objects.create(usuario=usuario, oferta=oferta, texto=texto)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mostrar_oferta', kwargs={'oferta_id':self.oferta_id})