from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Chamado, Tecnico
from .forms import ChamadoForm, ChamadoAlterarForm, FecharChamadoForm

def abrir_chamado(request):
    if request.method == 'POST':
        form = ChamadoForm(request.POST)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.usuario = request.user  # Associe o usuário atual
            chamado.save()
            return redirect('chamado_enviado', chamado_id=chamado.id)
    else:
        form = ChamadoForm()
    return render(request, 'abrir_chamado.html', {'form': form})

def chamado_enviado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    return render(request, 'chamado_enviado.html', {'chamado': chamado})

@login_required
def detalhes_do_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    tecnico = get_object_or_404(Tecnico, user=request.user)

    # Verifique se o técnico é responsável pelo chamado ou se o chamado é do técnico
    if chamado.tecnico and chamado.tecnico != tecnico:
        messages.error(request, 'Você não tem permissão para visualizar este chamado.')
        return redirect('listar_chamados_disponiveis')

    if request.method == 'POST':
        form = ChamadoAlterarForm(request.POST, instance=chamado)
        if form.is_valid():
            chamado = form.save(commit=False)
            if chamado.status == Chamado.Status.FECHADO:
                chamado.marcar_como_concluido()
            chamado.save()
            return redirect('detalhes_do_chamado', id=id)
    else:
        form = ChamadoAlterarForm(instance=chamado)

    context = {
        'form': form,
        'chamado': chamado,
    }
    return render(request, 'detalhes_do_chamado.html', context)

@login_required
def atualizar_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    if request.method == 'POST':
        form = ChamadoAlterarForm(request.POST, instance=chamado)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.tecnico = request.user.tecnico  # Associe o técnico atual
            if chamado.status == Chamado.Status.FECHADO:
                chamado.marcar_como_concluido()
            chamado.save()
            return redirect('detalhes_do_chamado', id=id)
    else:
        form = ChamadoAlterarForm(instance=chamado)
    return render(request, 'atualizar_chamado.html', {'form': form, 'chamado': chamado})

@login_required
def fechar_chamado_view(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    tecnico = get_object_or_404(Tecnico, user=request.user)

    # Verifique se o técnico pode fechar o chamado
    if chamado.tecnico != tecnico:
        messages.error(request, 'Você não tem permissão para fechar este chamado.')
        return redirect('detalhes_do_chamado', id=chamado_id)

    if request.method == 'POST':
        form = FecharChamadoForm(request.POST, instance=chamado)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.status = Chamado.Status.FECHADO
            chamado.data_fechamento = timezone.now()
            chamado.tecnico = tecnico  # Atribua o técnico ao chamado
            chamado.save()
            messages.success(request, 'Chamado fechado com sucesso!')
            return redirect('admin:integrador_chamado_changelist')
    else:
        form = FecharChamadoForm(instance=chamado)

    context = {
        'form': form,
        'chamado': chamado,
        'opts': Chamado._meta,
        'change': True,
        'is_popup': False,
        'save_as': False,
        'save_on_top': False,
        'has_delete_permission': request.user.has_perm('integrador.delete_chamado'),
        'has_change_permission': request.user.has_perm('integrador.change_chamado'),
    }
    return render(request, 'admin/fechar_chamado.html', context)


@login_required
def listar_chamados_disponiveis(request):
    tecnico = get_object_or_404(Tecnico, user=request.user)
    especialidades = tecnico.especialidade.all()
    chamados = Chamado.objects.filter(equipamento__especialidade__in=especialidades, tecnico__isnull=True)
    return render(request, 'listar_chamados_disponiveis.html', {'chamados': chamados, 'tecnico': tecnico})

@login_required
def assumir_chamado(request, chamado_id):
    tecnico = get_object_or_404(Tecnico, user=request.user)
    chamado = get_object_or_404(Chamado, id=chamado_id)

    # Verifique se o chamado corresponde a uma das especialidades do técnico
    if chamado.equipamento.especialidade not in tecnico.especialidade.all():
        messages.error(request, 'Você não tem a especialidade necessária para este chamado.')
        return redirect('listar_chamados_disponiveis')

    # Associe o técnico ao chamado
    chamado.tecnico = tecnico
    chamado.save()
    messages.success(request, f'Você agora é responsável pelo chamado {chamado.id}.')
    return redirect('detalhes_do_chamado', id=chamado.id)