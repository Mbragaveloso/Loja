from django.template import Library


register = Library()


@register
def formata_preco(val):
    return f'R$ {val: 2f}'.replace('.', ',')