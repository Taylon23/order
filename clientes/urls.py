from django.urls import path
from . import views
from allauth.account.views import LoginView, LogoutView, SignupView

urlpatterns = [
    # URL para a página de login
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    # URL para a página de logout
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    # URL para a página de singup
    path('accounts/singup/', SignupView.as_view(), name='account_singup'),
    # URL para a página de cadastro
    path('add/clientes/', views.CreateClientesView.as_view(),
         name='adicionar-cliente'),
    path('atualizar/cliente/<int:pk>',
         views.UpdateClitenteView.as_view(), name='atualizar-cliente'),
    path('deletar/cliente/<int:pk>',
         views.DeleteCliente.as_view(), name='deletar-cliente'),
    path('tabela/clientes/', views.TabelaClientesView, name='tabela-clientes'),
    path('criar/produto/', views.CriarProdutoCreate.as_view(), name='criar-produto'),
    path('editar/produto/<int:pk>',
         views.EditarProdutoUpdate.as_view(), name='editar-produto'),
    path('deletar/produto/<int:pk>', views.DeletarProdutoDelete.as_view(),
         name='deletar-produto'),    path('perfil/cliente/<int:id>', views.PerfilClienteView, name='perfil-cliente'),
    path('criar/pedido/', views.CreatePedidoView.as_view(),
         name='criar-pedido'),
    path('atualizar/pedido/<int:pk>',
         views.UpdatePedidoView.as_view(), name='atualizar-pedido'),
    path('deletar/pedido/<int:pk>',
         views.DeletePedidoView.as_view(), name='deletar-pedido'),
    path('tabela/pedidos', views.TabelaPedidoView, name='tabela-pedido'),
    path(('add/item/'), views.CreateAdicionarProduto.as_view(),
         name='adicionar-produto'),
    path('pedido/<int:pedido_id>/itens/',
         views.ItensPedido, name='itens_pedido'),
    path('pedido/<int:pedido_id>/item/<int:item_id>/excluir/',
         views.excluir_item_pedido, name='excluir_item_pedido'),
]
