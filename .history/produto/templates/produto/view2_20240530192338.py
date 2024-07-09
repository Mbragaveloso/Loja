from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from .models import Produto, Variacao
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Carrinho, ItemCarrinho

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
        variacao = get_object_or_404(Variacao, id=variacao_id)
        
        carrinho = request.session.get('carrinho', {})
        
        if variacao_id in carrinho:
            carrinho[variacao_id]['quantidade'] += 1
        else:
            carrinho[variacao_id] = {
                'produto_nome': produto.nome,
                'variacao_nome': variacao.nome,
                'quantidade': 1,
                'preco_unitario': str(variacao.preco_marketing),
                'preco_unitario_promocional': str(variacao.preco_marketing_promocional) if variacao.preco_marketing_promocional else None,
                'slug': produto.slug, # item incluido
                'imagem': produto.imagem.url if produto.imagem else None,
                'variacao_id': variacao_id  # Adicione este campo
            }
        
        request.session['carrinho'] = carrinho
        return redirect('produto:carrinho')

class RemoverDoCarrinho(View):
    def post(self, request, variacao_id):
        carrinho = request.session.get('carrinho', {})
         # Verificando se a variacao_id está sendo recebido corretamente
        print(f"Tentando remover variacao_id: {variacao_id}")
        print(f"Carrinho antes da remoção: {carrinho}")

        if str(variacao_id) in carrinho:  # Certifique-se de comparar strings, pois o id na sessão pode estar como string
            del carrinho[str(variacao_id)]
            request.session['carrinho'] = carrinho
            messages.success(request, "O item foi removido do carrinho.")
        else:
            messages.error(request, "O item não foi encontrado no carrinho.")

        print(f"Carrinho depois da remoção: {carrinho}")
        return redirect('produto:carrinho')

class CarrinhoView(View):
    def get(self, request):
        carrinho = request.session.get('carrinho', {})
        itens_carrinho = []

        # Iterar sobre os itens do carrinho e buscar as informações de preço necessárias
        for variacao_id, item in carrinho.items():
            preco_unitario = item.get('preco_sem_desconto') if 'preco_com_desconto' not in item else item.get('preco_com_desconto')

            # Obter a instância da variação do banco de dados
            variacao = get_object_or_404(Variacao, id=variacao_id)
            preco_marketing = variacao.preco_marketing
            preco_marketing_promocional = variacao.preco_marketing_promocional
            
            quantidade = item.get('quantidade')

            # Calcular o valor total para este item do carrinho
            valor_total = quantidade * float(preco_unitario)

            # Criar um dicionário com as informações do item e adicionar à lista de itens do carrinho
            item_carrinho = {
                'variacao': variacao,
                'quantidade': quantidade,
                'preco_unitario': preco_unitario,
                'preco_marketing': preco_marketing,
                'preco_marketing_promocional': preco_marketing_promocional,
                'valor_total': valor_total,
                # Outras informações que você deseja incluir no contexto
            }
            itens_carrinho.append(item_carrinho)

        # Renderizar o template com os dados do carrinho
        return render(request, 'produto/carrinho.html', {'itens_carrinho': itens_carrinho})
    

class Finalizar(View):
    def post(self, request, *args, **kwargs):
        # Lógica para finalizar a compra
        messages.success(request, "Sua compra foi finalizada com sucesso!")
        return redirect('produto:lista')

def view_de_erro(request):
    # Lógica para exibir uma página de erro personalizada
    return render(request, 'produto/erro.html')

def verificar_sessao_carrinho(request):
    # Obter o conteúdo da sessão do carrinho
    carrinho = request.session.get('carrinho', {})
    
    # Converter o conteúdo do carrinho em JSON para exibição
    carrinho_json = json.dumps(carrinho, indent=4)
    
    # Retornar uma resposta HTTP com o conteúdo do carrinho
    return HttpResponse(carrinho_json, content_type='application/json')
