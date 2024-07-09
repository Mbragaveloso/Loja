from django.urls import path
from .views import ListaProdutos, DetalheProduto, AdicionarAoCarrinho, RemoverDoCarrinho, CarrinhoView, ResumoDaCompra

app_name = 'produto'

urlpatterns = [
    path('', ListaProdutos.as_view(), name='lista'),
    path('adicionar/<int:produto_id>/', AdicionarAoCarrinho.as_view(), name='adicionar_ao_carrinho'),
    path('remover/<int:variacao_id>/', RemoverDoCarrinho.as_view(), name='remover_do_carrinho'),  # Corrigido aqui
    path('carrinho/', CarrinhoView.as_view(), name='carrinho'),
    path('resumodacompra/', ResumoDaCompra.as_view(), name='resumodacompra'),  # Corrigido para 'resumodacompra'
    path('finalizar-compra/', FinalizarCompra.as_view(), name='finalizar_compra'),  # URL para finalização da compra
    path('<slug:slug>/', DetalheProduto.as_view(), name='detalhe'),  # Movido para o final
]