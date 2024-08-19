from django import forms
from .models import Chamado, Especialidade

class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = [
            'departamento',
            'sala',
            'descricao_problema',
            'patrimonio',
            'equipamento',
            'especialidade'
        ]
        widgets = {
            'data_abertura': forms.HiddenInput(),
            'data_fechamento': forms.HiddenInput(),
            'data_modificacao': forms.HiddenInput(),
            'data_reabertura': forms.HiddenInput(),
            'especialidade': forms.Select(attrs={'style': 'width: 300px;'}),
        }

class ChamadoAlterarForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = [
            'departamento', 
            'sala', 
            'equipamento', 
            'descricao_problema', 
            'patrimonio', 
            'relato_tecnico'
        ]
        widgets = {
            'data_abertura': forms.HiddenInput(),  
            'data_fechamento': forms.HiddenInput(),
            'data_modificacao': forms.HiddenInput(),
            'data_reabertura': forms.HiddenInput(),
            'especialidade': forms.Select(attrs={'style': 'width: 2000%;'}),
        }

class FecharChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['relato_tecnico', 'tecnico']  # Adicione o campo tecnico

    def clean(self):
        cleaned_data = super().clean()
        relato_tecnico = cleaned_data.get("relato_tecnico")
        tecnico = cleaned_data.get("tecnico")

        if not relato_tecnico:
            raise forms.ValidationError("O relatório técnico é obrigatório para fechar o chamado.")
        
        if not tecnico:
            raise forms.ValidationError("O técnico é obrigatório para fechar o chamado.")

        return cleaned_data


class PedidoReaberturaForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['descricao_problema']
        widgets = {
            'data_abertura': forms.HiddenInput(),  
            'data_fechamento': forms.HiddenInput(),
            'data_modificacao': forms.HiddenInput(),
            'data_reabertura': forms.HiddenInput(),
        }

class RelatorioReaberturaForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['descricao_problema']
        widgets = {
            'data_abertura': forms.HiddenInput(),  
            'data_fechamento': forms.HiddenInput(),
            'data_modificacao': forms.HiddenInput(),
            'data_reabertura': forms.HiddenInput(),
        }