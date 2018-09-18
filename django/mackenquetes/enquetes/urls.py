from django.urls import path
from . import views

app_name = "enquetes"
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('<int:pk>/detalhes', views.DetalhesView.as_view(), name="detalhes"),
    path('<int:enquete_id>/votar', views.votar, name="votar"),
    path('<int:pk>/resultados', views.ResultadosView.as_view(), name="resultados")
]
