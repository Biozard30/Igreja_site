from django.shortcuts import render, redirect, get_object_or_404
from .forms import PedidoOracaoForm
from .models import Evento, Culto, Noticia, Ministerio, Contato
import calendar
from datetime import datetime, timedelta
from django.utils import timezone

def pedido_oracao_sucesso(request):
    return render(request, 'main/pedido_oracao_sucesso.html')

def base(request):
    return render(request, 'main/base.html')

def noticia_detalhes(request, pk):
    # Pega a notícia com a chave primária fornecida, ou retorna um erro 404 se não encontrada
    noticia = get_object_or_404(Noticia, pk=pk)
    return render(request, 'main/noticia_detalhes.html', {'noticia': noticia})

def calendario_view(request):
    # Defina o mês e ano para o calendário
    hoje = datetime.today()
    ano = hoje.year
    mes = hoje.month
    
    # Calcule o primeiro e o último dia do mês
    primeiro_dia_mes = datetime(ano, mes, 1)
    
    # Ajuste para o próximo mês (com verificação para não ultrapassar dezembro)
    if mes == 12:
        ultimo_dia_mes = datetime(ano + 1, 1, 1) - timedelta(days=1)
    else:
        ultimo_dia_mes = datetime(ano, mes + 1, 1) - timedelta(days=1)
    
    # Pegue todos os eventos e cultos que ocorrem no mês
    eventos = Evento.objects.filter(data__month=mes, data__year=ano)
    cultos = Culto.objects.filter(data__month=mes, data__year=ano)

    # Prepare o calendário
    cal = calendar.Calendar(firstweekday=6)  # Inicia o calendário no domingo
    dias_do_mes = cal.monthdays2calendar(ano, mes)  # Retorna as semanas do mês
    
    # Crie listas com as datas dos eventos e cultos
    eventos_dates = [evento.data.strftime('%Y-%m-%d') for evento in eventos]
    cultos_dates = [culto.data.strftime('%Y-%m-%d') for culto in cultos]

    contexto = {
        'ano': ano,
        'mes': mes,
        'dias_do_mes': dias_do_mes,
        'eventos': eventos,
        'cultos': cultos,
        'eventos_dates': eventos_dates,
        'cultos_dates': cultos_dates,
    }
    return render(request, 'main/calendario.html', contexto)

def home_unificada(request):
    # Dados para a seção de cultos
    hoje = timezone.now().date()
    culto_hoje = Culto.objects.filter(data=hoje).first()
    
    if not culto_hoje:
        culto_proximo = Culto.objects.filter(data__gt=hoje).order_by('data').first()
        if not culto_proximo:
            final_do_mes = hoje.replace(day=28) + timedelta(days=4)
            final_do_mes = final_do_mes.replace(day=1) - timedelta(days=1)
            culto_proximo = Culto.objects.filter(data__lte=final_do_mes).first()
            if culto_proximo and culto_proximo.data <= hoje:
                culto_proximo = None
    else:
        culto_proximo = None

    # Dados para a seção de notícias
    noticias = Noticia.objects.all().order_by('-data_publicacao')[:5]
    
    # Dados para a seção de pedidos de oração
    if request.method == 'POST':
        form = PedidoOracaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedido_oracao_sucesso')  # Redireciona após o envio
    else:
        form = PedidoOracaoForm()
    
    # Renderizando o template com os dados consolidados
    return render(request, 'main/home.html', {
        'culto_hoje': culto_hoje,
        'culto_proximo': culto_proximo,
        'noticias': noticias,
        'form': form,
        'hoje': hoje,
    })

def ministerio_view(request):
    # Pegando o primeiro ministério da base de dados
    ministerio = Ministerio.objects.first()  # Ou use um filtro para pegar o ministério desejado
    return render(request, 'paginas/ministerio.html', {'ministerio': ministerio})

def contato_view(request):
    # Pegando o primeiro ministério da base de dados
    contato = Contato.objects.first()  # Ou use um filtro para pegar o ministério desejado
    return render(request, 'paginas/contato.html', {'contato': contato})

#APIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated  # Importando a permissão
from .models import Igreja, Culto, PedidoOracao, Evento, Ministerio, Noticia
from .serializers import IgrejaSerializer, CultoSerializer, PedidoOracaoSerializer, EventoSerializer, MinisterioSerializer, NoticiaSerializer

class IgrejaViewSet(viewsets.ModelViewSet):
    queryset = Igreja.objects.all()
    serializer_class = IgrejaSerializer
    permission_classes = [IsAuthenticated]  # Requer autenticação

class CultoViewSet(viewsets.ModelViewSet):
    queryset = Culto.objects.all()
    serializer_class = CultoSerializer
    permission_classes = [IsAuthenticated]  # Requer autenticação

class PedidoOracaoViewSet(viewsets.ModelViewSet):
    queryset = PedidoOracao.objects.all()
    serializer_class = PedidoOracaoSerializer
    permission_classes = [IsAuthenticated]  # Requer autenticação

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]  # Requer autenticação

class MinisterioViewSet(viewsets.ModelViewSet):
    queryset = Ministerio.objects.all()
    serializer_class = MinisterioSerializer
    permission_classes = [IsAuthenticated]  # Requer autenticação

class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer
    permission_classes = [IsAuthenticated]  # Requer autenticação
