from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.contrib import messages
from .models import Produto, Variacao
from django.contrib.auth.models import User
from .models import Produto, Variacao, Carrinho, ItemCarrinho
from .models import Carrinho, Pedido, ItemPedido
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class ListaProdutos(ListView):
    model = Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'

class DetalheProduto(DetailView):
    model = Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AdicionarAoCarrinho(View):
    def post(self, request, produto_id):
        produto = get_object_or_404(Produto, id=produto_id)
        variacao_id = request.POST.get('variacao_id')
        tamanho = request.POST.get('tamanho')

        if not tamanho:
            messages.error(request, "Por favor, selecione um tamanho.")
            return redirect('produto:detalhe', slug=produto.slug)
        
        variacao = get_object_or_404(Variacao, id=variacao_id)
        
        carrinho = request.session.get('carrinho', {})
        item_id = f"{variacao_id}-{tamanho}"
        
        if item_id in carrinho:
            carrinho[item_id]['quantidade'] += 1
        else:
            carrinho[item_id] = {
                'produto_nome': produto.nome,
                'variacao_nome': variacao.nome,
                'quantidade': 1,
                'preco_unitario': str(variacao.preco_marketing),
                'preco_unitario_promocional': str(variacao.preco_marketing_promocional) if variacao.preco_marketing_promocional else None,
                'slug': produto.slug,
                'imagem': produto.imagem.url if produto.imagem else None,
                'variacao_id': variacao_id,
                'tamanho': tamanho
            }
        
        request.session['carrinho'] = carrinho
        return redirect('produto:carrinho')

class RemoverDoCarrinho(View):
    def post(self, request, variacao_id):
        carrinho = request.session.get('carrinho', {})
        tamanho = request.POST.get('tamanho')
        item_id = f"{variacao_id}-{tamanho}"
        
        if item_id in carrinho:
            del carrinho[item_id]
            request.session['carrinho'] = carrinho
            messages.success(request, "O item foi removido do carrinho.")
        
        return redirect('produto:carrinho')

class CarrinhoView(View):
    def get(self, request, *args, **kwargs):
        carrinho = request.session.get('carrinho', {})
        total = sum(item['quantidade'] * float(item.get('preco_unitario_promocional', item['preco_unitario'])) for item in carrinho.values())
        context = {
            'carrinho': carrinho,
            'total': total,
        }
        return render(request, 'produto/carrinho.html', context)

class ResumoDaCompra(View):
    template_name = 'produto/resumodacompra.html'

    def get(self, request, *args, **kwargs):
        carrinho = request.session.get('carrinho', {})
        
        produtos_no_carrinho = []
        total = 0

        for item_id, detalhes_produto in carrinho.items():
            nome_produto = detalhes_produto['produto_nome']
            preco_unitario_promocional = detalhes_produto.get('preco_unitario_promocional')
            preco_unitario = float(preco_unitario_promocional) if preco_unitario_promocional else float(detalhes_produto['preco_unitario'])
            quantidade = detalhes_produto['quantidade']
            subtotal = preco_unitario * quantidade
            total += subtotal

            produtos_no_carrinho.append({
                'produto_nome': nome_produto,
                'preco_unitario': preco_unitario,
                'quantidade': quantidade,
                'subtotal': subtotal,
            })
        context = {
            'produtos': produtos_no_carrinho,
            'total': total,
        }

        return render(request, self.template_name, context)
           
class PedidoConfirmado(View):
    def get(self, request, *args, **kwargs):
        pedido = Pedido.objects.filter(usuario=request.user).order_by('-criado_em').first()
        if not pedido:
            return redirect('produto:lista')  # Redireciona para a lista de produtos se não encontrar um pedido

        context = {
            'pedido': pedido,
        }
        return render(request, 'produto/pedidoconfirmado.html', context)
    
def view_de_erro(request):
    return render(request, 'produto/erro.html')

lass FinalizarCompra(View):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                # Todo o código de criação de pedido, itens de pedido e atualização de estoque aqui
                # Isso garante que todas as operações sejam tratadas atomicamente
        except Exception as e:
            messages.error(request, "Ocorreu um erro ao finalizar a compra.")
            return redirect('produto:carrinho')