from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse

from .models import Pergunta, Escolha

# Create your views here.
class IndexView(generic.ListView):
    template_name = "enquetes/index.html"
    context_object_name = "enquetes"

    def get_queryset(self):
        enquetes = Pergunta.objects.all()[:6]
        return enquetes

class DetalhesView(generic.DetailView):
    template_name = "enquetes/detalhes.html"
    model = Pergunta

def votar(request, enquete_id):
    pergunta = get_object_or_404(Pergunta, pk=enquete_id)
    try:
        escolha = pergunta.escolha_set.get(pk=request.POST['escolha'])
    except (KeyError, Escolha.DoesNotExist):
        return render(request, 'enquetes/detalhes.html', {
            'pergunta':pergunta,
            'erro':'Você não selecionou uma opção.',
        })
    
    escolha.votos += 1
    escolha.save()
    return HttpResponseRedirect(reverse('enquetes:resultados', args=(pergunta.id,)))

class ResultadosView(generic.DetailView):
    template_name = "enquetes/resultados.html"
    model = Pergunta