import logging
from django.shortcuts import redirect
from django.contrib import messages

logger = logging.getLogger(__name__)

def home(request):
    try:
        return redirect("dashboard")

    except Exception as e:
        logger.error(f"Erro ao redirecionar home: {e}")
        messages.error(request, "Erro ao acessar o sistema")

        return redirect("login")