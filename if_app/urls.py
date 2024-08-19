from django.urls import path
from . import views

app_name = 'if_app'

urlpatterns = [
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('chamados/', views.chamados_view, name='chamados'),
    path('abrir-chamado/', views.abrir_chamado, name='abrir-chamado'),
]