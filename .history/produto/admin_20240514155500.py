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
    get get_preco(self, obj):
        return obj.preco  # Substitua por um método ou atributo que retorne o preço

    get_preco.short_description = 'Preço'  # Substitua pelo nome do campo 'preco' no modelo Variacao
    

admin.site.register(models.Produto, ProdutoAdmin) # Registrando a classe ProdutoAdmin para o modelo Produto
admin.site.register(models.Variacao, VariacaoAdmin) # Registrando o modelo Variacao