from django.urls import path
from . import views

app_name = 'if_dados'

urlpatterns = [
    path('abrir-chamado/', views.abrir_chamado, name='abrir_chamado'),
    path('chamado-enviado/', views.chamado_enviado, name='chamado_enviado'),
]
