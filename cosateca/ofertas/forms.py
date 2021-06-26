from django import forms

class OfertaForm(forms.Form):
    titulo = forms.CharField(required=True)
    descripcion = forms.CharField(required=True, widget=forms.Textarea())
    imagen = forms.CharField(required=True)

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