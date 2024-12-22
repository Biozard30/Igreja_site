from django.contrib import admin
from .models import Igreja, Culto, PedidoOracao, Evento, Noticia, Ministerio, Noticia

@admin.register(Igreja)
class IgrejaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'estado', 'pais')
    search_fields = ('nome', 'cidade', 'estado', 'pais')
    list_filter = ('estado', 'pais')

@admin.register(Culto)
class CultoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'data', 'horario', 'dia_da_semana')
    search_fields = ('tipo',)
    list_filter = ('data',)

@admin.register(PedidoOracao)
class PedidoOracaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'data')
    search_fields = ('nome', 'telefone')
    list_filter = ('data',)

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data', 'criado_em')
    search_fields = ('titulo',)
    list_filter = ('data', 'criado_em')

@admin.register(Ministerio)
class MinisterioAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_publicacao')
    list_filter = ('data_publicacao',)
    search_fields = ('titulo', 'subtitulo', 'conteudo')
    ordering = ('-data_publicacao',)
