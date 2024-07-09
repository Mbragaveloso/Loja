from django import template
from utils import utils
from produto.models import Carrinho

register = template.Library()

@register.filter
def formata_preco(val):
    return utils.formata_preco(val)

@register.filter
def cart_total_qtd(user):
    try:
        carrinho = Carrinho.objects.get(usuario=user)
        return sum(item['quantidade'] for item in carrinho.itens.values())
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
        return float(value) + float(arg)
    except(ValueError, TypeError):
        return 0