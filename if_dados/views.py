from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Chamado, HistoricoChamado, Tecnico
from .forms import ChamadoForm, ChamadoAlterarForm, FecharChamadoForm, ReabrirChamadoForm

@login_required
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

@login_required
def chamado_enviado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    return render(request, 'chamado_enviado.html', {'chamado': chamado})

@login_required
def detalhes_do_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    tecnico = get_object_or_404(Tecnico, user=request.user)

    if chamado.tecnico and chamado.tecnico != tecnico:
        messages.error(request, 'Você não tem permissão para visualizar este chamado.')
        return redirect('listar_chamados_disponiveis')

    if request.method == 'POST':
        form = ChamadoAlterarForm(request.POST, instance=chamado)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.data_modificacao = timezone.now()
            if chamado.status == Chamado.Status.FECHADO:
                chamado.marcar_como_concluido()
            chamado.save()
            return redirect('detalhes_do_chamado', id=id)
    else:
        form = ChamadoAlterarForm(instance=chamado)

    context = {
        'form': form,
        'chamado': chamado,
        'mostrar_botao_reabrir': chamado.status == Chamado.Status.FECHADO,
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
    
    if request.method == 'POST':
        form = FecharChamadoForm(request.POST)
        if form.is_valid():
            chamado.status = Chamado.Status.FECHADO
            chamado.data_fechamento = timezone.now()
            chamado.relato_tecnico = form.cleaned_data.get('relato_tecnico', '')

            tecnico = form.cleaned_data.get('tecnico')  # Obtém o técnico selecionado

            # Criar um registro no histórico de chamados
            HistoricoChamado.objects.create(
                chamado=chamado,
                data_fechamento=chamado.data_fechamento,
                status=Chamado.Status.FECHADO,
                relatorio=chamado.relato_tecnico,
                tecnico=tecnico  # Passa o técnico selecionado
            )

            chamado.save()

            messages.success(request, 'Chamado fechado com sucesso!')
            return redirect('admin:if_dados_chamado_changelist')
    else:
        form = FecharChamadoForm()

    context = {
        'form': form,
        'chamado': chamado,
    }
    return render(request, 'admin/fechar_chamado.html', context)

@login_required
def listar_chamados_disponiveis(request):
    try:
        tecnico = get_object_or_404(Tecnico, user=request.user)
    except Http404:
        messages.error(request, 'Você não tem um técnico associado. Entre em contato com o administrador.')
        return redirect('chamados')  # Redireciona para a URL nomeada 'chamados'

    especialidades = tecnico.especialidades.all()
    
    status_filtro = request.GET.get('status')
    if status_filtro:
        chamados = Chamado.objects.filter(
            status=status_filtro,
            especialidade__in=especialidades,
            tecnico__isnull=True
        )
    else:
        chamados = Chamado.objects.filter(
            especialidade__in=especialidades,
            tecnico__isnull=True
        )
    
    return render(request, 'listar_chamados_disponiveis.html', {'chamados': chamados, 'tecnico': tecnico})

@login_required
def assumir_chamado(request, chamado_id):
    tecnico = get_object_or_404(Tecnico, user=request.user)
    chamado = get_object_or_404(Chamado, id=chamado_id)

    if not set(chamado.equipamento.especialidades_requeridas.all()).intersection(tecnico.especialidades.all()):
        messages.error(request, 'Você não tem a especialidade necessária para este chamado.')
        return redirect('listar_chamados_disponiveis')

    chamado.tecnico = tecnico
    chamado.save()
    messages.success(request, f'Você agora é responsável pelo chamado {chamado.id}.')
    return redirect('detalhes_do_chamado', id=chamado.id)

# View para reabrir o chamado
@login_required
def reabrir_chamado(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    if request.method == 'POST':
        chamado.reabrir()
        messages.success(request, 'Chamado reaberto com sucesso!')
        return redirect('meus_chamados')
    return render(request, 'reabrir_chamado.html', {'chamado': chamado})


@login_required
def chamado_reaberto(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    return render(request, 'chamado_reaberto.html', {'chamado': chamado})

@login_required
def submit_chamado(request):
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

@login_required
def meus_chamados(request):
    chamados = Chamado.objects.filter(usuario=request.user).order_by('-data_abertura')
    return render(request, 'meus-chamados.html', {'chamados': chamados})

@login_required
def detalhes_do_chamado_aberto(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    contexto = {
        'chamado': chamado,
        'usuario_email': request.user.email 
    }
    return render(request, 'detalhes-do-chamado-aberto.html', contexto)

@login_required
def detalhes_do_chamado_fechado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    contexto = {
        'chamado': chamado,
        'usuario_email': request.user.email 
    }
    return render(request, 'detalhes-do-chamado-fechado.html', contexto)
