from django.urls import path
from . import views

urlpatterns = [
    path('submit-chamado/', views.submit_chamado, name='submit-chamado'),  # Submissão do chamado
]
