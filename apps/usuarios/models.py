from django.contrib.auth.hashers import check_password, make_password
from django.db import models


class Usuario(models.Model):
    usuario = models.CharField(max_length=150, unique=True)
    senha = models.CharField(max_length=255)

    class Meta:
        db_table = "usuarios"

    def set_senha(self, senha):
        self.senha = make_password(senha)

    def check_senha(self, senha):
        return check_password(senha, self.senha)
