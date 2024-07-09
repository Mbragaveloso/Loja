from django import template
from crispy_forms.templatetags.crispy_forms_tags import render_crispy as crispy_render_crispy

register = template.Library()

@register.simple_tag
def render_crispy(form):
    return crispy_render_crispy(form)

def render_form_with_crispy(form):
    # Aqui você pode usar o filtro render_crispy para renderizar o formulário
    return render_crispy(form)

from django import template
from utils import utils


register = template.Library()

@register.filter
def formata_preco(val):
    return utils.formata_preco(val)

@register.filter
def cart_total_qtd(carrinho):
    return utils.cart_total_qtd(carrinho)

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
def sum(value, arg):
    try:
        return float(value) * float(arg)
    except(ValueError, TypeError):
        return 0 
