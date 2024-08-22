from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('chamados/', views.chamados_view, name='chamados'),
    path('meus-chamados/', views.meus_chamados, name='meus_chamados'),
    path('abrir-chamado/', views.abrir_chamado, name='abrir-chamado'),
]