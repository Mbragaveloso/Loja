from django.contrib import admin
from .models import Carrinho, Produto, Variacao, ItemCarrinho
from django.utils.safestring import mark_safe
from .models import Produto, Variacao

class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 1

class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 
        'descricao_curta', 
        'preco_formatado', 
        'preco_promocional_formatado', 
        'tipo', 
        'exibir_promocao',  # Aqui adicionamos o método exibir_promocao
        'imagem_preview'
    )
    search_fields = ('nome', 'descricao_curta', 'descricao_longa')
    list_filter = ('tipo', 'preco_marketing', 'preco_marketing_promocional')
    fields = (
        'nome', 
        'descricao_curta', 
        'descricao_longa', 
        'imagem', 
        'slug', 
        'preco_marketing', 
        'preco_marketing_promocional', 
        'tipo'
    )
    inlines = [VariacaoInline]

    def exibir_promocao(self, obj):
        return "Em Promoção" if obj.preco_marketing_promocional > 0 else "Preço Normal"
    exibir_promocao.short_description = 'Status da Promoção'

    def preco_formatado(self, obj):
        return obj.get_preco_formatado()
    preco_formatado.short_description = 'Preço'

    def preco_promocional_formatado(self, obj):
        return obj.get_preco_promocional_formatado()
    preco_promocional_formatado.short_description = 'Preço Promo.'

    def imagem_preview(self, obj):
        if obj.imagem:
            return mark_safe(f'<img src="{obj.imagem.url}" width="100" />')
        return 'Sem imagem'
    imagem_preview.short_description = 'Imagem'

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao)
admin.site.register(Produto)
admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)