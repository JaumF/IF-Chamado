# Generated by Django 5.1 on 2024-08-21 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('if_dados', '0003_remove_chamado_equipamento_delete_equipamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamado',
            name='equipamento',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
