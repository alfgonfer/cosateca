from django import forms

class PeticionForm(forms.Form):
    titulo = forms.CharField(required=True)
    descripcion = forms.CharField(required=True, widget=forms.Textarea())

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



class PeticionDeleteForm(forms.Form):
    peticion_id = forms.IntegerField(widget=forms.HiddenInput(), required= True)