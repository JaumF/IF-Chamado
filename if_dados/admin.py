from django.utils import timezone
from django.urls import path, reverse
from django import forms
from django.contrib import admin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import format_html
from django_select2.forms import Select2MultipleWidget
from .models import Chamado, Especialidade, Tecnico, HistoricoChamado
from .forms import ChamadoForm, FecharChamadoForm

@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'telefone', 'get_especialidades')
    search_fields = ('nome', 'email')

    def get_especialidades(self, obj):
        return ", ".join([especialidade.nome for especialidade in obj.especialidades.all()])
    get_especialidades.short_description = 'Especialidades'

@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'departamento', 'sala', 'descricao_problema', 'patrimonio', 'data_abertura', 'status', 'usuario_email', 'action_buttons'
    )
    list_filter = ('status', 'departamento', 'especialidade')
    search_fields = ('departamento', 'sala', 'descricao_problema', 'patrimonio', 'usuario__email')
    readonly_fields = ('data_abertura', 'data_fechamento', 'data_modificacao', 'data_reabertura', 'especialidade')
    fields = (
        'departamento', 'sala', 'descricao_problema', 'patrimonio', 'status',
        'data_abertura', 'data_fechamento', 'data_modificacao', 'data_reabertura', 'especialidade', 'relato_tecnico', 'usuario'
    )
    form = ChamadoForm 

    def usuario_email(self, obj):
        return obj.usuario.email
    usuario_email.short_description = 'Email do Usuário'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'chamado/<int:chamado_id>/fechar/',
                self.admin_site.admin_view(self.fechar_chamado_view),
                name='fechar_chamado',
            ),
            path(
                'chamado/<int:chamado_id>/reabrir/',
                self.admin_site.admin_view(self.reabrir_chamado_view),
                name='reabrir_chamado',
            ),
            path(
                'especialidade/<int:especialidade_id>/relacionados/',
                self.admin_site.admin_view(self.chamados_relacionados_view),
                name='chamados_relacionados',
            ),
        ]
        return custom_urls + urls

    def fechar_chamado_view(self, request, chamado_id):
        chamado = get_object_or_404(Chamado, id=chamado_id)
        if request.method == 'POST':
            form = FecharChamadoForm(request.POST)
            if form.is_valid():
                chamado.status = Chamado.Status.FECHADO
                chamado.data_fechamento = timezone.now()
                chamado.relato_tecnico = form.cleaned_data.get('relato_tecnico', '')
                chamado.save()

                # Criar um registro no histórico de chamados
                HistoricoChamado.objects.create(
                    chamado=chamado,
                    data_fechamento=chamado.data_fechamento,
                    status=Chamado.Status.FECHADO,
                    relatorio=chamado.relato_tecnico
                )

                self.message_user(request, 'Chamado fechado com sucesso!')
                return redirect('admin:if_dados_chamado_changelist')
        else:
            form = FecharChamadoForm()

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

    def reabrir_chamado_view(self, request, chamado_id):
        chamado = get_object_or_404(Chamado, id=chamado_id)
        if request.method == 'POST':
            chamado.status = Chamado.Status.ABERTO
            chamado.data_fechamento = None
            chamado.save()

            self.message_user(request, 'Chamado reaberto com sucesso!')
            return redirect('admin:if_dados_chamado_changelist')
        else:
            # Aqui não há formulário específico para reabrir chamado
            pass

        context = {
            'chamado': chamado,
            'opts': self.model._meta,
            'change': True,
            'is_popup': False,
            'save_as': False,
            'save_on_top': False,
            'has_delete_permission': True,
            'has_change_permission': True,
        }
        return render(request, 'admin/reabrir_chamado.html', context)

    def chamados_relacionados_view(self, request, especialidade_id):
        especialidade = get_object_or_404(Especialidade, id=especialidade_id)
        chamados = Chamado.objects.filter(especialidade=especialidade)
        context = {
            'especialidade': especialidade,
            'chamados': chamados,
        }
        return render(request, 'admin/chamados_relacionados.html', context)

    def action_buttons(self, obj):
        if obj.status == Chamado.Status.FECHADO:
            return format_html(
                '<a class="button" href="{}">Reabrir Chamado</a>',
                reverse('admin:reabrir_chamado', args=[obj.id])
            )
        return format_html(
            '<a class="button" href="{}">Fechar Chamado</a>',
            reverse('admin:fechar_chamado', args=[obj.id])
        )
    action_buttons.short_description = 'Ações'


@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

@admin.register(HistoricoChamado)
class HistoricoChamadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'chamado', 'data_fechamento', 'status', 'tecnico')
    list_filter = ('status', 'data_fechamento', 'tecnico')
    search_fields = ('chamado__id', 'tecnico__nome', 'status')
