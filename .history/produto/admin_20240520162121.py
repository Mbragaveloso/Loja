from django.contrib import admin
from .models import Produto, Variacao

class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 1

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_marketing', 'preco_marketing_promocional', 'tipo')
    search_fields = ('nome', 'descricao_curta', 'descricao_longa')
    list_filter = ('tipo', 'preco_marketing', 'preco_marketing_promocional')
    fields = ('nome', 'descricao_curta', 'descricao_longa', 'imagem', 'slug', 'preco_marketing', 'preco_marketing_promocional', 'tipo')


    def preco_formatado(self, obj):
        return obj.get_preco_formatado()

    def preco_promocional_formatado(self, obj):
        return obj.get_preco_promocional_formatado()

    def imagem_preview(self, obj):  # Método para exibir uma miniatura da imagem na administração
        if obj.imagem:
            return '<img src="{}" width="100" />'.format(obj.imagem.url)
        else:
            return 'Sem imagem'

    preco_formatado.short_description = 'Preço'
    preco_promocional_formatado.short_description = 'Preço Promo.'
    imagem_preview.short_description = 'Imagem'  # Definindo o cabeçalho da coluna de miniaturas

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao)