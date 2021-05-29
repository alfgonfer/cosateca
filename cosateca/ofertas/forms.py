from django import forms

class OfertaForm(forms.Form):
    titulo = forms.CharField(max_length=50,required=True)
    descripcion = forms.CharField(max_length=300, required=True, widget=forms.Textarea())
    imagen = forms.CharField(required=True)

class OfertaDeleteForm(forms.Form):
    oferta_id = forms.IntegerField(widget=forms.HiddenInput(), required= True)