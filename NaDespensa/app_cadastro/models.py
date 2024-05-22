from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    quantidade = models.PositiveIntegerField()
    validade = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
