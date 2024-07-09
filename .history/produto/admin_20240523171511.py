from django.contrib import admin
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
        'exibir_com_ssd', 
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

    def exibir_com_ssd(self, obj):
        return "Com SSD" if "SSD" in obj.nome else "Sem SSD"
    exibir_com_ssd.short_description = 'Com SSD ou Sem SSD'

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