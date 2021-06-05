from django import forms

class PrestarForm(forms.Form):
    peticion_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)

class SolicitarForm(forms.Form):
    oferta_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)