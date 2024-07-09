from django.contrib import admin
from .models import Carrinho, Produto, Variacao, ItemCarrinho, Perfil


class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'idade', 'cpf', 'cidade', 'estado')
    search_fields = ('usuario__username', 'cpf', 'cidade', 'estado')

admin.site.register(Perfil, PerfilAdmin)