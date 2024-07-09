from django.contrib import admin
from . import models


class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    extra = 1
    

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_marketing', 'preco_marketing_promocional')
    fields = ['nome', 'descricao_curta', 'preco_marketing', 'preco_marketing_promocional']
    readonly_fields = ['get_preco_formatado', 'get_preco_promocional_formatado']
    inlines = [VariacaoInline]

class VariacaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'preco')  # Adicione outros campos que deseja exibir na lista
    fields = ['produto', 'preco']  # Campos a serem exibidos no formulário de edição
    # Adicione outros campos conforme necessário

admin.site.register(models.Produto, ProdutoAdmin) # Registrando a classe ProdutoAdmin para o modelo Produto
admin.site.register(models.Variacao) # Registrando o modelo Variacao