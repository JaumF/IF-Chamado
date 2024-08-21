from django import forms
from django_select2.forms import Select2MultipleWidget, Select2Widget
from .models import Chamado, Especialidade

class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['status', 'usuario', 'departamento', 'sala', 'descricao_problema', 'patrimonio', 'data_abertura', 'data_fechamento', 'data_modificacao', 'data_reabertura', 'especialidade', 'relato_tecnico']
        widgets = {
            'descricao_problema': forms.Textarea(attrs={'rows': 5}),
            'data_abertura': forms.DateInput(attrs={'type': 'date'}),
            'data_fechamento': forms.DateInput(attrs={'type': 'date'}),
            'data_modificacao': forms.DateInput(attrs={'type': 'date'}),
            'data_reabertura': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remova a linha referente ao queryset do equipamento
        # self.fields['equipamento'].queryset = Equipamento.objects.all()
        self.fields['especialidade'].widget = forms.CheckboxSelectMultiple()
        self.fields['especialidade'].queryset = Especialidade.objects.all()

class ChamadoAlterarForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = [
            'departamento', 
            'sala', 
            'descricao_problema', 
            'patrimonio', 
        ]
        widgets = {
            'data_abertura': forms.HiddenInput(),
            'data_fechamento': forms.HiddenInput(),
            'data_modificacao': forms.HiddenInput(),
            'data_reabertura': forms.HiddenInput(),
            'especialidade': Select2Widget(attrs={'style': 'width: 300px;'}),  # Ajuste a largura aqui
        }

class FecharChamadoForm(forms.Form):
    relato_tecnico = forms.CharField(widget=forms.Textarea, required=True)

    def clean(self):
        cleaned_data = super().clean()
        relato_tecnico = cleaned_data.get("relato_tecnico")

        if not relato_tecnico:
            raise forms.ValidationError("O relatório técnico é obrigatório para fechar o chamado.")

        return cleaned_data
