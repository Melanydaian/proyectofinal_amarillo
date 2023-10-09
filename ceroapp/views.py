
from django.shortcuts import render, redirect, get_object_or_404
from .models import Publicacion, Comentario
from .forms import PublicacionForm
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import ComentarioForm, UserEditForm


def inicio(request):
    #muestra las últimas 6 publicaciones
    publicaciones = Publicacion.objects.order_by('-fecha_creacion')[:6]
    return render(request, 'inicio.html', {'lista_de_publicaciones': publicaciones})

def publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
    ingredientes = publicacion.ingredientes.split(',') if publicacion.tipo == 'receta' else None
    
    context = {
        'publicacion': publicacion,
        'ingredientes': ingredientes,
    }
    
    return render(request, 'publicacion.html', context)

#crud para el admin
def publicar_publicacion(request): 
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_publicacion = form.save()
            return redirect('publicacion', publicacion_id=nueva_publicacion.pk)
    else:
        form = PublicacionForm()
    return render(request, 'publicar_publicacion.html', {'form': form})

#lista crud
class ListaPublicacionesView(ListView):
    model = Publicacion
    template_name = 'lista_publicaciones.html'
    context_object_name = 'publicaciones'
    paginate_by = 6  

    def get_queryset(self):
        return Publicacion.objects.all()


class EditarPublicacionView(UpdateView):
    model = Publicacion
    form_class = PublicacionForm
    template_name = 'editar_publicacion.html'
    success_url = reverse_lazy('lista_publicaciones')

class EliminarPublicacionView(DeleteView):
    model = Publicacion
    template_name = 'eliminar_publicacion.html'
    success_url = reverse_lazy('lista_publicaciones')

#lista de recetas   
def lista_recetas(request):
    recetas = Publicacion.objects.filter(tipo='receta')
    
 
    paginator = Paginator(recetas, 5)
    
    page = request.GET.get('page')  
    try:
        recetas = paginator.page(page)
    except PageNotAnInteger:
        
        recetas = paginator.page(1)
    except EmptyPage:
        recetas = paginator.page(paginator.num_pages)
    
    return render(request, 'lista_recetas.html', {'recetas': recetas})

#lista de posteos del blog
def lista_posts(request):
    posts = Publicacion.objects.filter(tipo='post')
    paginator = Paginator(posts, 5)
    
    page = request.GET.get('page') 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:

        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'lista_posts.html', {'posts': posts})

#formulario para publicar recetas 
@staff_member_required(login_url='/ceroapp/inicio') 
def publicar_post(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save()
            return redirect('publicacion', publicacion_id=publicacion.id)
    else:
        form = PublicacionForm()
    
        return render(request, 'publicar_form.html', {'form': form})

def loginView(request):
    if request.method == 'POST':
        miFormulario = AuthenticationForm(request, data=request.POST)
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            usuario = data["username"]
            psw = data["password"]
            user = authenticate(username=usuario, password=psw)
            if user:
                login(request, user)
                return render(request, "inicio.html", {"mensaje": f"Bienvenido {usuario}"})
            else:
                return render(request, "inicio.html", {"mensaje": "Datos incorrectos"})
        else:
            return render(request, "inicio.html", {"mensaje": "Datos incorrectos vuelva a intentar"})
    else:
        miFormulario = AuthenticationForm()
        return render(request, "login.html", {"miFormulario": miFormulario})


#registro del usuario
def register(req):
    if req.method == 'POST':
        miFormulario = UserCreationForm(req.POST)
        if miFormulario.is_valid():
            nuevo_usuario = miFormulario.save()
            return render(req, "inicio.html", {"mensaje": f"Usuario {nuevo_usuario} creado con exito, inicie sesion"})  
        else:
           return render(req, "inicio.html", {"mensaje": "Registro incorrecto, reintentelo"})
    
    else:
        miFormulario = UserCreationForm()
    
    return render(req, "registro.html", {"miFormulario": miFormulario})


#busqueda
def buscar_publicaciones(request):
    query = request.GET.get('q')  
    if query:
        resultados = Publicacion.objects.filter(Q(titulo__icontains=query) | Q(subtitulo__icontains=query))
    else:
        resultados = []  

    return render(request, 'resultado_busqueda.html', {'resultados': resultados, 'query': query})

def acerca_de(request):
    return render(request, 'acerca_de.html')

#sistema de comentarios 
@login_required
def agregar_comentario(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == 'POST':
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            nuevo_comentario = comentario_form.save(commit=False)
            nuevo_comentario.autor = request.user
            nuevo_comentario.publicacion = publicacion
            nuevo_comentario.save()
            return redirect('publicacion', publicacion_id=publicacion_id)

    else:
        comentario_form = ComentarioForm()

    return render(request, 'comentarios.html', {'publicacion': publicacion, 'comentario_form': comentario_form})

#editar perfil
def editar_perfil(req):

    usuario = req.user

    if req.method == 'POST':

        miFormulario = UserEditForm(req.POST, instance=req.user)
        
        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
            print(miFormulario)
            usuario.first_name = data["first_name"]
            usuario.last_name = data["last_name"]
            usuario.email = data["email"]
            usuario.set_password(data["password1"])
            usuario.save()
           
            return render(req, "inicio.html", {"mensaje": "Perfil actualizado con éxito"})
        else:
            return render(req, "editar_perfil.html", {"miFomulario": miFormulario})
    else:

        miFormulario = UserEditForm(instance=req.user)

        return render(req, "editar_perfil.html", {"miFomulario": miFormulario})
   
@login_required
def ver_perfil(request):
    usuario = request.user
    return render(request, 'ver_perfil.html', {'usuario': usuario})