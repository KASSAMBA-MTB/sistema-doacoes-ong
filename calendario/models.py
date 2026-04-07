from django.db import models


class Evento(models.Model):
    TIPO_CHOICES = [
        ('liturgico', 'Litúrgico'),
        ('feriado', 'Feriado'),
        ('personalizado', 'Personalizado'),
    ]

    titulo = models.CharField(max_length=200)
    data = models.DateField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.data}"