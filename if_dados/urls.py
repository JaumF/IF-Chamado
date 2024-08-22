from django.urls import path
from . import views

urlpatterns = [
    path('submit-chamado/', views.submit_chamado, name='submit-chamado'),
    path('chamado_enviado/<int:chamado_id>/', views.chamado_enviado, name='chamado_enviado'),
    path('chamados/', views.listar_chamados_disponiveis, name='listar_chamados_disponiveis'),
    path('detalhes/<int:id>/', views.detalhes_do_chamado_aberto, name='detalhes_do_chamado_aberto'),
    path('meus-chamados/', views.meus_chamados, name='meus_chamados'),
]
