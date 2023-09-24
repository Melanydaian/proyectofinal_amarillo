from django.db import models

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
    video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name="Video de la publicacion")

    def __str__(self):
        return self.titulo
    

    def get_ingredientes_lista(self):
        if self.ingredientes:
            return self.ingredientes.split('\n')  
        else:
            return []