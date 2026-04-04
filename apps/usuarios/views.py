from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .services import cadastrar_usuario, inicializar_banco, usuario_existe, validar_login


@csrf_exempt
def login_view(request):
    inicializar_banco()

    if request.method == "POST":
        usuario = request.POST.get("usuario", "").strip()
        senha = request.POST.get("senha", "").strip()

        if not usuario or not senha:
            messages.warning(request, "Preencha todos os campos")
            return redirect("/login")

        usuario_logado = validar_login(usuario, senha)

        if usuario_logado:
            request.session["usuario"] = usuario_logado
            messages.success(request, "Login realizado com sucesso!")

            next_page = request.POST.get("next") or request.GET.get("next")
            if not next_page or not next_page.startswith("/"):
                next_page = "/dashboard"
            return redirect(next_page)

        messages.error(request, "Usuário ou senha inválidos", extra_tags="danger")
        return redirect("/login")

    return render(request, "usuarios/login.html")


@csrf_exempt
def registro(request):
    inicializar_banco()

    if request.method == "POST":
        usuario = request.POST.get("usuario")
        senha = request.POST.get("senha")

        if not usuario or not senha:
            messages.warning(request, "Preencha todos os campos")
            return redirect("/registro")

        if usuario_existe(usuario):
            messages.error(request, "Usuário já existe", extra_tags="danger")
            return redirect("/registro")

        cadastrar_usuario(usuario, senha)
        messages.success(request, "Usuário cadastrado com sucesso!")
        return redirect("/login")

    return render(request, "usuarios/registro.html")


def logout_view(request):
    request.session.flush()
    messages.success(request, "Logout realizado com sucesso!")
    return redirect("/login")
