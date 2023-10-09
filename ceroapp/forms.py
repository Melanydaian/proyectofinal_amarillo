from django import forms
from .models import Publicacion, Comentario
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'subtitulo', 'copy', 'autor', 'imagen', 'tipo', 'ingredientes',]

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')

        #Si la publicación es de tipo 'post', se elimna el campo 'ingredientes'
        if tipo == 'post':
            cleaned_data.pop('ingredientes', None)  

        return cleaned_data

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
    'texto': forms.Textarea(attrs={'placeholder': 'Escribe tu comentario aquí...'}),
    }
        
class UserEditForm(UserChangeForm):

    password = forms.CharField(
        help_text="",
        widget=forms.HiddenInput(), required=False
    )

    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repita contraseña", widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_password2(self):

        print(self.cleaned_data)

        password2 = self.cleaned_data["password2"]
        if password2 != self.cleaned_data["password1"]:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2
    