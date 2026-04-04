from django.shortcuts import redirect

from apps.usuarios.services import inicializar_banco

def home(request):
    inicializar_banco()
    return redirect("/dashboard")
