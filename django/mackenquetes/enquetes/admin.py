from django.contrib import admin
from .models import Pergunta, Escolha

# Register your models here.
class EscolhaInline(admin.TabularInline):
    model = Escolha
    extra = 2

class PerguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['enunciado']}),
        ('Data', {'fields':['data_pub']})
    ]
    inlines = [EscolhaInline]
    list_display = ('enunciado', 'data_pub')
    list_filter = ['data_pub']
    search_fields = ['enunciado']

admin.site.register(Pergunta, PerguntaAdmin)