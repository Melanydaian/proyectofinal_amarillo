
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('publicacion/<int:publicacion_id>/', views.publicacion, name='publicacion'),
    path('publicar_publicacion/', views.publicar_publicacion, name='publicar_publicacion'),
    path('eliminar_publicacion/<int:publicacion_id>/', views.EliminarPublicacionView.as_view(), name='eliminar_publicacion'),
    path('editar_publicacion/<int:publicacion_id>/', views.EditarPublicacionView.as_view(), name='editar_publicacion'),
    path('lista_recetas/', views.lista_recetas, name='lista_recetas'),
    path('lista_post/', views.lista_posts, name='lista_post'),


]
