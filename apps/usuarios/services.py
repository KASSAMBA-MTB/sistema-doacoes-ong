import threading

from django.contrib.auth.hashers import make_password

from .models import Usuario


_db_lock = threading.Lock()
_db_initialized = False


def criar_usuario_padrao():
    if not Usuario.objects.filter(usuario="admin").exists():
        Usuario.objects.create(usuario="admin", senha=make_password("123"))


def inicializar_banco():
    global _db_initialized

    if _db_initialized:
        return

    with _db_lock:
        if _db_initialized:
            return

        criar_usuario_padrao()
        _db_initialized = True


def validar_login(usuario, senha):
    resultado = Usuario.objects.filter(usuario=usuario).first()

    if not resultado:
        return None

    if resultado.check_senha(senha):
        return resultado.usuario

    return None


def usuario_existe(usuario):
    return Usuario.objects.filter(usuario=usuario).exists()


def cadastrar_usuario(usuario, senha):
    Usuario.objects.create(usuario=usuario, senha=make_password(senha))
