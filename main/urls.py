from django.urls import path
from .views import base
from . import views

urlpatterns = [
    
    #página dos pedidos de oração
    path('sucesso/', views.pedido_oracao_sucesso, name='pedido_oracao_sucesso'),
    
    #página base do site principal
    path('base/', base, name='base'),
    
    # página do calendário
    path('calendario/', views.calendario_view, name='calendario'), 
        
    # página das notícias
    path('noticia/<int:pk>/', views.noticia_detalhes, name='noticia_detalhes'),  # Detalhes da notícia
    
    path('', views.home_unificada, name='home'),
    
    # página dos ministérios
    path('ministerio/', views.ministerio_view, name='ministerio'),
    path('contato/', views.contato_view, name='contato'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IgrejaViewSet, CultoViewSet, PedidoOracaoViewSet, EventoViewSet, MinisterioViewSet, NoticiaViewSet

router = DefaultRouter()
router.register(r'igrejas', IgrejaViewSet)
router.register(r'cultos', CultoViewSet)
router.register(r'pedidos-oracao', PedidoOracaoViewSet)
router.register(r'eventos', EventoViewSet)
router.register(r'ministerios', MinisterioViewSet)
router.register(r'noticias', NoticiaViewSet)

urlpatterns += [
    path('api/', include(router.urls)),
]
