import json

from django.shortcuts import render

from apps.usuarios.decorators import login_required
from apps.usuarios.services import inicializar_banco
from apps.doacoes.models import Doacao


@login_required
def dashboard(request):
    inicializar_banco()

    total_doacoes = Doacao.objects.count()
    total_itens = sum(Doacao.objects.values_list("quantidade", flat=True)) if total_doacoes else 0

    acumulado = {}
    for item, qtd in Doacao.objects.values_list("item", "quantidade"):
        acumulado[item] = acumulado.get(item, 0) + qtd

    dados = sorted(acumulado.items(), key=lambda x: x[1], reverse=True)

    top_itens = dados[:3] if dados else []
    labels = [d[0] for d in dados] if dados else []
    valores = [d[1] for d in dados] if dados else []

    return render(
        request,
        "dashboards/dashboard.html",
        {
            "total_doacoes": total_doacoes,
            "total_itens": total_itens,
            "labels": labels,
            "valores": valores,
            "top_itens": top_itens,
            "labels_json": json.dumps(labels, ensure_ascii=False),
            "valores_json": json.dumps(valores, ensure_ascii=False),
        },
    )
