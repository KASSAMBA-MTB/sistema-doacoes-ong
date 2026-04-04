from django.urls import path
from .views import *

urlpatterns = [
    path('popular/<int:ano>/', popular_eventos),
    path('eventos/', listar_eventos),
    path('evento/criar/', criar_evento),
    path('evento/editar/<int:id>/', editar_evento),
    path('evento/deletar/<int:id>/', deletar_evento),
]