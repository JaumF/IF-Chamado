# Generated by Django 5.1 on 2024-08-18 20:46

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Equipamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_de_equipamento', models.CharField(max_length=255)),
                ('especialidades_requeridas', models.ManyToManyField(blank=True, to='if_dados.especialidade')),
            ],
        ),
        migrations.CreateModel(
            name='Tecnico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(blank=True, max_length=11, null=True)),
                ('especialidades', models.ManyToManyField(blank=True, to='if_dados.especialidade')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chamado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Aberto', 'Aberto'), ('Fechado', 'Fechado'), ('Pendente', 'Pendente'), ('Reaberto', 'Reaberto')], default='Aberto', max_length=10)),
                ('departamento', models.CharField(max_length=255)),
                ('sala', models.CharField(max_length=255)),
                ('descricao_problema', models.TextField()),
                ('patrimonio', models.CharField(blank=True, max_length=6, null=True)),
                ('data_abertura', models.DateField(default=django.utils.timezone.now)),
                ('data_fechamento', models.DateField(blank=True, null=True)),
                ('data_modificacao', models.DateField(blank=True, null=True)),
                ('data_reabertura', models.DateField(blank=True, null=True)),
                ('relato_tecnico', models.TextField(blank=True, null=True)),
                ('usuario', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('equipamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='if_dados.equipamento')),
                ('especialidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='if_dados.especialidade')),
                ('tecnico', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chamados', to='if_dados.tecnico')),
            ],
        ),
    ]
