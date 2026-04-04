from django.urls import path

from . import views

urlpatterns = [
    path("doar", views.listar_doacoes, name="listar_doacoes"),
    path("doar/cadastrar", views.cadastrar_doacao, name="cadastrar_doacao"),
    path("excluir/<int:id>", views.excluir, name="excluir"),
    path("editar/<int:id>", views.editar, name="editar"),
]
