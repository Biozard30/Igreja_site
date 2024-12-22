from rest_framework import serializers
from .models import Igreja, Culto, PedidoOracao, Evento, Ministerio, Noticia

class IgrejaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Igreja
        fields = ['id', 'nome', 'rua', 'numero', 'bairro', 'cidade', 'cep', 'estado', 'pais', 'ministerios', 'lideres', 'membros', 'pastor', 'pedidos_oracao', 'noticias', 'cultos', 'eventos']

class CultoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culto
        fields = ['id', 'tipo', 'descricao', 'horario', 'data']

class PedidoOracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoOracao
        fields = ['id', 'nome', 'telefone', 'texto', 'data']

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ['id', 'titulo', 'data', 'texto', 'foto', 'criado_em']

class MinisterioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ministerio
        fields = ['id', 'nome', 'foto', 'descricao', 'membros']

class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = ['id', 'titulo', 'subtitulo', 'imagem', 'conteudo', 'data_publicacao']

