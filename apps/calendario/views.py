from django.shortcuts import render, redirect
from django.contrib.auth.decorators import  login_required
from django.contrib import messages

from .models import Evento
from .logica_pascoa import gerar_eventos

from django.db import DatabaseError
import logging

logger = logging.getLogger(__name__)

@login_required
def popular_eventos(request, ano):
    try:
        eventos = gerar_eventos(ano)

        for titulo, data, tipo in eventos:
            Evento.objects.get_or_create(
                titulo=titulo,
                data=data,
                tipo=tipo
            )

        messages.success(request, "Eventos criados com sucesso!")

    except DatabaseError as e:
        logger.error(f"Erro no banco: {e}")
        messages.error(request, "Erro ao salvar eventos")

    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        messages.error(request, "Erro interno")

    return redirect("listar_eventos")

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
        try:
            titulo = request.POST.get("titulo", "").strip()
            data = request.POST.get("data")

            if not titulo or not data:
                raise ValueError("Título e data são obrigatórios")

            Evento.objects.create(
                titulo=titulo,
                data=data,
                tipo="personalizado",
                descricao=request.POST.get("descricao", "")
            )

            messages.success(request, "Evento criado com sucesso!")
            return redirect("listar_eventos")

        except ValueError as e:
            messages.warning(request, str(e))

        except Exception as e:
            logger.error(f"Erro ao criar evento: {e}")
            messages.error(request, "Erro ao criar evento")

        return redirect("criar_evento")

    return render(request, "eventos/criar.html")


@login_required
def editar_evento(request, id):
    try:
        evento = Evento.objects.get(id=id)
    except Evento.DoesNotExist:
        messages.error(request, "Evento não encontrado")
        return redirect("listar_eventos")

    if request.method == "POST":
        try:
            titulo = request.POST.get("titulo", "").strip()
            data = request.POST.get("data")

            if not titulo or not data:
                raise ValueError("Campos obrigatórios")

            evento.titulo = titulo
            evento.data = data
            evento.descricao = request.POST.get("descricao", "")
            evento.save()

            messages.success(request, "Evento atualizado!")
            return redirect("listar_eventos")

        except ValueError as e:
            messages.warning(request, str(e))

        except Exception as e:
            logger.error(f"Erro ao editar: {e}")
            messages.error(request, "Erro ao atualizar")

        return redirect("editar_evento", id=id)

    return render(request, "eventos/editar.html", {"evento": evento})


@login_required
def deletar_evento(request, id):
    if request.method != "POST":
        messages.warning(request, "Requisição inválida")
        return redirect("listar_eventos")

    try:
        evento = Evento.objects.get(id=id)
        evento.delete()

        messages.success(request, "Evento deletado com sucesso!")

    except Evento.DoesNotExist:
        messages.error(request, "Evento não encontrado")

    except Exception as e:
        logger.error(f"Erro ao deletar: {e}")
        messages.error(request, "Erro ao deletar")

    return redirect("listar_eventos")