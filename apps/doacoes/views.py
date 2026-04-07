from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages

from django.contrib.auth.decorators import login_required
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




@login_required
def cadastrar_doacao(request):
    if request.method == "POST":
        try:
            item = request.POST.get("item")
            quantidade = request.POST.get("quantidade")

            if not item:
                raise ValueError("Item é obrigatório")

            quantidade = int(quantidade)
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que 0")

            Doacao.objects.create(item=item, quantidade=quantidade)

            messages.success(request, "Doação cadastrada com sucesso!")
            return redirect("listar_doacoes")

        except ValueError as e:
            messages.error(request, str(e))

        except DatabaseError:
            messages.error(request, "Erro ao salvar no banco")

        except Exception:
            messages.error(request, "Erro inesperado")

    return render(request, "doacoes/doar_cadastro.html")


@login_required
def excluir(request, id):
    if request.method != "POST":
        messages.warning(request, "Ação inválida")
        return redirect("listar_doacoes")

    try:
        doacao = Doacao.objects.get(id=id)
        doacao.delete()

        messages.success(request, "Excluído com sucesso")

    except Doacao.DoesNotExist:
        messages.error(request, "Doação não encontrada")

    except Exception:
        messages.error(request, "Erro ao excluir")

    return redirect("listar_doacoes")


@login_required
def editar(request, id):
    try:
        doacao = Doacao.objects.get(id=id)
    except Doacao.DoesNotExist:
        messages.error(request, "Doação não encontrada")
        return redirect("listar_doacoes")

    if request.method == "POST":
        try:
            item = request.POST.get("item")
            quantidade = int(request.POST.get("quantidade"))

            if quantidade <= 0:
                raise ValueError("Quantidade inválida")

            doacao.item = item
            doacao.quantidade = quantidade
            doacao.save()

            messages.success(request, "Atualizado com sucesso")
            return redirect("listar_doacoes")

        except ValueError as e:
            messages.error(request, str(e))

        except Exception:
            messages.error(request, "Erro ao atualizar")

    return render(request, "doacoes/editar.html", {"doacao": doacao})
