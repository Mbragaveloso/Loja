from django import template
from utils import utils

register = template.Library()

@register.filter
def formata_preco(val):
    return utils.formata_preco(val)

@register.filter
def cart_total_qtd(carrinho):
    try:
        return sum(item['quantidade'] for item in carrinho.values())
    except Exception:
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
    except (ValueError, TypeError):
        return 0