from django.db import models
from django.utils.html import format_html
from PIL import Image
from django.contrib.auth.models import User
from django import forms
class Publicacion(models.Model):
    TIPOS_DE_PUBLICACION = (
        ('post', 'Post'),
        ('receta', 'Receta'),
    )

    tipo = models.CharField(max_length=10, choices=TIPOS_DE_PUBLICACION, default='receta')
    titulo = models.CharField(max_length=100, verbose_name="Titulo de la publicación")
    subtitulo = models.CharField(max_length=100, verbose_name="Subtitulo de la publicación")
    copy = models.TextField(("Contenido de la publicación"))
    autor = models.CharField(max_length=50, verbose_name="Nombre del autor")
    fecha_creacion = models.DateTimeField(auto_now_add=True)  
    imagen = models.ImageField(verbose_name="Imagen de la publicación", upload_to='imagenes/')
    ingredientes = models.TextField(("Ingredientes de la receta"), blank=True, null=True)

    def __str__(self):
        return self.titulo
    

    def get_ingredientes_lista(self):
        if self.ingredientes:
            return self.ingredientes.split('\n')  
        else:
            return []
        

class Comentario(models.Model):
    autor = models.CharField(max_length=25)
    texto = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comentarios')

    def __str__(self):
        return f"Comentario de {self.autor} en {self.fecha_publicacion}"
    
widgets = {
    'texto': forms.Textarea(attrs={'placeholder': 'Escribe tu comentario aquí...'}),
    }