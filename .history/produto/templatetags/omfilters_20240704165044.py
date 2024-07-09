from django import template
from utils import utils

register = template.Library()

@register.filter
def formata_preco(val):
    return utils.formata_preco(val)

@register.filter
def cart_total_qtd(user):
    # Implemente a lógica para calcular o total de itens no carrinho para o usuário
    try:
        carrinho = Carrinho.objects.get(usuario=user)
        total_qtd = carrinho.total_de_itens()  # Supondo que você tenha um método 'total_de_itens' no seu modelo Carrinho
        return total_qtd
    except Carrinho.DoesNotExist:
        return 0

@register.filter
def cart_totals(carrinho):
    return utils.cart_totals(carrinho)

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
    
@register.filter
def custom_sum(value, arg):
    try:
        return float(value) + float(arg)  # Corrigido de mul para sum
    except(ValueError, TypeError):
        return 0