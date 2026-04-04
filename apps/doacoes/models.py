from django.db import models


class Doacao(models.Model):
    item = models.CharField(max_length=255)
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "doacoes"
