from django import forms
from .models import Publicacion

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'subtitulo', 'copy', 'autor', 'imagen', 'tipo', 'ingredientes', 'video']

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')

        #Si la publicación es de tipo 'post', se elimna el campo 'ingredientes'
        if tipo == 'post':
            cleaned_data.pop('ingredientes', None)  

        return cleaned_data
