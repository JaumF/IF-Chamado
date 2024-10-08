from django.conf import settings
from django.db import models
from django.utils import timezone

# Define the Especialidade model
class Especialidade(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# Define the Tecnico model
class Tecnico(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True, null=True)
    especialidades = models.ManyToManyField(Especialidade, blank=True)

    def __str__(self):
        return self.nome

# Define the Chamado model
class Chamado(models.Model):
    class Status(models.TextChoices):
        ABERTO = 'Aberto', 'Aberto'
        FECHADO = 'Fechado', 'Fechado'
        PENDENTE = 'Pendente', 'Pendente'
        REABERTO = 'Reaberto', 'Reaberto'

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ABERTO)
    departamento = models.CharField(max_length=255)
    sala = models.CharField(max_length=255)
    descricao_problema = models.TextField()
    patrimonio = models.CharField(max_length=50, blank=True, null=True)
    data_abertura = models.DateTimeField(default=timezone.now)
    data_fechamento = models.DateTimeField(blank=True, null=True)
    data_modificacao = models.DateTimeField(blank=True, null=True)
    data_reabertura = models.DateTimeField(blank=True, null=True)
    equipamento = models.CharField(max_length=255, blank=True, null=True)
    especialidade = models.ManyToManyField(Especialidade, blank=True)
    relato_tecnico = models.TextField(blank=True)

    def marcar_como_concluido(self):
        self.status = self.Status.FECHADO
        self.data_fechamento = timezone.now()
        self.save()


    def reabrir(self):
        self.status = self.Status.REABERTO
        self.data_reabertura = timezone.now()
        self.save()


    def __str__(self):
        user_email = getattr(self.usuario, 'email', 'Email desconhecido')
        return f"Chamado {self.id} - {self.departamento} - {user_email}"

# Define the HistoricoChamado model
class HistoricoChamado(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE)
    data_fechamento = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=Chamado.Status.choices)
    relatorio = models.TextField(blank=True)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Histórico do Chamado {self.chamado.id} - {self.status}"
