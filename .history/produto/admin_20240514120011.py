from django.contrib import admin
from . import models

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco')  
    
    
class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    extra = 1
    

class ProdutoAdmin(admin.ModelAdmin):
    display_fields = ['nome', 'descricao_curta',
                      'get_preco_formatado', 'get_preco_promocional_formatado']
    inlines = [
        VariacaoInline
    ]
    
    
admin.site.register(models.Produto)
admin.site.register(models.Varia)
verbose_name_plural = 'Variações'