from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if "usuario" not in request.session:
            messages.warning(request, "Faça login para acessar o sistema")
            return redirect(f"/login?next={request.path}")
        return func(request, *args, **kwargs)

    return wrapper
