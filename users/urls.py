from django.urls import path
from . import views

# AUTENTICAÇÃO
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('approve/', views.approve_users, name='approve_users'),
    path('approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('logout/', views.user_logout, name='logout'),
]

#API
urlpatterns += [
    path('api-page/', views.api_page, name='api_page'),
    path('culto-page/', views.culto_page, name='culto_page'),
    path('pedido-oracao-page/', views.pedido_oracao_page, name='pedido_oracao_page'),
    path('evento-page/', views.evento_page, name='evento_page'),
    path('ministerio-page/', views.ministerio_page, name='ministerio_page'),
    path('noticia-page/', views.noticia_page, name='noticia_page'),
]

# PÁGINAS COM PERMISSÕES
urlpatterns += [
    path('mensagem/', views.mensagem, name='mensagem'),
    path('feed/', views.feed, name='feed'),
    path('ministerio/', views.ministerio, name='ministerio'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('perfil/', views.perfil, name='perfil'),
    path('lideres/', views.lideres, name='lideres'),
    path('pastor/', views.pastor, name='pastor'),
    path('editar_site/', views.editar_site, name='editar_site'),
]

urlpatterns += [
    path('cultos_eventos/', views.cultos_eventos, name='cultos_eventos'),
    path('culto/editar/<int:pk>/', views.editar_culto, name='editar_culto'),
    path('evento/editar/<int:pk>/', views.editar_evento, name='editar_evento'),
    path('culto/excluir/<int:pk>/', views.excluir_culto, name='excluir_culto'),
    path('evento/excluir/<int:pk>/', views.excluir_evento, name='excluir_evento'),
]
