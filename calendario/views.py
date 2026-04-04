from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Evento
from .logica_pascoa import gerar_eventos


def popular_eventos(request, ano):
    eventos = gerar_eventos(ano)

    for titulo, data, tipo in eventos:
        Evento.objects.get_or_create(
            titulo=titulo,
            data=data,
            tipo=tipo
        )

    return JsonResponse({"status": "Eventos criados"})



def listar_eventos(request):
    eventos = Evento.objects.all()

    data = [
        {
            "id": e.id,
            "title": e.titulo,
            "start": e.data,
            "tipo": e.tipo,
            "descricao": e.descricao
        }
        for e in eventos
    ]

    return JsonResponse(data, safe=False)


@csrf_exempt
def criar_evento(request):
    if request.method == "POST":
        dados = json.loads(request.body)

        evento = Evento.objects.create(
            titulo=dados["titulo"],
            data=dados["data"],
            tipo="personalizado",
            descricao=dados.get("descricao", "")
        )

        return JsonResponse({"status": "criado", "id": evento.id})

@csrf_exempt
def editar_evento(request, id):
    evento = Evento.objects.get(id=id)

    if request.method == "PUT":
        dados = json.loads(request.body)

        evento.titulo = dados.get("titulo", evento.titulo)
        evento.data = dados.get("data", evento.data)
        evento.descricao = dados.get("descricao", evento.descricao)
        evento.save()

        return JsonResponse({"status": "atualizado"})


@csrf_exempt
def deletar_evento(request, id):
    if request.method == "DELETE":
        evento = Evento.objects.get(id=id)
        evento.delete()

        return JsonResponse({"status": "deletado"})
