from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta



class User(AbstractUser):
    ROLE_CHOICES = (
        ('membro', 'Membro'),
        ('lider', 'Líder'),
        ('pastor', 'Pastor'),
        ('admin', 'Administrador'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='membro')
    is_approved = models.BooleanField(default=False)  # Para saber se foi aprovado pelo admin
    
    # Modificando os relacionamentos para evitar conflitos
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='user_set_custom',  # Renomeando o relacionamento reverso
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='user_permissions_set_custom',  # Renomeando o relacionamento reverso
        blank=True
    )

    def __str__(self):
        return self.username

#MENSAGENSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'Mensagem de {self.sender} para {self.receiver} - {self.timestamp.strftime("%d/%m/%Y %H:%M:%S")}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    ministry = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Foto de perfil

    def __str__(self):
        return self.nome if self.nome else self.user.username

class NewsFeed(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    content = models.TextField(max_length=1000, verbose_name="Conteúdo")
    image = models.ImageField(upload_to='feed_images/', blank=True, null=True, verbose_name="Imagem")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Autor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Ministerio(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    content = models.TextField(max_length=1000, verbose_name="Descrição")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Autor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    is_public = models.BooleanField(default=True, verbose_name="É público?")  # Configuração de privacidade

    class Meta:
        verbose_name = "Ministério"
        verbose_name_plural = "Ministérios"
        ordering = ['-created_at']

    def is_recent(self):
        """Verifica se a notícia é recente (últimos 30 dias)."""
        return self.created_at >= now() - timedelta(days=30)

    def __str__(self):
        return self.title
