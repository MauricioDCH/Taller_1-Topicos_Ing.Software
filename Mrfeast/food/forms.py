from django.forms import ModelForm, Textarea 
from .models import Review

class ReviewForm(ModelForm): 
    def __init__(self, *args, **kwargs): 
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update( {'class': 'form-control'}) 
        self.fields['favorito'].widget.attrs.update( {'class': 'form-check-input'}) 
        self.fields['calificacion']
        
    class Meta: 
        model = Review 
        fields = ['text','favorito', 'calificacion'] 
        labels = { 'favorito': ('Favorito'), 'calificacion':('Calificación 1 a 5') } 
        widgets = { 'text': Textarea(attrs={'rows': 4}), }

# forms.py

from django import forms

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre')
    email = forms.EmailField(label='Correo Electrónico')
    mensaje = forms.CharField(widget=forms.Textarea, label='Mensaje')
