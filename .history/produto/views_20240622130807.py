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
        
        request.session['carrinho'] = carrinho
        print(request.session['carrinho'])
        
        return redirect('produto:carrinho')

class RemoverDoCarrinho(View):
    def post(self, request, variacao_id):
        carrinho = request.session.get('carrinho', {})
        tamanho = request.POST.get('tamanho')  # Recupera o tamanho do formulário
        item_id = f"{variacao_id}-{tamanho}"  # Gera o ID do item a ser removido
        
        if item_id in carrinho:
            del carrinho[item_id]
            request.session['carrinho'] = carrinho
            messages.success(request, "O item foi removido do carrinho.")
        
        return redirect('produto:carrinho')
    
class CarrinhoView(View):
    def get(self, request):
        carrinho = request.session.get('carrinho', {})
        return render(request, 'produto/carrinho.html', {'carrinho': carrinho})

class ResumoDaCompra(View):
    def post(self, request):
        # Lógica para finalizar a compra
        messages.success(request, "Sua compra foi finalizada com sucesso!")
        return redirect(request, 'produto:resumodacompra.html')
    
    def post(self, request):
        # Lógica para processar a finalização da compra
        # Exemplo: processar pagamento, salvar pedido no banco de dados, etc.
        # Após o processamento, pode ser necessário redirecionar para uma página de confirmação
        return HttpResponse('Compra finalizada com sucesso!')  # Exemplo simples de resposta

    # Se necessário, adicione lógica para outros métodos HTTP, como PUT, DELETE, etc.

def view_de_erro(request):
    # Lógica para exibir uma página de erro personalizada
    return render(request, 'produto/erro.html')
