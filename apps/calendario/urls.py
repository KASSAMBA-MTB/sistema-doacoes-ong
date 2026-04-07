from django.urls import path
from . import views

urlpatterns = [
    path('popular/<int:ano>/', views.popular_eventos, name='popular_eventos'),
    path('eventos/', views.listar_eventos, name='listar_eventos'),
    path('evento/criar/', views.criar_evento, name='criar_evento'),
    path('evento/editar/<int:id>/', views.editar_evento, name='editar'),
    path('evento/deletar/<int:id>/', views.deletar_evento, name='excluir'),
]


