from django import forms

class PrestarForm(forms.Form):
    peticion_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)

class SolicitarForm(forms.Form):
    oferta_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)

class PrestarNotificacionForm(forms.Form):
    oferta_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    nombre_recibidor = forms.CharField(widget=forms.HiddenInput(), required=True)