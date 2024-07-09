from django import forms
from django.db import models
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Produto
from django import forms

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ('nome', 'descricao_curta', 'descricao_longa', 'imagem', 'slug', 'preco_marketing', 'preco_marketing_promocional', 'tipo')
        labels = {
            'preco_marketing': 'Preço',
            'preco_marketing_promocional': 'Preço Promocional',
        }

class ListaProdutos(ListView):
    model = Produto
    template_name = 'produto/lista.html'  # Definição do caminho do template aqui
    context_object_name = 'produtos'
    
class DetalheProduto(DetailView):
    model = Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'  # Corrigido para singular
    slug_url_kwarg = 'slug'

class RemoverItemCarrinhoForm(forms.Form):
    variacao_id = forms.IntegerField(widget=forms.HiddenInput)
    tamanho = forms.CharField(max_length=100, widget=forms.HiddenInput)