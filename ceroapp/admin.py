from django.contrib import admin
from .models import Publicacion, Comentario

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
   list_display = ('titulo', 'autor', 'fecha_creacion')
   list_filter = ('autor', 'fecha_creacion')  
   search_fields = ('titulo', 'contenido')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'texto', 'fecha_publicacion', 'publicacion')
    list_filter = ('autor', 'publicacion')
