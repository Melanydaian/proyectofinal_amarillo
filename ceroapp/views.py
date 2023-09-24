
from django.shortcuts import render, redirect, get_object_or_404
from .models import Publicacion
from .forms import PublicacionForm  
from django.views import View

from django.shortcuts import render

def inicio(request):
    #muestra las últimas 5 publicaciones
    publicaciones = Publicacion.objects.order_by('-fecha_creacion')[:5]
    return render(request, 'padre.html', {'lista_de_publicaciones': publicaciones})



def publicacion(request, publicacion_id): #detalles de la publicacion
    publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
    return render(request, 'publicacion.html', {'publicacion': publicacion})

def publicar_publicacion(request): 
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_publicacion = form.save()
            return redirect('publicacion', publicacion_id=nueva_publicacion.pk)
    else:
        form = PublicacionForm()
    return render(request, 'publicar_publicacion.html', {'form': form})

class EliminarPublicacionView(View): #elimino publicacion solo si esta autorizado
    def get(self, request, publicacion_id):
        publicacion = Publicacion.objects.get(pk=publicacion_id)
        return render(request, 'eliminar_publicacion.html', {'publicacion': publicacion})

    def post(self, request, publicacion_id):
        publicacion = Publicacion.objects.get(pk=publicacion_id)
        publicacion.delete()
        return redirect('inicio')

class EditarPublicacionView(View):
    template_name = 'editar_publicacion.html'

    def get(self, request, publicacion_id):
        publicacion = Publicacion.objects.get(pk=publicacion_id)
        form = PublicacionForm(instance=publicacion)
        return render(request, self.template_name, {'form': form, 'publicacion': publicacion})

    def post(self, request, publicacion_id):
        publicacion = Publicacion.objects.get(pk=publicacion_id)
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('detalle_publicacion', publicacion_id=publicacion_id)
        return render(request, self.template_name, {'form': form, 'publicacion': publicacion})
    
#lista de recetas, que se accede desde el navbar "recetas"
def lista_recetas(request):
    recetas = Publicacion.objects.filter(tipo='receta')
    return render(request, 'lista_recetas.html', {'recetas': recetas})

#lista de posts, que se accede desde el navbar "blog"
def lista_posts(request):
    posts = Publicacion.objects.filter(tipo='post')
    return render(request, 'lista_posts.html', {'posts': posts})


