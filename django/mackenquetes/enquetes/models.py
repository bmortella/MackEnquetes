from django.db import models

# Create your models here.
class Pergunta(models.Model):
    enunciado = models.CharField(max_length=200)
    data_pub = models.DateTimeField("Data de publicação")

    def __str__(self):
        return self.enunciado

class Escolha(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    texto = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.texto