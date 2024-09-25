from django import forms
from .models import Image


METHOD_CHOICES = [
    ('barcode', 'Codice a barre'),
    ('testo', 'Testo'),
    ('entrambi', 'entrambi'),
    ]


class MethodForm(forms.Form):
    method = forms.CharField(label='Metodo', widget=forms.RadioSelect(choices=METHOD_CHOICES), required=False)


class ImagesForm(forms.ModelForm):

    pic = forms.FileField(widget=forms.TextInput(attrs={
            "name": "images",
            "type": "File",
            "class": "form-control",
            "multiple": "True",
        }), label="Caricamento foto")

    class Meta:
        model = Image
        fields = ['pic']
