from django.conf import settings
from django.db import models
from django.utils import timezone

class Especialidade(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Tecnico(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=11, blank=True, null=True)
    especialidades = models.ManyToManyField(Especialidade, blank=True)

    def __str__(self):
        return self.nome

class Equipamento(models.Model):
    tipo_de_equipamento = models.CharField(max_length=255)
    especialidades_requeridas = models.ManyToManyField(Especialidade, blank=True)

    def __str__(self):
        return self.tipo_de_equipamento

class Chamado(models.Model):
    class Status(models.TextChoices):
        ABERTO = 'Aberto', 'Aberto'
        FECHADO = 'Fechado', 'Fechado'
        PENDENTE = 'Pendente', 'Pendente'
        REABERTO = 'Reaberto', 'Reaberto'

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ABERTO)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, blank=True, null=True, related_name='chamados')
    departamento = models.CharField(max_length=255)
    sala = models.CharField(max_length=255)
    descricao_problema = models.TextField()
    patrimonio = models.CharField(max_length=6, blank=True, null=True)
    data_abertura = models.DateField(default=timezone.now)
    data_fechamento = models.DateField(blank=True, null=True)
    data_modificacao = models.DateField(blank=True, null=True)
    data_reabertura = models.DateField(blank=True, null=True)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, blank=True, null=True)
    relato_tecnico = models.TextField(blank=True, null=True)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.SET_NULL, null=True, blank=True)

    def marcar_como_concluido(self):
        self.status = self.Status.FECHADO
        self.data_fechamento = timezone.now()
        self.save()

    def __str__(self):
        return f"Chamado {self.id} - {self.departamento}"
