from django.urls import path
from .views import inicio, publicacion, EliminarPublicacionView, EditarPublicacionView,lista_recetas,lista_posts,publicar_post,loginView,register, ListaPublicacionesView, buscar_publicaciones, acerca_de, agregar_comentario, editar_perfil,ver_perfil
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', inicio, name='inicio'),
    path('publicacion/<int:publicacion_id>/', publicacion, name='publicacion'),
    path('lista_recetas/', lista_recetas, name='lista_recetas'),
    path('lista_posts/', lista_posts, name='lista_posts'),
    path('publicar_form/', publicar_post, name='publicar_form'), #crear publicacion desde el crud
    path('lista_publicaciones/',ListaPublicacionesView.as_view(), name="lista_publicaciones"), #lista crud
    path('eliminar_publicacion/<int:pk>/', EliminarPublicacionView.as_view(), name='eliminar_publicacion'), #eliminar
    path('editar_publicacion/<int:pk>/', EditarPublicacionView.as_view(), name='editar_publicacion'), #editar
    path('login/', loginView, name="Login"),
    path('registrar/', register, name="Registrar"),
    path('logout/', LogoutView.as_view(template_name="inicio.html"), name="Logout"),
    path('buscar/', buscar_publicaciones, name='buscar_publicaciones'),
    path('acerca/', acerca_de, name='acerca'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('comentario/<int:publicacion_id>/', agregar_comentario, name='agregar_comentario'),
    path('editar-perfil/', editar_perfil, name="Editar_perfil"),
     path('perfil/', ver_perfil, name='ver_perfil')
 


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)