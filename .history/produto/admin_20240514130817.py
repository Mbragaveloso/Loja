from django.contrib import admin
from . import models


class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    extra = 1
    

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco')
    fields = ['nome', 'descricao_curta', 'preco_marketing', 'preco_marketing_promocional']
    readonly_fields = ['get_preco_formatado', 'get_preco_promocional_formatado']
    inlines = [VariacaoInline]


admin.site.register(models.Produto, ProdutoAdmin) # registrando a classe produto
admin.site.register(models.Variacao) # registrando as