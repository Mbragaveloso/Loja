from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from .models import Produto, Variacao
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Produto
from .models import Carrinho


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
        tamanho = request.POST.get('tamanho')  # Captura o tamanho do formulário

        # Verifica se tamanho foi fornecido
        if not tamanho:
            messages.error(request, "Por favor, selecione um tamanho.")
            return redirect('produto:detalhe', slug=produto.slug)
        
        variacao = get_object_or_404(Variacao, id=variacao_id)
        
        carrinho = request.session.get('carrinho', {})
        # Gera um identificador único para a combinação de variação e tamanho
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
                'tamanho': tamanho  # Adicione o tamanho ao carrinho
            }
            
            # Atualiza o estoque da variação do produto
        variacao.estoque -= 1
        variacao.save()
        
        request.session['carrinho'] = carrinho
        print(request.session['carrinho'])
        
        return redirect('produto:carrinho')

class RemoverDoCarrinho(View):
    def post(self, request, variacao_id):
        carrinho = request.session.get('carrinho', {})
        tamanho = request.POST.get('tamanho')  # Recupera o tamanho do formulário
        item_id = f"{variacao_id}-{tamanho}"  # Gera o ID do item a ser removido
        
        if item_id in carrinho:
            quantidade_removida = carrinho[item_id]['quantidade'] 
            del carrinho[item_id]
            request.session['carrinho'] = carrinho
            
            # Atualiza o estoque da variação do produto
            variacao = get_object_or_404(Variacao, id=variacao_id)
            variacao.estoque += quantidade_removida
            variacao.save()
            
            messages.success(request, "O item foi removido do carrinho.")
        
        return redirect('produto:carrinho')
    
class CarrinhoView(View):
    def get(self, request):
        carrinho = request.session.get('carrinho', {})
        return render(request, 'produto/carrinho.html', {'carrinho': carrinho})
    
class ResumoDaCompra(View):
    template_name = 'produto/resumodacompra.html'  # Ajuste o nome do template conforme necessário

    def get(self, request, *args, **kwargs):
        # Recuperar os itens do carrinho da sessão
        carrinho = request.session.get('carrinho', {})
        
        # Lista para armazenar os detalhes dos produtos no carrinho
        produtos_no_carrinho = []
        total = 0
        
        # Iterar sobre os itens do carrinho
        for item_id, detalhes_produto in carrinho.items():
            nome_produto = detalhes_produto['produto_nome']
            preco_unitario = float(detalhes_produto.get('preco_unitario_promocional') or detalhes_produto['preco_unitario'])
            quantidade = detalhes_produto['quantidade']
            subtotal = preco_unitario * quantidade
            total += subtotal
            
            # Adicionar detalhes do produto à lista de produtos no carrinho
            produtos_no_carrinho.append({
                'nome': nome_produto,
                'preco_unitario': preco_unitario,
                'quantidade': quantidade,
                'subtotal': subtotal,
            })
        
        # Contexto a ser passado para o template
        context = {
            'produtos': produtos_no_carrinho,
            'total': total,
        }
        
        return render(request, self.template_name, context)
    
class FinalizarCompra(View):
    def post(self, request, *args, **kwargs):
        total = 0
        carrinho = request.session.get('carrinho', {})
        produtos_no_carrinho = []

        for item in carrinho.values():
            preco_unitario = float(item.get('preco_unitario_promocional') if item.get('preco_unitario_promocional') else item.get('preco_unitario'))
            quantidade = item['quantidade']
            subtotal = preco_unitario * quantidade
            total += subtotal

            produtos_no_carrinho.append({
                'produto_nome': item['produto_nome'],
                'preco_unitario': preco_unitario,
                'quantidade': quantidade,
                'subtotal': subtotal,
            })

        # Salva os dados na sessão para serem usados na página de pedido confirmado
        request.session['produtos_no_carrinho'] = produtos_no_carrinho
        request.session['total'] = total

        # Limpar o carrinho após a compra ser finalizada
        request.session['carrinho'] = {}

        return redirect('produto:pedidoconfirmado')
    
class PedidoConfirmado(View):
    def get(self, request, *args, **kwargs):
        # Recupera os dados da sessão que foram salvos pela view FinalizarCompra
        produtos_no_carrinho = request.session.get('produtos_no_carrinho', [])
        total = request.session.get('total', 0)

        context = {
            'produtos': produtos_no_carrinho,
            'total': total,
        }

        # Limpa os dados da sessão após serem usados
        del request.session['carrinho']
        del request.session['total']

        return render(request, 'produto/pedidoconfirmado.html', context)
    
def view_de_erro(request):
    # Lógica para exibir uma página de erro personalizada
    return render(request, 'produto/erro.html')


