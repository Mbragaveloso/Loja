from django.contrib import admin
from . import models


class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    extra = 1
    

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_marketing', 'preco_marketing_promocional')
    fields = ['nome', 'descricao_curta', 'preco_marketing', 'preco_marketing_promocional']
    readonly_fields = ['preco_formatado', 'preco_promocional_formatado']  # Atualize aqui
    
    def preco_formatado(self, obj):
        return obj.get_preco_formatado()  # Substitua pelo método correto que formata o preço

    def preco_promocional_formatado(self, obj):
        return obj.get_preco_promocional_formatado()  # Substitua pelo método correto que formata o preço promocional

    preco_formatado.short_description = 'Preço Formatado'
    preco_promocional_formatado.short_description = 'Preço Promocional Formatado'

    inlines = [VariacaoInline]


class VariacaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'preco')
    fields = ['produto', 'preco']

admin.site.register(models.Produto, ProdutoAdmin)
admin.site.register(models.Variacao, VariacaoAdmin)