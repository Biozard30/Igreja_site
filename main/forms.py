from django import forms
from .models import PedidoOracao

class PedidoOracaoForm(forms.ModelForm):
    class Meta:
        model = PedidoOracao
        fields = ['nome', 'telefone', 'texto']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu telefone'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Seu pedido de oração', 'rows': 5}),
        }

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if not telefone.isdigit():
            raise forms.ValidationError("O telefone deve conter apenas números.")
        return telefone
