from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from .models import Produto, Variacao
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
    
class FinalizarCompra(View):
    def post(self, request, *args, **kwargs):
        # Implemente aqui a lógica para finalização da compra
        # Por exemplo, criar um pedido, atualizar estoques, etc.

        # Após finalizar, você pode redirecionar para uma página de confirmação, por exemplo:
        return redirect('produto:pedidoconfirmado')  # Defina a URL correta para a página de confirmação
    
class PedidoConfirmado(View):
    def get(self, request, *args, **kwargs):
        pedido = Pedido.objects.filter(usuario=request.user).order_by('-criado_em').first()
        if not pedido:
            return redirect('produto:lista')  # Redireciona para a lista de produtos se não encontrar um pedido

        context = {
            'pedido': pedido,
        }
        return render(request, 'produto/pedidoconfirmado.html', context)
    
class FinalizarCompra(View):
    def post(self, request, *args, **kwargs):
        try:
            carrinho = Carrinho.objects.get(usuario=request.user, ativo=True)
        except Carrinho.DoesNotExist:
            messages.error(request, "Seu carrinho está vazio.")
            return redirect('produto:carrinho')

        total = carrinho.get_total()

        # Criação do pedido
        pedido = Pedido.objects.create(
            usuario=request.user,
            total=Decimal(total),
            criado_em=timezone.now(),
            status='Pendente'
        )

        # Criar os itens do pedido e atualizar o estoque
        for item in carrinho.itemcarrinho_set.all():
            produto = item.produto
            quantidade = item.quantidade
            preco_unitario = produto.preco_marketing_promocional or produto.preco_marketing

            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=quantidade,
                preco=Decimal(preco_unitario)
            )

            # Atualizar o estoque
            produto.estoque -= quantidade
            produto.save()

        # Limpar o carrinho após a finalização da compra
        carrinho.ativo = False
        carrinho.save()

        messages.success(request, "Compra finalizada com sucesso!")
        return redirect('produto:pedidoconfirmado')

def view_de_erro(request):
    return render(request, 'produto/erro.html')