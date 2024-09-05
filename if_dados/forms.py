from django import forms
from .models import Chamado, Especialidade, Tecnico

# Formulário para Especialidade
class EspecialidadeForm(forms.ModelForm):
    class Meta:
        model = Especialidade
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulário para Técnico
class TecnicoForm(forms.ModelForm):
    class Meta:
        model = Tecnico
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidades': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

# Formulário para abrir Chamado
class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = [
            'departamento', 'sala', 'descricao_problema',
            'patrimonio', 'equipamento', 'especialidade'
        ]
        widgets = {
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'sala': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao_problema': forms.Textarea(attrs={'class': 'form-control'}),
            'patrimonio': forms.TextInput(attrs={'class': 'form-control'}),
            'equipamento': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidade': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

# Formulário para alterar Chamado
class ChamadoAlterarForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = [
            'status', 'departamento', 'sala', 'descricao_problema',
            'patrimonio', 'equipamento', 'especialidade'
        ]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'sala': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao_problema': forms.Textarea(attrs={'class': 'form-control'}),
            'patrimonio': forms.TextInput(attrs={'class': 'form-control'}),
            'equipamento': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidade': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

# Formulário para Fechar Chamado
class FecharChamadoForm(forms.ModelForm):
    tecnico = forms.ModelChoiceField(
        queryset=Tecnico.objects.all(),
        label='Técnico',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Chamado
        fields = ['relato_tecnico', 'tecnico']
        widgets = {
            'relato_tecnico': forms.Textarea(attrs={'class': 'form-control'}),
        }

# Formulário para Reabrir Chamado
class ReabrirChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['descricao_problema']
        widgets = {
            'descricao_problema': forms.Textarea(attrs={'class': 'form-control'}),
        }
