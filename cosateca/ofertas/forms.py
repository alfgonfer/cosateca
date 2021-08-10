from django import forms
from django.forms import widgets
from django.forms.fields import ChoiceField
from django.utils.translation import ugettext_lazy as _

PROVINCIAS_CHOICES=[
    ('Álava', _('Álava')),
    ('Albacete', _('Albacete')),
    ('Alicante', _('Alicante')),
    ('Almería', _('Almería')),
    ('Ávila', _('Ávila')),
    ('Badajoz', _('Badajoz')),
    ('Baleares', _('Baleares')),
    ('Barcelona', _('Barcelona')),
    ('Burgos', _('Burgos')),
    ('Cáceres', _('Cáceres')),
    ('Cádiz', _('Cádiz')),
    ('Castellón', _('Castellón')),
    ('Ciudad Real', _('Ciudad Real')),
    ('Córdoba', _('Córdoba')),
    ('A Coruña', _('A Coruña')),
    ('Cuenca', _('Cuenca')),
    ('Girona', _('Girona')),
    ('Granada', _('Granada')),
    ('Guadalajara', _('Guadalajara')),
    ('Guipúzcoa', _('Guipúzcoa')),
    ('Huelva', _('Huelva')),
    ('Huesca', _('Huesca')),
    ('Jaén', _('Jaén')),
    ('León', _('León')),
    ('Lleida', _('Lleida')),
    ('La Rioja', _('La Rioja')),
    ('Lugo', _('Lugo')),
    ('Madrid', _('Madrid')),
    ('Málaga', _('Málaga')),
    ('Murcia', _('Murcia')),
    ('Navarra', _('Navarra')),
    ('Orense', _('Orense')),
    ('Asturias', _('Asturias')),
    ('Palencia', _('Palencia')),
    ('Las Palmas', _('Las Palmas')),
    ('Pontevedra', _('Pontevedra')),
    ('Salamanca', _('Salamanca')),
    ('Santa Cruz de Tenerife', _('Santa Cruz de Tenerife')),
    ('Cantabria', _('Cantabria')),
    ('Segovia', _('Segovia')),
    ('Sevilla', _('Sevilla')),
    ('Soria', _('Soria')),
    ('Tarragona', _('Tarragona')),
    ('Teruel', _('Teruel')),
    ('Toledo', _('Toledo')),
    ('Valencia', _('Valencia')),
    ('Valladolid', _('Valladolid')),
    ('Vizcaya', _('Vizcaya')),
    ('Zamora', _('Zamora')),
    ('Zaragoza', _('Zaragoza')),
    ('Ceuta', _('Ceuta')),
    ('Melilla', _('Melilla'))
]

class OfertaForm(forms.Form):
    titulo = forms.CharField(required=True)
    descripcion = forms.CharField(required=True, widget=forms.Textarea())
    imagen = forms.CharField(required=True)
    provincia = forms.ChoiceField(widget=forms.Select(attrs={'class' : 'form-control', 'name' : 'provincia'}), choices=PROVINCIAS_CHOICES, required=True)

    def clean(self):
        titulo = self.cleaned_data.get('titulo')
        descripcion = self.cleaned_data.get('descripcion')
        if len(str(titulo)) > 50:
            msg = 'El título debe tener como máximo 50 caracteres (tiene ' + str(len(titulo)) + ')'
            self._errors['titulo'] = self.error_class([msg])
        if len(str(descripcion)) > 250:
            msg = 'La descripción debe tener como máximo 250 caracteres (tiene ' + str(len(descripcion)) +')'
            self._errors['descripcion'] = self.error_class([msg])
        return self.cleaned_data

class OfertaDeleteForm(forms.Form):
    oferta_id = forms.IntegerField(widget=forms.HiddenInput(), required= True)

class ComentarForm(forms.Form):
    texto = forms.CharField(required=True)

    def clean(self):
        texto = self.cleaned_data.get('texto')
        if len(str(texto)) > 400:
            msg = 'El comentario debe tener como máximo 400 caracteres (tiene ' + str(len(descripcion)) +')'
        return self.cleaned_data


class BuscarForm(forms.Form):
    texto = forms.CharField()
    provincia = forms.ChoiceField(widget=forms.Select(attrs={'class' : 'form-control rounded', 'name' : 'provincia'}), choices=PROVINCIAS_CHOICES)