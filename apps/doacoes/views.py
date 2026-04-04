from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from apps.usuarios.decorators import login_required
from apps.usuarios.services import inicializar_banco

from .models import Doacao


@login_required
def listar_doacoes(request):
    inicializar_banco()

    dados = Doacao.objects.all().order_by("-data")

    doacoes = []
    for d in dados:
        data_formatada = "-"
        if d.data:
            data_formatada = d.data.strftime("%d/%m/%Y %H:%M")

        doacoes.append(
            {
                "id": d.id,
                "item": d.item,
                "quantidade": d.quantidade,
                "data": data_formatada,
            }
        )

    return render(request, "doacoes/doar_lista.html", {"doacoes": doacoes, "active": "lista"})


@csrf_exempt
@login_required
def cadastrar_doacao(request):
    inicializar_banco()

    if request.method == "POST":
        item = request.POST.get("item")
        quantidade = request.POST.get("quantidade")

        if item and quantidade:
            Doacao.objects.create(item=item, quantidade=int(quantidade))

            messages.success(request, "Doação cadastrada com sucesso!")
            return redirect("/doar")

    return render(request, "doacoes/doar_cadastro.html", {"active": "cadastro"})


@csrf_exempt
@login_required
def excluir(request, id):
    inicializar_banco()

    if request.method != "POST":
        return HttpResponseRedirect("/doar")

    Doacao.objects.filter(id=id).delete()

    messages.success(request, "Doação excluída com sucesso!")
    return redirect("/doar")


@csrf_exempt
@login_required
def editar(request, id):
    inicializar_banco()

    doacao_obj = Doacao.objects.filter(id=id).first()
    if not doacao_obj:
        return redirect("/doar")

    if request.method == "POST":
        item = request.POST.get("item")
        quantidade = request.POST.get("quantidade")

        if item and quantidade:
            doacao_obj.item = item
            doacao_obj.quantidade = int(quantidade)
            doacao_obj.save(update_fields=["item", "quantidade"])

            messages.success(request, "Doação atualizada com sucesso!")
            return redirect("/doar")

    doacao = (doacao_obj.item, doacao_obj.quantidade)

    return render(request, "doacoes/editar.html", {"doacao": doacao, "id": id})
