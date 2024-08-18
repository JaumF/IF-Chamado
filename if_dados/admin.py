from django.contrib import admin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils import timezone

from .models import Tecnico, Equipamento, Chamado, Especialidade
from .forms import FecharChamadoForm

@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'telefone', 'get_especialidades')
    search_fields = ('nome', 'email')

    def get_especialidades(self, obj):
        return ", ".join([especialidade.nome for especialidade in obj.especialidades.all()])
    get_especialidades.short_description = 'Especialidades'

@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_de_equipamento', 'get_especialidades_requeridas')
    search_fields = ('tipo_de_equipamento',)

    def get_especialidades_requeridas(self, obj):
        return ", ".join([especialidade.nome for especialidade in obj.especialidades_requeridas.all()])
    get_especialidades_requeridas.short_description = 'Especialidades Requeridas'

@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'departamento', 'sala', 'equipamento', 'descricao_problema', 'patrimonio', 'data_abertura', 'status', 'tecnico', 'fechar_chamado_link'
    )
    list_filter = ('status', 'departamento', 'equipamento', 'tecnico')
    search_fields = ('departamento', 'sala', 'descricao_problema', 'patrimonio')
    readonly_fields = ('data_abertura', 'data_fechamento', 'data_modificacao', 'data_reabertura')
    fields = (
        'departamento', 'sala', 'equipamento', 'descricao_problema', 'patrimonio', 'status', 'tecnico',
        'data_abertura', 'data_fechamento', 'data_modificacao', 'data_reabertura', 'relato_tecnico'
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'chamado/<int:chamado_id>/fechar/',
                self.admin_site.admin_view(self.fechar_chamado_view),
                name='fechar_chamado',
            ),
        ]
        return custom_urls + urls

    def fechar_chamado_view(self, request, chamado_id):
        chamado = get_object_or_404(Chamado, id=chamado_id)
        if request.method == 'POST':
            form = FecharChamadoForm(request.POST, instance=chamado)
            if form.is_valid():
                chamado = form.save(commit=False)
                chamado.status = Chamado.Status.FECHADO
                chamado.data_fechamento = timezone.now()
                chamado.save()
                self.message_user(request, 'Chamado fechado com sucesso!')
                return redirect('admin:if_dados_chamado_changelist')
        else:
            form = FecharChamadoForm(instance=chamado)
        
        context = {
            'form': form,
            'chamado': chamado,
            'opts': self.model._meta,
            'change': True,
            'is_popup': False,
            'save_as': False,
            'save_on_top': False,
            'has_delete_permission': True,
            'has_change_permission': True,
        }
        return render(request, 'admin/fechar_chamado.html', context)

    def fechar_chamado_link(self, obj):
        return format_html(
            '<a class="button" href="{}">Fechar</a>',
            reverse('admin:fechar_chamado', args=[obj.pk])
        )
    fechar_chamado_link.short_description = 'Fechar Chamado'