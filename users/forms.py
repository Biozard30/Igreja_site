from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Message, UserProfile, NewsFeed, Ministerio
from main.models import Culto, Evento

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_approved = False  # Usuário fica aguardando aprovação
        if commit:
            user.save()
        return user

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']  # Removemos 'receiver' porque ele será gerenciado pelo backend

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget = forms.Textarea(attrs={'placeholder': 'Digite sua mensagem...'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nome', 'phone', 'address', 'ministry', 'profile_picture']  # Incluir todos os campos desejados
    
    profile_picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

class NewsFeedForm(forms.ModelForm):
    class Meta:
        model = NewsFeed
        fields = ['title', 'content', 'image']
        labels = {
            'title': 'Título',
            'content': 'Conteúdo',
            'image': 'Imagem (opcional)',
        }

class MinisterioForm(forms.ModelForm):
    class Meta:
        model = Ministerio
        fields = ['title', 'content', 'is_public']
        labels = {
            'title': 'Título',
            'content': 'Descrição',
            'is_public': 'É público?',
        }

class CultoForm(forms.ModelForm):
    class Meta:
        model = Culto
        fields = ['tipo', 'descricao', 'horario', 'data']

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'data', 'texto', 'foto']
