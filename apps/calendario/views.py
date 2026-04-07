from django.shortcuts import render, redirect
from django.views.decorators.csrf import  login_required
from django.contrib import messages

from .models import Evento
from .logica_pascoa import gerar_eventos


@login_required
def popular_eventos(request, ano):
    eventos = gerar_eventos(ano)

    for titulo, data, tipo in eventos:
        Evento.objects.get_or_create(
            titulo=titulo,
            data=data,
            tipo=tipo
        )

    messages.success(request, "Eventos criados com sucesso!")
    return redirect("/eventos")

@login_required
def listar_eventos(request):
    eventos = Evento.objects.all()

    return render(
        request,
        "eventos/lista.html",
        {"eventos": eventos}
    )



@login_required
def criar_evento(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        data = request.POST.get("data")
        descricao = request.POST.get("descricao")

        Evento.objects.create(
            titulo=titulo,
            data=data,
            tipo="personalizado",
            descricao=descricao
        )

        messages.success(request, "Evento criado com sucesso!")
        return redirect("/eventos")

    return render(request, "eventos/criar.html")



@login_required
def editar_evento(request, id):
    evento = Evento.objects.get(id=id)

    if request.method == "POST":
        evento.titulo = request.POST.get("titulo")
        evento.data = request.POST.get("data")
        evento.descricao = request.POST.get("descricao")
        evento.save()

        messages.success(request, "Evento atualizado com sucesso!")
        return redirect("/eventos")

    return render(
        request,
        "eventos/editar.html",
        {"evento": evento}
    )



@login_required
def deletar_evento(request, id):
    if request.method == "POST":
        evento = Evento.objects.get(id=id)
        evento.delete()

        messages.success(request, "Evento deletado com sucesso!")

    return redirect("/eventos")