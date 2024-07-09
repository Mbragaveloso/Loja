from django.contrib import admin
from django.utils.html import format_html
from . import models

class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    extra = 1

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_marketing', 'preco_marketing_promocional', 'imagem_thumbnail')  # Adicionando 'imagem_thumbnail' à lista de exibição
    fields = ['nome', 'descricao_curta', 'preco_marketing', 'preco_marketing_promocional', 'imagem']  # Incluindo 'imagem' nos campos editáveis
    readonly_fields = ['preco_formatado', 'preco_promocional_formatado', 'imagem_thumbnail']  # Adicionando 'imagem_thumbnail' aos campos somente leitura

    def preco_formatado(self, obj):
        return obj.get_preco_formatado()
    
    def preco_promocional_formatado(self, obj):
        return obj.get_preco_promocional_formatado()

    def imagem_thumbnail(self, obj):  # Método para exibir uma miniatura da imagem na administração
        if obj.imagem:
            return format_html('<img src="{}" width="50" />', obj.imagem.url)
        else:
            return 'Sem imagem'

    preco_formatado.short_description = 'Preço'
    preco_promocional_formatado.short_description = 'Preço Promocional'
    imagem_thumbnail.short_description = 'Imagem'  # Definindo o cabeçalho da coluna de miniaturas

    inlines = [VariacaoInline]

admin.site.register(models.Produto, ProdutoAdmin)