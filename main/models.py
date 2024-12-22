from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.conf import settings


class Igreja(models.Model):
    nome = models.CharField(max_length=100)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    cep = models.CharField(max_length=20)
    estado = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    ministerios = models.ManyToManyField('Ministerio')
    
    lideres = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lideres_igreja', null=True, blank=True)
    membros = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='membros_igreja', null=True, blank=True)
    pastor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pastor_igreja', null=True, blank=True)
    
    pedidos_oracao = models.ManyToManyField('PedidoOracao', blank=True)
    noticias = models.ManyToManyField('Noticia', blank=True)
    cultos = models.ManyToManyField('Culto', blank=True)
    eventos = models.ManyToManyField('Evento', blank=True)

    def __str__(self):
        return self.nome

class Culto(models.Model):
    tipo = models.CharField(max_length=100)
    descricao = models.TextField()
    horario = models.TimeField()  # Pode mudar para DateTimeField, se necessário
    data = models.DateField()

    def dia_da_semana(self):
        # Método simplificado
        dias = {
            'Monday': 'Segunda-feira',
            'Tuesday': 'Terça-feira',
            'Wednesday': 'Quarta-feira',
            'Thursday': 'Quinta-feira',
            'Friday': 'Sexta-feira',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo',
        }
        # Retorna o nome do dia da semana de forma traduzida
        return dias[self.data.strftime('%A')]

    def __str__(self):
        return f"{self.tipo} - {self.data} às {self.horario}"  # Exibe o horário no __str__

class PedidoOracao(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    texto = models.TextField()
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    data = models.DateField()
    texto = models.TextField()
    foto = models.ImageField(upload_to='eventos/')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Ministerio(models.Model):
    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='ministerios/')
    descricao = models.TextField()
    membros = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='ministerios')

    def __str__(self):
        return self.nome

class Noticia(models.Model):
    titulo = models.CharField(max_length=200, default="Titulo padrão")  # Valor padrão para título
    subtitulo = models.CharField(max_length=300, default="Subtítulo padrão")  # Valor padrão para subtítulo
    imagem = models.ImageField(upload_to='noticias/', default="noticias/default.jpg")  # Valor padrão para imagem (imagem de placeholder)
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(default=now)  # Valor padrão para data de publicação (data atual)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('noticia_detalhes', args=[str(self.id)])

class Contato(models.Model):
    telefone = models.CharField(max_length=100)
    descricao = models.TextField()
    
    def __str__(self):
        return self.nome
