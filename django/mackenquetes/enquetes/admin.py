from django.contrib import admin
from .models import Pergunta, Escolha

# Register your models here.
admin.site.egister(Pergunta)
admin.site.register(Escolha)