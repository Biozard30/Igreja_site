from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, MessageForm, UserProfileForm, UserProfileForm, NewsFeedForm, MinisterioForm
from django.http import JsonResponse, HttpResponseForbidden
import requests
from .models import User, Message, UserProfile, NewsFeed, Ministerio
from django.db import models  # Necessário para Q() nas consultas
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.timezone import now
from datetime import timedelta
from main.forms import PedidoOracaoForm  # Importe o formulário do app 'main'
from main.models import PedidoOracao  # Importe o modelo do app 'main'



User = get_user_model()

# AUTENTICAÇÃOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

# Verifica se o usuário é um admin
def is_admin(user):
    return user.is_superuser

# Página de cadastro
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redireciona para a página de login após o cadastro
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# Página de login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')  # Redireciona para a página inicial
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# View de Logout
def user_logout(request):
    logout(request)  # Desloga o usuário
    return redirect('login')  # Redireciona para a página de login

# Página de aprovação de usuários (somente para administradores)
@user_passes_test(is_admin)
def approve_users(request):
    # Lógica para listar usuários que aguardam aprovação
    users = User.objects.filter(is_approved=False)
    return render(request, 'users/approve_users.html', {'users': users})

# Aprovar usuário
@user_passes_test(is_admin)
def approve_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_approved = True
    user.save()
    return redirect('approve_users')

#APIiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii

def api_page(request):
    # Fazer uma requisição para a API que você criou
    url = 'http://127.0.0.1:8000/api/igrejas/'  # Altere a URL conforme a sua API
    response = requests.get(url)
    igrejas = response.json()  # Converte o retorno da API em formato JSON para dicionário Python
    return render(request, 'crudapi/api_page.html', {'igrejas': igrejas})

def culto_page(request):
    url = 'http://127.0.0.1:8000/api/cultos/'  # URL da sua API de Cultos
    response = requests.get(url)
    cultos = response.json()
    return render(request, 'crudapi/culto_page.html', {'cultos': cultos})

def pedido_oracao_page(request):
    url = 'http://127.0.0.1:8000/api/pedidos-oracao/'  # URL da API de Pedidos de Oração
    response = requests.get(url)
    pedidos_oracao = response.json()
    return render(request, 'crudapi/pedido_oracao_page.html', {'pedidos_oracao': pedidos_oracao})

def evento_page(request):
    url = 'http://127.0.0.1:8000/api/eventos/'  # URL da API de Eventos
    response = requests.get(url)
    eventos = response.json()
    return render(request, 'crudapi/evento_page.html', {'eventos': eventos})

def ministerio_page(request):
    url = 'http://127.0.0.1:8000/api/ministerios/'  # URL da API de Ministérios
    response = requests.get(url)
    ministerios = response.json()
    return render(request, 'crudapi/ministerio_page.html', {'ministerios': ministerios})

def noticia_page(request):
    url = 'http://127.0.0.1:8000/api/noticias/'  # URL da API de Notícias
    response = requests.get(url)
    noticias = response.json()
    return render(request, 'crudapi/noticia_page.html', {'noticias': noticias})

# PERMISSÕES E PÁGINASSSSSSSSSSS

@login_required
def mensagem(request):
    # Verifica se o usuário tem permissão para acessar
    if request.user.role not in ['membro', 'lider', 'pastor', 'admin']:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    
    # Filtra os usuários com quem o usuário logado tem conversas
    mensagens = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).values('sender', 'receiver').distinct()

    # Todos os usuários cadastrados (exceto o usuário logado)
    all_users = User.objects.exclude(id=request.user.id)

    # Usuários com quem o logado trocou mensagens
    users_with_messages = User.objects.filter(
        id__in=[msg['sender'] for msg in mensagens] +
               [msg['receiver'] for msg in mensagens]
    ).exclude(id=request.user.id)  # Exclui o usuário logado

    selected_user = None
    mensagens_conversacao = []

    # Se o usuário escolheu um destinatário (receiver) na URL
    if request.GET.get('user_id'):
        selected_user = User.objects.get(id=request.GET['user_id'])
        mensagens_conversacao = Message.objects.filter(
            Q(sender=request.user, receiver=selected_user) | Q(sender=selected_user, receiver=request.user)
        ).order_by('timestamp')

    # Quando o formulário for enviado
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # Recebe o receiver da URL ou da interação
            receiver_user = selected_user or User.objects.get(id=form.cleaned_data['receiver'])
            mensagem = form.save(commit=False)
            mensagem.sender = request.user  # O remetente é o usuário logado
            mensagem.receiver = receiver_user  # O receptor é o usuário selecionado
            mensagem.save()
            return redirect('mensagem')  # Após o envio, redireciona para a mesma página

    else:
        form = MessageForm()

    # Contexto para renderizar a página
    context = {
        'all_users': all_users,  # Todos os usuários cadastrados
        'users_with_messages': users_with_messages,  # Usuários com quem o logado trocou mensagens
        'mensagens': mensagens_conversacao,  # Mensagens trocadas com o usuário selecionado
        'form': form,
        'selected_user': selected_user,  # O usuário selecionado para ver as mensagens
    }

    return render(request, 'pag/mensagem.html', context)

@login_required
def ministerio(request):
    if request.user.role in ['membro', 'lider', 'pastor', 'admin']:
        if request.method == 'POST' and request.user.role in ['lider', 'pastor', 'admin']:
            form = MinisterioForm(request.POST)
            if form.is_valid():
                ministerio = form.save(commit=False)
                ministerio.author = request.user
                ministerio.save()
                return redirect('ministerio')
        else:
            form = MinisterioForm()

        # Filtrar informações recentes e públicas
        recent_ministerios = Ministerio.objects.filter(is_public=True).filter(created_at__gte=now() - timedelta(days=30))
        return render(request, 'pag/ministerio.html', {'form': form, 'ministerios': recent_ministerios})
    else:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")

@login_required
def feed(request):
    if request.user.role in ['membro', 'lider', 'pastor', 'admin']:
        if request.method == 'POST':
            form = NewsFeedForm(request.POST, request.FILES)
            if form.is_valid():
                news = form.save(commit=False)
                news.author = request.user
                news.save()
                return redirect('feed')
        else:
            form = NewsFeedForm()

        # Obter todas as notícias e configurar o paginador
        news_list = NewsFeed.objects.all()
        paginator = Paginator(news_list, 10)  # 10 notícias por página

        # Obter a página atual
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'pag/feed.html', {'form': form, 'page_obj': page_obj})
    else:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")

@login_required
def pedidos(request):
    if request.user.role in ['membro', 'lider', 'pastor', 'admin']:
        if request.method == 'POST':
            form = PedidoOracaoForm(request.POST)
            if form.is_valid():
                pedido = form.save(commit=False)
                pedido.nome = request.user.userprofile.nome  # Adicionando o nome automaticamente
                pedido.save()
                return redirect('pedidos')

        else:
            form = PedidoOracaoForm()

        pedidos_oracao = PedidoOracao.objects.all()

        return render(request, 'pag/pedidos.html', {'form': form, 'pedidos_oracao': pedidos_oracao})

    else:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")

@login_required
def perfil(request):
    user = request.user
    # Tenta obter o perfil do usuário ou cria um novo se não existir
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    if created:
        # Ação a ser tomada caso o perfil tenha sido criado
        print("Perfil criado para o usuário!")

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()  # Salva as alterações no perfil
            return redirect('perfil')  # Redireciona após salvar
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'pag/perfil.html', {'form': form, 'user_profile': user_profile})

@login_required
def lideres(request):
    if request.user.role in ['pastor', 'admin']:
        return render(request, 'pag/lideres.html')
    else:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")

@login_required
def pastor(request):
    if request.user.role == 'admin':
        return render(request, 'pag/pastor.html')
    else:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")

@login_required
def editar_site(request):
    if request.user.role == 'admin':
        return render(request, 'pag/editar_site.html')
    else:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")



# Cultos e Eventos
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .forms import CultoForm, EventoForm

# URL da API para cultos e eventos
CULTOS_API_URL = 'http://127.0.0.1:8000/api/cultos/'
EVENTOS_API_URL = 'http://127.0.0.1:8000/api/eventos/'

@login_required
def cultos_eventos(request):
    # Verificando permissões
    if request.user.role not in ['lider', 'pastor', 'admin']:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    
    # Recuperar os cultos e eventos da API
    cultos_response = requests.get(CULTOS_API_URL)
    eventos_response = requests.get(EVENTOS_API_URL)
    
    cultos = cultos_response.json() if cultos_response.status_code == 200 else []
    eventos = eventos_response.json() if eventos_response.status_code == 200 else []

    # Lidar com o envio de formulários de criação
    if request.method == 'POST':
        # Adicionar Culto
        if 'add_culto' in request.POST:
            culto_form = CultoForm(request.POST)
            if culto_form.is_valid():
                culto_form.save()
                messages.success(request, 'Culto adicionado com sucesso!')
                return redirect('cultos_eventos')
            else:
                messages.error(request, 'Erro ao adicionar culto!')

        # Adicionar Evento
        elif 'add_evento' in request.POST:
            evento_form = EventoForm(request.POST, request.FILES)
            if evento_form.is_valid():
                evento_form.save()
                messages.success(request, 'Evento adicionado com sucesso!')
                return redirect('cultos_eventos')
            else:
                messages.error(request, 'Erro ao adicionar evento!')

    else:
        culto_form = CultoForm()
        evento_form = EventoForm()

    return render(request, 'pag/cultos_eventos.html', {
        'cultos': cultos,
        'eventos': eventos,
        'culto_form': culto_form,
        'evento_form': evento_form
    })

# Função para editar culto
@login_required
def editar_culto(request, pk):
    culto = requests.get(f'{CULTOS_API_URL}{pk}/').json()  # Buscar culto pela PK
    if request.method == 'POST':
        data = {
            'tipo': request.POST['tipo'],
            'descricao': request.POST['descricao'],
            'horario': request.POST['horario'],
            'data': request.POST['data'],
        }
        response = requests.put(f'{CULTOS_API_URL}{pk}/', data=data)
        if response.status_code == 200:
            messages.success(request, 'Culto atualizado com sucesso!')
            return redirect('cultos_eventos')
        else:
            messages.error(request, 'Erro ao atualizar culto!')
    return render(request, 'pag/editar_culto.html', {'culto': culto})

# Função para editar evento
@login_required
def editar_evento(request, pk):
    evento = requests.get(f'{EVENTOS_API_URL}{pk}/').json()  # Buscar evento pela PK
    if request.method == 'POST':
        data = {
            'titulo': request.POST['titulo'],
            'texto': request.POST['texto'],
            'data': request.POST['data'],
        }
        files = {'foto': request.FILES['foto']} if 'foto' in request.FILES else {}
        response = requests.put(f'{EVENTOS_API_URL}{pk}/', data=data, files=files)
        if response.status_code == 200:
            messages.success(request, 'Evento atualizado com sucesso!')
            return redirect('cultos_eventos')
        else:
            messages.error(request, 'Erro ao atualizar evento!')
    return render(request, 'pag/editar_evento.html', {'evento': evento})

# Função para excluir culto
@login_required
def excluir_culto(request, pk):
    response = requests.delete(f'{CULTOS_API_URL}{pk}/')
    if response.status_code == 204:
        messages.success(request, 'Culto excluído com sucesso!')
    else:
        messages.error(request, 'Erro ao excluir culto!')
    return redirect('cultos_eventos')

# Função para excluir evento
@login_required
def excluir_evento(request, pk):
    response = requests.delete(f'{EVENTOS_API_URL}{pk}/')
    if response.status_code == 204:
        messages.success(request, 'Evento excluído com sucesso!')
    else:
        messages.error(request, 'Erro ao excluir evento!')
    return redirect('cultos_eventos')
